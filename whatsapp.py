import pywhatkit as kit

phone = '+918260701843'
message = 'Hello! This is a test message sent using Python.'
hour = 1
minute = 4

kit.sendwhatmsg(phone_no = phone, message = message, time_hour = hour, time_min = minute)
print('Message sent successfully')