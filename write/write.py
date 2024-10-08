#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import signal

GPIO.setwarnings(False)

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522()

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MFRC522.PICC_REQIDL)

    # If a card is found
    if status == MFRC522.MI_OK:
        print("Card detected")
    
        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MFRC522.MI_OK:
            # Print UID
            print("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
    
            # This is the default key for authentication
            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        
            # Select the scanned tag
            MIFAREReader.MFRC522_SelectTag(uid)

            # Authenticate
            status = MIFAREReader.MFRC522_Auth(MFRC522.PICC_AUTHENT1A, 8, key, uid)
            print("\n")

            # Check if authenticated
            if status == MFRC522.MI_OK:
                # Variable for the data to write
                data = [0xFF] * 16

                print("Sector 8 looked like this:")
                # Read block 8
                MIFAREReader.MFRC522_Read(8)
                print("\n")

                print("Sector 8 will now be filled with 0xFF:")
                # Write the data
                MIFAREReader.MFRC522_Write(8, data)
                print("\n")

                print("It now looks like this:")
                # Check to see if it was written
                MIFAREReader.MFRC522_Read(8)
                print("\n")

                data = [0x00] * 16

                print("Now we fill it with 0x00:")
                MIFAREReader.MFRC522_Write(8, data)
                print("\n")

                print("It is now empty:")
                # Check to see if it was written
                MIFAREReader.MFRC522_Read(8)
                print("\n")

                # Stop
                MIFAREReader.MFRC522_StopCrypto1()

                # Make sure to stop reading for cards
                continue_reading = False
            else:
                print("Authentication error")

