# WhatsApp Automation Hub

A powerful and flexible tool to automate sending messages, images, videos, and documents via WhatsApp. This project includes multi-language support, scheduling, and logging for efficient message management.

## Features
- **Send Messages**: Automate WhatsApp messages to any phone number.
- **Send Images, Videos, and Documents**: Upload and send various media files.
- **Multi-Language Support**: Automatically translate messages to different languages using Google Translate.
- **Message Scheduling**: Schedule messages to be sent at specific times.
- **Message Logs**: View detailed logs of all sent and failed messages, including the status and time.
- **Database Integration**: Store message logs in a MySQL database for efficient tracking.

## Tech Stack
- **Backend**: Python
- **Web Framework**: Streamlit
- **WhatsApp Automation**: `pywhatkit`
- **Database**: MySQL
- **Translation**: Google Translate API
- **File Handling**: `os` and `pandas` for handling files and logs.

## Setup & Installation

### Prerequisites
- Python 3.x
- MySQL Database
- Install the following Python packages:
  - `pywhatkit`
  - `mysql-connector-python`
  - `googletrans`
  - `streamlit`
  - `pandas`

### Installation Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/whatsapp-automation-hub.git
   cd whatsapp-automation-hub
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL Database:**

   - Create a database named whatsapp_db.
   - Use the following query to create the message_logs table:
```bash
CREATE TABLE IF NOT EXISTS message_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_code VARCHAR(5),
    phone_number VARCHAR(15),
    file_type VARCHAR(20),
    message TEXT,
    file_path VARCHAR(255),
    timestamp DATETIME,
    status VARCHAR(50)
);
```

4. **Run the Streamlit Application:**

```bash
streamlit run app.py
```

The app will be accessible at **http://localhost:8501**

## **How to Use**
- Select Country Code: Choose from a list of supported country codes.
- Enter Phone Number: Enter the recipient's phone number (without the country code).
- Choose File Type: Select between sending a message, image, video, or document.
- Upload File (Optional): For images, videos, or documents, upload the desired file.
- Message Input: Optionally enter a text message (or image/video caption).
- Multi-Language Support: Optionally translate your message into different languages.
- Schedule Message: Choose to send the message immediately or at a scheduled time.
- Send: Click "Send Message" to execute the task.

### Known Issues in Video & Document Sending:
- **Issue**: There are known issues with sending video files and documents through `pywhatkit`. These file types may not be sent successfully, and you may encounter errors or failures when attempting to send them.
- **Status**: This issue is being actively investigated. Future versions of the project may include fixes or alternative methods for handling media files. I recommend using image files until the issue is resolved.

I am committed to improving this functionality and appreciate your patience as I work on a solution.

## **Logging and Tracking**
- All sent and failed messages are logged in the MySQL database for future reference.
- You can view the message logs via the Streamlit sidebar.
