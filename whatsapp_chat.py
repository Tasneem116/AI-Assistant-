# import pywhatkit as kit
# import datetime
#
# # Replace 'Your Message' and 'Contact Name' with your message content and the recipient's name.
# message = "testing whatsapp message"
# contact_name = "Personal (You)"
#
# # Set the time at which you want to send the message (24-hour format).
# send_time_hour = 11  # Replace with the desired hour.
# send_time_minute = 58  # Replace with the desired minute.
#
# # Calculate the current date and time.
# now = datetime.datetime.now()
# current_hour = now.hour
# current_minute = now.minute
#
# # Calculate the time delay in seconds until the scheduled message.
# time_delay_seconds = ((send_time_hour - current_hour) * 3600) + ((send_time_minute - current_minute) * 60)
#
# # Send the message.
# try:
#     kit.sendwhatmsg(f"+919581669518", message, now.hour, now.minute + 2)  # Replace with the recipient's phone number.
#     print(f"Message to {contact_name} scheduled for {send_time_hour}:{send_time_minute}.")
# except Exception as e:
#     print(f"An error occurred: {str(e)}")


import pywhatkit as kit
import datetime

# Set the target phone number (with the country code)
phone_number = "+919581669518"

# Message to send
message = "Hello, this is an automated WhatsApp message sent from Python!"

# Schedule the message (optional)
# This example schedules the message to be sent immediately.
now = datetime.datetime.now()
hour = now.hour
minute = now.minute + 1  # Send the message one minute from now
print(f"Scheduled to send at: {hour}:{minute}")
kit.sendwhatmsg(phone_number, message, hour, minute)


import pyautogui_test
import time

# def send_whatsapp_message(contact_name, message):
#     # Adjust these coordinates based on your screen resolution and browser size
#     browser_x = 1000
#     browser_y = 100
#     message_x = 200
#     message_y = 800
#
#     # Click on the browser to focus
#     pyautogui.click(browser_x, browser_y)
#     time.sleep(2)  # Wait for the browser to focus
#
#     # Search for the contact
#     pyautogui.hotkey('ctrl', 'f')  # Press Ctrl + F to search
#     pyautogui.write(contact_name)
#     time.sleep(1)
#     pyautogui.press('enter')
#     time.sleep(1)
#
#     # Type and send the message
#     pyautogui.click(message_x, message_y)  # Click on the message input field
#     pyautogui.write(message)
#     pyautogui.press('enter')
#
# # Example usage
# send_whatsapp_message("Personal (You)", "Hello, this is an automated message.")

# Add additional error handling and adjust coordinates as needed.


