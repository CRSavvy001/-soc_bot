# 
Solana Address Forwarder Telegram Bot

A Telegram bot that automatically detects Solana contract addresses in messages, adds /nar prefix, and forwards them to another group or channel.

Features

🔍 Automatically detects Solana contract addresses (base58 format, 32-44 characters)

✏️ Adds /nar prefix to detected addresses

📤 Forwards modified addresses to a destination group/channel

🚀 Easy deployment to Railway.app

📝 Comprehensive logging

How It Works

Bot monitors messages in a source group/channel

When a Solana address is detected (e.g., 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU)

Bot adds /nar prefix: /nar7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU

Sends the modified address to the destination group/channel

Setup Instructions

1. Create Your Telegram Bot

Open Telegram and search for @BotFather

Send /newbot command

Follow the prompts to create your bot

Save the Bot Token (looks like 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz)

2. Get Chat IDs

You need two chat IDs:

Source Chat ID: The group/channel to monitor

Destination Chat ID: Where to send modified addresses

To get chat IDs:

Add @RawDataBot to your groups/channels

The bot will send a message with the chat ID

Chat IDs look like -1001234567890 (for groups/channels)

Important: Make sure to add your bot to both groups/channels as an admin with permission to:

Read messages (in source chat)

Send messages (in destination chat)

3. Deploy to Railway.app

Option A: Using GitHub (Recommended)

Upload to GitHub:

Create a new repository on GitHub

Upload all files from this project:

bot.py

requirements.txt

Procfile

runtime.txt

README.md

.gitignore

Deploy on Railway:

Go to Railway.app

Sign up/Login with GitHub

Click "New Project" → "Deploy from GitHub repo"

Select your repository

Railway will auto-detect it's a Python project

Set Environment Variables:

In Railway project dashboard, go to "Variables" tab

Add these three variables:

BOT_TOKEN=your_bot_token_here SOURCE_CHAT_ID=-1001234567890 DESTINATION_CHAT_ID=-1009876543210 

Replace with your actual values

Deploy:

Railway will automatically deploy

Check logs to ensure bot is running

Option B: Using Railway CLI

Install Railway CLI:

npm install -g @railway/cli

Login and link project:

railway login railway init

Set environment variables:

railway variables set BOT_TOKEN=your_token railway variables set SOURCE_CHAT_ID=-1001234567890 railway variables set DESTINATION_CHAT_ID=-1009876543210

Deploy:

railway up

Environment Variables

VariableDescriptionExampleBOT_TOKENYour Telegram bot token from BotFather1234567890:ABCdefGHI...SOURCE_CHAT_IDChat ID of the group to monitor-1001234567890DESTINATION_CHAT_IDChat ID where to send modified addresses-1009876543210

Testing the Bot

Send a message with a Solana address in the source group:

Check out this token: 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 

The bot should detect it and send to destination:

/nar7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 

Troubleshooting

Bot not detecting addresses

Ensure the address is valid Solana format (32-44 base58 characters)

Check bot has admin rights in source group

Verify SOURCE_CHAT_ID is correct

Bot not sending messages

Verify bot is admin in destination chat

Check DESTINATION_CHAT_ID is correct

Review Railway logs for errors

Bot not running on Railway

Check Railway logs for errors

Verify all environment variables are set

Ensure Procfile is present in repository

Mobile GitHub Upload Guide

Using GitHub Mobile App:

Install GitHub app from App Store/Play Store

Login to your account

Tap "+" → "New repository"

Name it (e.g., solana-telegram-bot)

Create repository

In repository, tap "+" → "Upload files"

Select all bot files from your device

Commit changes

Using GitHub Web (Mobile Browser):

Go to github.com on mobile browser

Sign in and create new repository

Desktop mode might be needed for uploading

Upload files one by one or zip them first

Alternative: Use Git on Phone

Apps like:

Termux (Android) - Full git support

Working Copy (iOS) - Git client

Project Structure

solana-telegram-bot/ ├── bot.py # Main bot logic ├── requirements.txt # Python dependencies ├── Procfile # Railway deployment config ├── runtime.txt # Python version ├── .gitignore # Git ignore rules └── README.md # This file 

How the Bot Detects Solana Addresses

The bot uses regex pattern: \b[1-9A-HJ-NP-Za-km-z]{32,44}\b

This matches:

Base58 characters only (excludes 0, O, I, l)

Length between 32-44 characters

Word boundaries to avoid partial matches

Example Solana Addresses

Valid addresses the bot will detect:

7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU

EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v (USDC)

So11111111111111111111111111111111111111112 (Wrapped SOL)

Logging

The bot logs important events:

When addresses are detected

When messages are sent successfully

Any errors that occur

Check Railway logs to monitor bot activity.

Support

If you encounter issues:

Check Railway logs

Verify environment variables

Ensure bot has proper permissions

Review Telegram Bot API limits

License

MIT License - feel free to modify and use as needed.

Credits

Built with:

python-telegram-bot - Telegram Bot API wrapper

Railway.app - Deployment platform

Note: This bot processes all messages in the source chat. Ensure you have permission to monitor messages and comply with Telegram's Terms of Service.
