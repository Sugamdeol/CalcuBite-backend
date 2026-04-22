#!/usr/bin/env python3
"""
CalcuBite Telegram Bot - Webhook Version for Render
AI-powered food analysis via Telegram
"""

import os
import logging
import base64
from io import BytesIO
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio

# Flask app for webhook
app = Flask(__name__)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
TOKEN = os.getenv('CALCUBITE_BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # e.g., https://calcubite-bot.onrender.com
PORT = int(os.getenv('PORT', 10000))

# Initialize bot and application
bot = Bot(token=TOKEN) if TOKEN else None
application = None

# Nutrition database
nutrition_db = {
    'roti': {'cal': 70, 'protein': 3, 'carbs': 15, 'fat': 0.5, 'portion': '1 piece'},
    'rice': {'cal': 130, 'protein': 3, 'carbs': 28, 'fat': 0.3, 'portion': '1 cup cooked'},
    'dal': {'cal': 150, 'protein': 9, 'carbs': 20, 'fat': 5, 'portion': '1 cup'},
    'paneer': {'cal': 265, 'protein': 18, 'carbs': 6, 'fat': 20, 'portion': '100g'},
    'chicken': {'cal': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'portion': '100g'},
    'egg': {'cal': 70, 'protein': 6, 'carbs': 0.6, 'fat': 5, 'portion': '1 large'},
    'banana': {'cal': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3, 'portion': '1 medium'},
    'milk': {'cal': 42, 'protein': 3.4, 'carbs': 5, 'fat': 1, 'portion': '100ml'},
    'oats': {'cal': 389, 'protein': 16.9, 'carbs': 66, 'fat': 6.9, 'portion': '100g dry'},
    'chapati': {'cal': 70, 'protein': 3, 'carbs': 15, 'fat': 0.5, 'portion': '1 piece'},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message."""
    welcome_text = """🍽️ *Welcome to CalcuBite!*

I'm your AI nutrition assistant. Send me a photo of your food and I'll analyze:
• Calories
• Protein, Carbs, Fats
• Portion size
• Health score

*Commands:*
/start - Show this message
/help - How to use
/about - About CalcuBite

Send a food photo to get started! 📸"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message."""
    help_text = """*How to use CalcuBite:*

1️⃣ Take a clear photo of your food
2️⃣ Send it to me here
3️⃣ I'll analyze and send nutrition data

*Tips for best results:*
• Good lighting
• Clear view of all items
• Include portion reference (hand, plate)

*Privacy:* Photos are processed securely and not stored."""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send about message."""
    about_text = """*About CalcuBite* 🤖

AI-powered food analysis for smarter nutrition choices.

Built by: Sugam Deol
Version: 1.0.0

For support, contact via Instagram @bytebuildrz"""
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def analyze_food_image(photo_bytes: bytes) -> str:
    """Analyze food image using AI."""
    try:
        return """🍽️ *Food Analysis*

*Items Detected:*
Analyzing your food photo...

*Note:* Full AI vision integration in progress. 
For now, please describe what you see in the photo and I'll provide detailed nutrition info!

Example: "Rice, dal, and 2 rotis\""""
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return "❌ Sorry, I couldn't analyze that image. Please try again."

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle food photos."""
    analyzing_msg = await update.message.reply_text("🔍 Analyzing your food photo...", parse_mode='Markdown')
    
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        analysis = await analyze_food_image(bytes(photo_bytes))
        await analyzing_msg.edit_text(analysis, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Photo handling error: {e}")
        await analyzing_msg.edit_text("❌ Error analyzing photo. Please try again.", parse_mode='Markdown')

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    text = update.message.text
    text_lower = text.lower()
    
    found_items = []
    total_cal = total_protein = total_carbs = total_fat = 0
    
    for food, data in nutrition_db.items():
        if food in text_lower:
            found_items.append(f"• {food.title()}: {data['cal']} cal ({data['portion']})")
            total_cal += data['cal']
            total_protein += data['protein']
            total_carbs += data['carbs']
            total_fat += data['fat']
    
    if found_items:
        response = f"""🍽️ *Nutrition Estimate*

*Items Found:*
{chr(10).join(found_items)}

*Total Estimated:*
• Calories: ~{total_cal} kcal
• Protein: ~{total_protein}g
• Carbs: ~{total_carbs}g
• Fat: ~{total_fat}g

*Note:* These are estimates. Portion sizes vary!

For accurate analysis, send a photo 📸"""
        await update.message.reply_text(response, parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "I can analyze food photos or estimate nutrition from descriptions!\n\n"
            "Try describing your meal (e.g., '2 roti, 1 cup rice, dal') or send a photo.",
            parse_mode='Markdown'
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

def setup_application():
    """Setup telegram application."""
    global application
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_error_handler(error_handler)
    
    return application

@app.route('/')
def home():
    """Home endpoint."""
    return jsonify({
        'status': 'CalcuBite Bot is running',
        'version': '1.0.0',
        'webhook': f'{WEBHOOK_URL}/webhook' if WEBHOOK_URL else 'Not configured'
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook from Telegram."""
    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), bot)
        
        # Process update
        async def process():
            await application.initialize()
            await application.process_update(update)
        
        asyncio.run(process())
        return 'OK', 200
    return 'Method not allowed', 405

@app.route('/set-webhook', methods=['GET'])
def set_webhook():
    """Set webhook with Telegram."""
    if not WEBHOOK_URL:
        return jsonify({'error': 'WEBHOOK_URL not set'}), 400
    
    webhook_url = f"{WEBHOOK_URL}/webhook"
    success = asyncio.run(bot.set_webhook(webhook_url))
    
    if success:
        return jsonify({'message': f'Webhook set to {webhook_url}'})
    return jsonify({'error': 'Failed to set webhook'}), 500

if __name__ == '__main__':
    if not TOKEN:
        logger.error("CALCUBITE_BOT_TOKEN not set!")
        exit(1)
    
    # Setup application
    setup_application()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=PORT)
