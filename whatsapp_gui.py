import streamlit as st
import pywhatkit as kit
from datetime import datetime
from mysql.connector import connect, Error
from googletrans import Translator
import os
import pandas as pd

# Initialize Translator for multi-language support
translator = Translator()

# MySQL Database Configuration
DB_CONFIG = {
    "host": "localhost",     
    "user": "root",          
    "password": "1234",  
    "database": "whatsapp_db"
}

# Function to create message_logs table if not exists
def initialize_database():
    try:
        with connect(**DB_CONFIG) as conn:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS message_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                country_code VARCHAR(5),
                phone_number VARCHAR(15),
                file_type VARCHAR(20),
                message TEXT,
                file_path VARCHAR(255),
                timestamp DATETIME,
                status VARCHAR(50)
            )
            """
            with conn.cursor() as cursor:
                cursor.execute(create_table_query)
                conn.commit()
    except Error as e:
        st.error(f"Database Error: {e}")

# Initialize Database
initialize_database()

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Country code list
COUNTRY_CODES = ["+1", "+91", "+44", "+61", "+81", "+86", "+33", "+49", "+39", "+7", "+34", "+971", "+93", "+55", "+27"]

# Title
st.title("WhatsApp Automation")

# Sidebar: Message Log Viewer
st.sidebar.header("Message Logs")
if st.sidebar.button("Refresh Logs"):
    try:
        with connect(**DB_CONFIG) as conn:
            logs_query = "SELECT * FROM message_logs"
            logs = pd.read_sql(logs_query, conn)
            st.sidebar.dataframe(logs)
    except Error as e:
        st.sidebar.error(f"Failed to fetch logs: {e}")

# Country code dropdown
country_code = st.selectbox("Select Country Code", COUNTRY_CODES)

# Phone number input
phone_number = st.text_input("Enter Phone Number (without country code)")

# File type selection
file_type = st.selectbox("Select Type", ["Message", "Image", "Video", "Document"])

# File uploader (for image, video, or document)
local_file_path = None
if file_type != "Message":
    uploaded_file = st.file_uploader("Upload File", type=["jpg", "png", "mp4", "pdf", "docx", "xlsx"])
    if uploaded_file:
        local_file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(local_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved to {local_file_path}")

# Message text area (optional for images/videos, required for messages)
message = None
if file_type == "Message" or file_type in ["Image", "Video"]:
    message = st.text_area("Enter Message Text (Optional for images/videos)")

# Multi-language support
if message:
    st.write("Translate Message (Optional)")
    target_language = st.selectbox("Select Language to Translate", ["None", "es", "fr", "de", "zh", "hi", "ar"])
    if target_language != "None":
        translated_message = translator.translate(message, dest=target_language).text
        st.write(f"Translated Message: {translated_message}")
        message = translated_message

# Time selection
st.write("**Set Time to Send:**")
send_immediately = st.checkbox("Send Immediately")

if not send_immediately:
    # Time scheduling dropdowns
    st.write("Choose Scheduled Time:")
    hours = st.selectbox("Hour", list(range(1, 13)))
    minutes = st.selectbox("Minute", list(range(0, 60)))
    am_pm = st.selectbox("AM/PM", ["AM", "PM"])

# Send button
if st.button("Send Message"):
    if not phone_number:
        st.error("Please enter the phone number.")
    elif not country_code:
        st.error("Please select a country code.")
    elif file_type != "Message" and not local_file_path:
        st.error("Please upload a file for Image, Video, or Document.")
    else:
        try:
            # Convert 12-hour format to 24-hour format if scheduling
            if not send_immediately:
                if am_pm == "PM" and hours != 12:
                    hours += 12
                elif am_pm == "AM" and hours == 12:
                    hours = 0

            # Full phone number with country code
            full_number = f"{country_code}{phone_number}"

            # Get current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Send message or file
            if file_type == "Message":
                if send_immediately:
                    current_time = datetime.now()
                    kit.sendwhatmsg(full_number, message, current_time.hour, current_time.minute + 1)
                else:
                    kit.sendwhatmsg(full_number, message, hours, minutes)
            elif file_type == "Image":
                kit.sendwhats_image(receiver=full_number, img_path=local_file_path, caption=message)
            elif file_type == "Video":
                kit.sendwhats_document(receiver=full_number, document=local_file_path)

            elif file_type == "Document":
                kit.sendwhats_document(phone_no=full_number, document=local_file_path)

            # Log the message
            with connect(**DB_CONFIG) as conn:
                insert_query = """
                    INSERT INTO message_logs (country_code, phone_number, file_type, message, file_path, timestamp, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                with conn.cursor() as cursor:
                    cursor.execute(insert_query, (
                        country_code, phone_number, file_type, message, 
                        local_file_path if local_file_path else None, timestamp, "Sent"
                    ))
                    conn.commit()

            st.success("Message sent successfully!")
        except Exception as e:
            # Log the error
            with connect(**DB_CONFIG) as conn:
                insert_query = """
                    INSERT INTO message_logs (country_code, phone_number, file_type, message, file_path, timestamp, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                with conn.cursor() as cursor:
                    cursor.execute(insert_query, (
                        country_code, phone_number, file_type, message, 
                        local_file_path if local_file_path else None, timestamp, f"Failed: {e}"
                    ))
                    conn.commit()

            st.error(f"An error occurred: {e}")
