# Netdata Telegram Integration

This guide will help you install Netdata and use the `netdata_to_telegram.py` script to send Netdata alerts to a Telegram chat.

## Installation

### Step 1: Install Netdata

Follow the official Netdata installation guide to install Netdata on your system:

```bash
wget -O /tmp/netdata-kickstart.sh https://get.netdata.cloud/kickstart.sh && sh /tmp/netdata-kickstart.sh
```

### Step 2: Clone the Repository

Clone the `netdata-telegram` repository to your local machine:

```bash
git clone https://github.com/yourusername/netdata-telegram.git
cd netdata-telegram
```

### Step 3: Install Dependencies

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

### Step 4: Configure Telegram Bot

1. Create a new bot on Telegram by talking to [BotFather](https://t.me/botfather) and get the API token.
2. Get your chat ID by talking to [userinfobot](https://t.me/userinfobot).

### Step 5: Update Configuration

Edit the `config.json` file with your Telegram bot token and chat ID:

```json
{
    "telegram_token": "YOUR_TELEGRAM_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID",
    "netdata_servers": ["IP_SERVER_1", "IP_SERVER_2", "IP_SERVER_3"]
}
```

## Usage

### Step 6: Set Up Service to run netdata_to_telegram.py

Create a systemd service to run the `netdata_to_telegram.py` script automatically:

1. Create a new service file:

```bash
sudo nano /etc/systemd/system/netdata-telegram.service
```

2. Add the following content to the service file:

```ini
[Unit]
Description=Netdata to Telegram Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/netdata-telegram/netdata_to_telegram.py
WorkingDirectory=/path/to/netdata-telegram
Restart=always
User=yourusername

[Install]
WantedBy=multi-user.target
```

3. Reload systemd to apply the new service:

```bash
sudo systemctl daemon-reload
```

4. Enable and start the service:

```bash
sudo systemctl enable netdata-telegram.service
sudo systemctl start netdata-telegram.service
```

5. Check the status of the service to ensure it is running:

```bash
sudo systemctl status netdata-telegram.service
```
