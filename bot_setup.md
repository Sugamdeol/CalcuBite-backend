# CalcuBite Telegram Bot Setup

## Quick Start

1. **Get Bot Token from @BotFather:**
   - Message @BotFather on Telegram
   - Create new bot: `/newbot`
   - Name it: `CalcuBiteBot` (or your choice)
   - Copy the token

2. **Set Environment Variable:**
   ```bash
   export CALCUBITE_BOT_TOKEN="your_bot_token_here"
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r bot_requirements.txt
   ```

4. **Run Bot:**
   ```bash
   python3 bot.py
   ```

## Features

- 📸 Photo analysis (AI-powered)
- 📝 Text-based nutrition estimates
- 📊 Calorie & macro tracking
- 🎯 Health scores
- 💡 Nutrition tips

## Deploy to Render (Free)

1. Create `render.yaml`:
   ```yaml
   services:
     - type: worker
       name: calcubite-bot
       runtime: python
       buildCommand: pip install -r bot_requirements.txt
       startCommand: python bot.py
       envVars:
         - key: CALCUBITE_BOT_TOKEN
           sync: false
   ```

2. Push to GitHub and deploy via Render dashboard

3. Set `CALCUBITE_BOT_TOKEN` in Render environment variables

## Commands

- `/start` - Welcome message
- `/help` - Usage guide
- `/about` - About CalcuBite

## Data Sources

Nutrition data based on standard Indian food database:
- Roti, Rice, Dal, Paneer, Chicken, Eggs, etc.
- Portion sizes: Standard household measures
- Values: Approximate estimates

## Privacy

- Photos processed in real-time
- No permanent storage
- No user data retained
