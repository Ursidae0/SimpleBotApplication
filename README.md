# Daily Message App for Telegram

This script allows you to schedule and send daily motivational messages to a specified Telegram chat using a Telegram bot.

## Features
- Automatically sends a motivational message every day at a scheduled time.
- Dynamically generates daily tasks, such as the number of pushups and situps, based on a progression model.
- Includes retry logic for failed message deliveries.
- Configurable via environment variables.

## Prerequisites
- Python 3.6+
- A Telegram bot token (generated via [BotFather](https://core.telegram.org/bots#botfather)).
- Your Telegram chat ID (can be obtained using the bot or other Telegram tools).

## Setup

### Install Required Libraries
Install the dependencies using pip:
```bash
pip install requests numpy
```

### Set Environment Variables
Set the following environment variables to configure the script:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
- `TELEGRAM_CHAT_ID`: The chat ID of the recipient.

Example (Linux/Mac):
```bash
export TELEGRAM_BOT_TOKEN="<your_bot_token>"
export TELEGRAM_CHAT_ID="<your_chat_id>"
```

Example (Windows):
```cmd
set TELEGRAM_BOT_TOKEN=<your_bot_token>
set TELEGRAM_CHAT_ID=<your_chat_id>
```

### Logging Permissions
Ensure the log file (`daily_message.log`) has proper permissions:
```bash
chmod 600 daily_message.log
```

## Usage
Run the script with the desired hour and minute for the daily message:

```bash
python Daily_Message_App_For_Telegram.py <hour> <minute>
```

- `<hour>`: The hour of the day (24-hour format) to send the message.
- `<minute>`: The minute of the hour to send the message.

### Example
To send a message at 7:30 AM every day:
```bash
python Daily_Message_App_For_Telegram.py 7 30
```

## How It Works
1. The script reads the bot token and chat ID from environment variables.
2. It generates a list of progressively increasing tasks (e.g., pushups and situps) using a multiplier.
3. It sends a message at the scheduled time each day and retries up to 3 times in case of failure.
4. Logs are maintained in `daily_message.log` for debugging and monitoring.

## Example Output
Telegram message sent by the bot:
```
Today you should do 10 pushups and situps.
```

## Notes
- Ensure your bot is added to the target chat (and granted admin privileges if necessary).
- Rotate your bot token periodically for security.
- Handle large group chat IDs carefully, as they may have special formatting.

## Contributing
Feel free to contribute to this project by submitting issues or pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
