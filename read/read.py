#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import subprocess

reader = SimpleMFRC522()

try:
    id, text = reader.read()
    print(f"Raw data: {text}")
    # Execute 1.py on successful read
    subprocess.run(["python3", "1.py"])
except Exception as e:
    print(f"Error: {e}")
finally:
    GPIO.cleanup()
