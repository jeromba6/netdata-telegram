#!/usr/bin/env python3
"""
This script reads the alarms from a netdata server and sends them to a telegram chat.
"""

import httpx
import json
import time
import atexit
import socket


def main():
    # Read configuration
    with open("config.json") as f:
        config = json.load(f)
    token = config["token"]
    chat_id = config["chat_id"]
    netdata_servers = config["netdata_servers"]
    poll_interval = config.get("poll_interval", 60)
    resend_interval = config.get("resend_interval", 60 * 60)
    alive_interval = config.get("alive_interval", 60 * 60 * 24)
    delay = config.get("delay", 300)
    hostname = socket.gethostname()
 
    # Get emojis
    emojis_unicode = emojis()

    # Register exit handler
    atexit.register(exit_handler, token, chat_id, f"{emojis_unicode['broken_heart']} netdata_to_telegram.py stopped on {hostname}")

    # Send start message
    send_to_telegram(token, chat_id, f"{emojis_unicode['heart']} netdata_to_telegram.py started on {hostname}")

    # initialize variables
    last_alarm_times = [0] * len(netdata_servers)
    messages = [""] * len(netdata_servers)
    old_messages = [""] * len(netdata_servers)
    alive_ts = 0

    # Main loop
    while True:
        # Send alive message
        if time.time() - alive_ts > alive_interval and alive_interval > 0:
            send_to_telegram(token, chat_id, f"{emojis_unicode['ok']} netdata_to_telegram.py is alive on {hostname}")
            alive_ts = time.time()

        # Store old message for comparison
        for i, netdata_server in enumerate(netdata_servers):
            old_messages[i] = messages[i]

            # Read alarms from netdata
            alarms, succes = read_netdat_alarms(netdata_server)

            # Convert alarms to message
            if succes:
                # Filter alarms that are to young
                alarms['alarms'] = [ alarm for alarm in alarms['alarms'] if int(alarm['last_status_change']) < time.time() - delay ]
                messages[i] = alarms_to_message(alarms)
            else:
                messages[i] = f"{emojis_unicode['warning']} Error reading alarms from {netdata_server} @ {hostname}"

            # Send message if alarms changed
            if messages[i] != old_messages[i]:
                print(f"Alarms changed on {netdata_server}")
                last_alarm_times[i] = time.time()
                send_to_telegram(token, chat_id, messages[i])

            # Resend message if time has passed
            if time.time() - last_alarm_times[i] > resend_interval and (not succes or alarms["alarms"]):
                print(f"Resending message on {netdata_server}")
                send_to_telegram(token, chat_id, messages[i])
                last_alarm_times[i] = time.time()
        time.sleep(poll_interval)


def exit_handler(token: str, chat_id: str, message: str):
    """
    Send message to telegram when the script is stopped.
    """
    send_to_telegram(token, chat_id, message)


def alarms_to_message(alarms: dict) -> str:
    """
    Convert alarms to a message.
    """
    
    # Get emojis
    emojis_unicode = emojis()

    # Check if there are alarms and create message accordingly
    if len(alarms["alarms"]) > 0:
        message = f"{emojis_unicode['alarm']} There are {len(alarms['alarms'])} Alarm(s) on {alarms['hostname']}:\n"
        for alarm in alarms["alarms"]:
            message += f"  - {alarm}\n"
    else:
        message = f"{emojis_unicode['green_check']} No alarms on {alarms['hostname']}"
    return message


def send_to_telegram(token: str, chat_id: str, message: str) -> dict:
    """
    Send message to telegram chat.
    """
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    try:
        response = httpx.post(url, data=data)
    except httpx.RequestError as e:
        print(f"Error sending message to telegram: {e}")
        return None
    return response.json()


def read_netdat_alarms(server: str) -> dict:
    """
    Read alarms from netdata server and return them as a dictionary.
    """

    default_port = 19999
    if not ':' in server:
        server += f':{default_port}'
    url = f"http://{server}/api/v1/alarms"
    try:
        response = httpx.get(url)
    except httpx.RequestError as e:
        print(f"Error reading alarms from {server}: {e}")
        return None, False
    return response.json(), True


def emojis() -> dict:
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
