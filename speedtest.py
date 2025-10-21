#!/bin/env python3
"""
This script checks the speed of a network connection using speedtest.net and sends the results to a telegram chat.
"""

import httpx
import os
import json
import socket

def main():
    # Read configuration
    with open("config.json") as f:
        config = json.load(f)
    token = config["token"]
    chat_id = config["chat_id_speed"]
    delay = config.get("delay", 300)
    hostname = socket.gethostname()

    result = os.popen('speedtest-cli --secure').read()
    result = result.split('\n')

    # Remove lines with "Testing" and "Download" or "Upload"
    result = [line for line in result if "Testing" not in line and ("Download" not in line or "Upload" not in line)]
    result = [line for line in result if "Selecting best" not in line]
    result = [line for line in result if "Retrieving" not in line]

    result = "\n".join(result)

    # Send the result to telegram
    print(send_to_telegram(token, chat_id, f"Speedtest on {hostname}\n{result}"))


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


if __name__ == "__main__":
    main()
