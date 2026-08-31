# Solana CA Forwarder Bot

A Telegram bot that watches messages in one or more chats, detects Solana
contract (token mint) addresses, and forwards each one to a target group or
channel as:

```
/soc <address>
```

## How detection works

Solana addresses are base58-encoded 32-byte public keys. The bot:

1. Scans message text/captions for base58-looking strings 32-44 characters
   long.
2. Attempts to base58-decode each candidate and keeps only the ones that
   decode to exactly 32 bytes — this is what a real Solana address always
   does, so it filters out most look-alike strings (words, hashes of the
   wrong length, etc.).
3. Sends `/soc <address>` (plus an optional "From: ..." line) to your
   configured target chat for every valid address found.

No blockchain calls are made — this only validates the *format* of the
address, not whether a token actually exists at that address.

## 1. Create the bot and get a token

1. Message [@BotFather](https://t.me/BotFather) on Telegram.
2. Send `/newbot` and follow the prompts to get a `BOT_TOKEN`.
3. In [@BotFather](https://t.me/BotFather), send `/setprivacy` for your bot
   and choose **Disable**. This lets the bot read all group messages
   (needed for detection) instead of only messages that mention it.

## 2. Add the bot to your chats

1. Add the bot to the **source** group(s) you want monitored.
2. Add the bot to the **target** group/channel you want addresses forwarded
   to, and make it an admin there if it's a channel (so it can post).
3. In each chat, send `/id` to the bot to get that chat's numeric ID —
   you'll need the target chat's ID for `TARGET_CHAT_ID`, and optionally
   the source chat ID(s) for `SOURCE_CHAT_IDS`.

## 3. Configure environment variables

Copy `.env.example` to `.env` and fill in:

| Variable | Required | Description |
|---|---|---|
| `BOT_TOKEN` | Yes | Token from BotFather |
| `TARGET_CHAT_ID` | Yes | Chat ID to forward `/soc <address>` messages to |
| `SOURCE_CHAT_IDS` | No | Comma-separated chat IDs to watch. Empty = watch every chat the bot is in |
| `INCLUDE_SOURCE_INFO` | No | `true`/`false` — append source chat/user info (default `true`) |

`.env` is gitignored — never commit real tokens.

## 4. Run locally

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then edit .env with your real values
python bot.py
```

## 5. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Solana CA forwarder bot"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

`.env` is excluded by `.gitignore`, so your token won't be pushed. Never
commit `.env` — set the real values as environment variables in Railway
instead (next step).

## 6. Deploy on Railway

1. Go to [railway.com](https://railway.com) and create a **New Project** →
   **Deploy from GitHub repo**, then select the repo you just pushed.
2. Railway will detect Python via Nixpacks and use `railway.json` /
   `Procfile` to run `python bot.py` as a worker.
3. In the Railway project, open **Variables** and add:
   - `BOT_TOKEN`
   - `TARGET_CHAT_ID`
   - `SOURCE_CHAT_IDS` (optional)
   - `INCLUDE_SOURCE_INFO` (optional)
4. Deploy. Check the **Deployments → Logs** tab — you should see
   `Bot starting (polling mode)...`.

The bot uses long polling, so no public URL/webhook is required — it works
out of the box on Railway with just the worker process running.

## Notes / customization ideas

- To forward the *original* message too (not just the address), you could
  swap `send_message` for `forward_message` in `bot.py` in addition to the
  `/soc` line.
- To watch only specific chats, set `SOURCE_CHAT_IDS`.
- To run as a webhook instead of polling (useful for very high traffic),
  swap `application.run_polling(...)` for `application.run_webhook(...)`
  and expose a public port — Railway provides one via the `PORT` env var.
 
