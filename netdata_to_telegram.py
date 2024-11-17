#!/usr/bin/env python3
"""
This script reads the alarms from a netdata server and sends them to a telegram chat.
"""

import httpx
import json
import time
import atexit

poll_interval = 60
resend_interval = 60 * 60


def main():
    # Read configuration
    with open("config.json") as f:
        config = json.load(f)
    token = config["token"]
    chat_id = config["chat_id"]
    netdata_server = config["netdata_server"]
 
    # Get emojis
    emojis_unicode = emojis()

    # Register exit handler
    atexit.register(exit_handler, token, chat_id, f"{emojis_unicode['broken_heart']} netdata_to_telegram.py stopped")

    # Send start message
    send_to_telegram(token, chat_id, f"{emojis_unicode['heart']} netdata_to_telegram.py started")

    # initialize variables
    last_alarm_time = 0
    message = ""

    # Main loop
    while True:
        # Store old message for comparison
        old_message = message

        # Read alarms from netdata
        alarms = read_netdat_alarms(netdata_server)

        # Convert alarms to message
        message = alarms_to_message(alarms)

        # Send message if alarms changed
        if message != old_message:
            print("Alarms changed")
            last_alarm_time = time.time()
            send_to_telegram(token, chat_id, message)

        # Resend message if time has passed
        if time.time() - last_alarm_time > resend_interval and alarms["alarms"]:
            print("Resending message")
            send_to_telegram(token, chat_id, message)
            last_alarm_time = time.time()
        time.sleep(poll_interval)


def exit_handler(token, chat_id, message):
    """
    Send message to telegram when the script is stopped.
    """
    send_to_telegram(token, chat_id, message)


def alarms_to_message(alarms):
    """
    Convert alarms to a message.
    """
    
    # Get emojis
    emojis_unicode = emojis()

    # Check if there are alarms and create message accordingly
    if len(alarms["alarms"]) > 0:
        message = f"{emojis_unicode['alarm']} There are {len(alarms['alarm'])} Alarm(s) on {alarms['hostname']}:\n"
        for alarm in alarms["alarms"]:
            message += f"  - {alarm}\n"
    else:
        message = f"{emojis_unicode['green_check']} No alarms on {alarms['hostname']}"
    return message


def send_to_telegram(token, chat_id, message):
    """
    Send message to telegram chat.
    """
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}    
    response = httpx.post(url, data=data)
    return response.json()


def read_netdat_alarms(server):
    """
    Read alarms from netdata server and return them as a dictionary.
    """

    url = f"http://{server}:19999/api/v1/alarms"
    response = httpx.get(url)
    return response.json()


def emojis():
    """
    Return a dictionary with emojis as unicode.
    """
    
    emojis_unicode = {
        "smile": "\U0001F604",
        "sad": "\U0001F621",
        "heart": "\U00002764",
        "fire": "\U0001F525",
        "ok": "\U0001F44C",
        "warning": "\U000026A0",
        "alarm": "\U0001F6A8",
        "check": "\U00002705",
        "green_check": "\U00002714",
        "broken_heart": "\U0001F494",
    }
    return emojis_unicode


if __name__ == "__main__":
    main()
