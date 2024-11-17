# Netdata Telegram Integration

This guide will help you install Netdata and use the `netdata_to_telegram.py` script to send Netdata alerts to a Telegram chat.

## Installation

### Step 1: Install Netdata

Follow the official Netdata installation guide to install Netdata on your system:

```bash
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
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
    "chat_id": "YOUR_CHAT_ID"
}
```

## Usage

### Step 6: Set Up Netdata Alarm Notification

1. Open the Netdata configuration directory:

```bash
cd /etc/netdata
```

2. Edit the `health_alarm_notify.conf` file and set the following variables:

```bash
DEFAULT_RECIPIENT_TELEGRAM="yourusername"
```

3. Add the following line to the `health_alarm_notify.conf` file to call the `netdata_to_telegram.py` script:

```bash
telegram_send() {
    /path/to/netdata-telegram/netdata_to_telegram.py "$@"
}
```

### Step 7: Restart Netdata

Restart the Netdata service to apply the changes:

```bash
sudo systemctl restart netdata
```

Now, Netdata will send alerts to your specified Telegram chat using the `netdata_to_telegram.py` script.
