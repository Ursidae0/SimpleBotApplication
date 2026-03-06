# Daily Fitness Telegram Bot

A lightweight Python daemon that sends a daily workout message to a Telegram chat at a scheduled time. The message count increments each day using a compound exponential progression — starting at 10 reps and growing by 5% daily over a 100-day program.

Designed to run persistently in the background (e.g., on a home server or Raspberry Pi) without any external scheduler like cron.

---

## How It Works

### Progression Model

```python
# Calculate_Day_Number_Exponential.py
day_n = floor(10 * 1.05 ** n)   # n = 0..99
```

Starting at 10 reps on day 0, the count grows exponentially at 5% per day:

| Day | Reps |
|---|---|
| 0 | 10 |
| 10 | 16 |
| 30 | 43 |
| 60 | 184 |
| 99 | 1,315 |

### Scheduling Mechanism

The bot uses `threading.Timer` for scheduling rather than blocking sleep loops or cron. On each successful send, a new timer is set for `now + 24h` at the target wall-clock time. This avoids drift that would accumulate with `time.sleep(86400)`.

```python
next_run = (datetime.now() + timedelta(days=1)).replace(hour=h, minute=m, second=0)
delay = (next_run - datetime.now()).total_seconds()
threading.Timer(delay, lambda: send_message(...)).start()
```

### Retry Logic

Failed Telegram API calls are retried up to 3 times with a 10-second delay between attempts. HTTP errors are caught via `response.raise_for_status()`. All events (sends, failures, retries) are written to `daily_message.log`.

---

## Architecture

```
Daily_Message_App_For_Telegram.py   - Entry point, scheduler, retry logic
Calculate_Day_Number_Exponential.py - Exponential progression array (100 days)
Constants.py                        - STEP_LENGTH=100, MULTIPLIER=1.05, RETRY_ATTEMPTS=3
```

The `Constants.py` separation means the progression curve (multiplier, length) and retry behavior can be tuned without touching the scheduling logic.

---

## Setup

### 1. Install Dependencies

```bash
pip install requests numpy
```

### 2. Create a Telegram Bot

1. Open Telegram, search for `@BotFather`
2. Run `/newbot` and follow the prompts
3. Copy the bot token

### 3. Get Your Chat ID

Send a message to your bot, then call:
```
https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
```
The `chat.id` field in the response is your Chat ID.

### 4. Set Environment Variables

```bash
# Linux / macOS
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

```cmd
:: Windows
set TELEGRAM_BOT_TOKEN=your_bot_token_here
set TELEGRAM_CHAT_ID=your_chat_id_here
```

Credentials are never stored in code — they are read exclusively from environment variables at startup.

### 5. Run

```bash
python Daily_Message_App_For_Telegram.py <hour> <minute>
```

Example — send at 07:30 AM daily:
```bash
python Daily_Message_App_For_Telegram.py 7 30
```

---

## Deployment Notes

For long-running use, keep the process alive with a process manager:

```bash
# Using nohup (simplest)
nohup python Daily_Message_App_For_Telegram.py 7 30 &

# Using systemd (recommended for Linux servers)
# Create /etc/systemd/system/fitbot.service
# See systemd documentation for service unit file format
```

**Log rotation:** `daily_message.log` grows unbounded. Set up `logrotate` if running for extended periods.

**Token security:** Rotate your bot token periodically via BotFather. Never commit the token to version control — always use environment variables or a secrets manager.

---

## Customization

| Parameter | Location | Description |
|---|---|---|
| `STEP_LENGTH` | `Constants.py` | Number of days in the program (default: 100) |
| `MULTIPLIER` | `Constants.py` | Daily growth rate (default: 1.05 = 5%) |
| `RETRY_ATTEMPTS` | `Constants.py` | API call retries before giving up (default: 3) |
| `RETRY_DELAY` | `Constants.py` | Seconds between retries (default: 10) |
| Message text | `send_message()` | Edit the f-string to change the message format |

To change the exercise type, edit `send_message()` in `Daily_Message_App_For_Telegram.py`:
```python
message = f"Today you should do {data[index]:.0f} pushups and situps."
# Change to any exercise of your choice
```

---

## License

MIT — see `LICENSE` for details.
