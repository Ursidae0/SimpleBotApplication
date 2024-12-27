import datetime as dt
import os
import requests
import numpy as np
import threading
import logging
import time
import sys
from Calculate_Day_Number_Exponential import getValues

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
RETRY_ATTEMPTS = 3
RETRY_DELAY = 10 * SECOND
STEP_LENGTH = 100

# Configure logging
def exists(filepath: str) -> bool:
    return os.path.isfile(filepath)

if not exists('daily_message.log'):
    with open('daily_message.log', 'w'):
        pass

logging.basicConfig(filename='daily_message.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_telegram_message(token: str, chat_id: str, message: str):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending message: {e}")
        return None
    

def checkTokenChatid() -> tuple[str, str]:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        logging.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not set in the environment variables.")
        logging.info("Exiting the program.")
        sys.exit(1)
    return token, chat_id

def send_daily_message():
    token, chat_id = checkTokenChatid()
    data = getValues() #
    index = 0
    send_message(data, index, token, chat_id)
    if index == STEP_LENGTH - 1:
        logging.info("All messages sent. Exiting the program.")
        sys.exit(0)

def send_message(data: np.ndarray, index: int, token: str, chat_id: str):
    message = f"Today you should do {data[index]:.0f} pushups and situps."
    logging.info(f"Sending message: {message}")
    for attempt in range(RETRY_ATTEMPTS):
        response = send_telegram_message(token, chat_id, message)
        if response and response.get("ok"):
            logging.info("Message sent successfully.")
            break
        else:
            logging.warning(f"Retrying... Attempt {attempt + 1}")
            time.sleep(RETRY_DELAY)
    index = (index + 1) % len(data)  

    next_run = (dt.datetime.now() + dt.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    delay = (next_run - dt.datetime.now()).total_seconds()
    threading.Timer(delay, lambda: send_message(data, index, token, chat_id)).start()

def adjustTime(hour: int = 6, minute: int = 0):
    now = dt.datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target < now:
        target += dt.timedelta(days=1)
    delay = (target - now).total_seconds()
    logging.info(f"Scheduling daily message at {target}")
    threading.Timer(delay, send_daily_message).start()

def checkInitialValues():
    if len(sys.argv) != 3:
        logging.error("Please provide hour and minute as command line arguments.")
        sys.exit(1)

    try:
        hour = int(sys.argv[1])
        minute = int(sys.argv[2])
        return hour, minute
    except ValueError:
        logging.error("Hour and minute must be integers.")
        sys.exit(1)

if __name__ == "__main__":
    hour, minute = checkInitialValues()
    adjustTime(hour, minute)
