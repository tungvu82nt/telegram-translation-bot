#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bot Phiên Dịch Tự Động (Automatic Translation Bot)
Bot tự động phiên dịch tin nhắn giữa tiếng Trung và tiếng Việt
"""

import os
import logging
import asyncio
import time
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from flask import Flask, request
import threading
from config import BotConfig
from glm_translator import GLMTranslator

# Cấu hình logging (Configure logging)
logging.basicConfig(
    level=getattr(logging, BotConfig.LOGGING_CONFIG['level']),
    format=BotConfig.LOGGING_CONFIG['format'],
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(BotConfig.LOGGING_CONFIG['file'], encoding='utf-8')
    ]
)

# Tạo logger (Create logger)
logger = logging.getLogger(__name__)

class TranslationBot:
    """Lớp chính cho bot phiên dịch (Main class for translation bot)"""
    
    def __init__(self):
        """Khởi tạo bot với translator (Initialize bot with translator)"""
        # Kiểm tra cấu hình (Validate configuration)
        config_errors = BotConfig.validate_config()
        if config_errors:
            for error in config_errors:
                logger.error(error)
            raise ValueError("Cấu hình không hợp lệ")
        
        self.translator = GLMTranslator()
        self.token = BotConfig.TELEGRAM_BOT_TOKEN
        self.config = BotConfig()
        self.logger = logger  # Thêm logger instance
    

    
    async def translate_text(self, text: str, target_lang: str) -> str:
        """Dịch văn bản sang ngôn ngữ đích (Translate text to target language)"""
        # Kiểm tra độ dài văn bản (Check text length)
        if len(text) > BotConfig.TRANSLATION_SETTINGS['max_text_length']:
            return BotConfig.get_system_message('text_too_long', 'vi')
        
        # Sử dụng GLMTranslator với cơ chế retry (Use GLMTranslator with retry mechanism)
        result = await self.translator.translate_with_retry(text, target_lang)
        
        if result:
            return result
        else:
            # Trả về thông báo lỗi nếu dịch thất bại (Return error message if translation failed)
            return BotConfig.get_system_message('translation_failed', 'vi')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Xử lý tin nhắn đến và dịch thuật (Handle incoming messages and translate)"""
        try:
            if not update.message or not update.message.text:
                return
            
            message_text = update.message.text.strip()
            
            # Bỏ qua tin nhắn trống hoặc lệnh bot (Skip empty messages or bot commands)
            if not message_text or message_text.startswith('/'):
                return
            
            user_info = f"{update.effective_user.first_name} ({update.effective_user.id})"
            self.logger.info(f"Nhận tin nhắn từ {user_info} (Received message from): {message_text}")
            
            # Phân tích ngôn ngữ (Analyze language)
            detected_lang = self.translator.detect_language(message_text)
            lang_info = BotConfig.get_language_info(detected_lang)
            
            self.logger.info(f"Ngôn ngữ phát hiện (Detected language): {detected_lang} - {lang_info['name']}")
            
            # Luôn dịch song song sang cả tiếng Trung và tiếng Việt (Always translate to both Chinese and Vietnamese in parallel)
            translation_tasks = [
                self.translate_text(message_text, 'zh'),
                self.translate_text(message_text, 'vi')
            ]
            
            # Thực hiện dịch song song để tăng tốc độ (Execute parallel translation for speed)
            chinese_translation, vietnamese_translation = await asyncio.gather(*translation_tasks)
            
            translations = []
            
            # Thêm bản dịch tiếng Trung (Add Chinese translation)
            if chinese_translation and chinese_translation != BotConfig.get_system_message('translation_failed', 'vi'):
                translations.append(f"🇨🇳 **中文**: {chinese_translation}")
            
            # Thêm bản dịch tiếng Việt (Add Vietnamese translation)
            if vietnamese_translation and vietnamese_translation != BotConfig.get_system_message('translation_failed', 'vi'):
                translations.append(f"🇻🇳 **Tiếng Việt**: {vietnamese_translation}")
            
            # Gửi bản dịch (Send translations)
            if translations:
                response_text = "\n\n".join(translations)
                await update.message.reply_text(
                    response_text,
                    parse_mode=BotConfig.BOT_SETTINGS['parse_mode'],
                    disable_web_page_preview=BotConfig.BOT_SETTINGS['disable_web_page_preview']
                )
                self.logger.info(f"Đã gửi bản dịch (Sent translation): {len(translations)} ngôn ngữ (languages)")
            else:
                self.logger.info("Lỗi dịch thuật (Translation error)")
                
        except Exception as e:
            self.logger.error(f"Lỗi xử lý tin nhắn (Message handling error): {e}")
            await update.message.reply_text(BotConfig.get_system_message('general_error', 'vi'))
    
    async def handle_start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Xử lý lệnh /start (Handle /start command)"""
        welcome_message = (
            "🤖 **Chào mừng đến với Bot Phiên Dịch Tự Động!**\n\n"
            "🔄 Bot sẽ tự động dịch tin nhắn của bạn sang:\n"
            "🇨🇳 Tiếng Trung (Chinese)\n"
            "🇻🇳 Tiếng Việt (Vietnamese)\n\n"
            "📝 Chỉ cần gửi tin nhắn văn bản, bot sẽ tự động phiên dịch!\n\n"
            "💡 Lệnh hỗ trợ:\n"
            "/start - Khởi động bot\n"
            "/help - Hướng dẫn sử dụng"
        )
        
        try:
            await update.message.reply_text(
                welcome_message,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Lỗi gửi tin nhắn chào mừng: {e}")
    
    async def handle_help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Xử lý lệnh /help (Handle /help command)"""
        help_message = (
            "📖 **Hướng dẫn sử dụng Bot Phiên Dịch**\n\n"
            "🔍 **Cách hoạt động:**\n"
            "• Bot tự động phát hiện ngôn ngữ của tin nhắn\n"
            "• Dịch sang tiếng Trung nếu không phải tiếng Trung\n"
            "• Dịch sang tiếng Việt nếu không phải tiếng Việt\n\n"
            "✅ **Ngôn ngữ hỗ trợ:**\n"
            "🇻🇳 Tiếng Việt\n"
            "🇨🇳 Tiếng Trung\n"
            "🇺🇸 Tiếng Anh\n"
            "🌍 Và nhiều ngôn ngữ khác...\n\n"
            "⚠️ **Lưu ý:**\n"
            "• Chỉ dịch tin nhắn văn bản\n"
            "• Không dịch lệnh bot (bắt đầu bằng /)\n"
            "• Cần kết nối internet để hoạt động"
        )
        
        try:
            await update.message.reply_text(
                help_message,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Lỗi gửi tin nhắn hướng dẫn: {e}")
    
    def run(self):
        """Chạy bot (Run the bot)"""
        # Tạo ứng dụng bot (Create bot application)
        application = Application.builder().token(self.token).build()
        
        # Thêm handler cho lệnh (Add command handlers)
        application.add_handler(CommandHandler("start", self.handle_start_command))
        application.add_handler(CommandHandler("help", self.handle_help_command))
        
        # Thêm handler cho tin nhắn văn bản (Add handler for text messages)
        message_handler = MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self.handle_message
        )
        application.add_handler(message_handler)
        
        # Kiểm tra môi trường để quyết định sử dụng webhook hay polling
        webhook_url = os.getenv('WEBHOOK_URL')
        port = int(os.getenv('PORT', 8000))
        
        logger.info("🤖 Bot phiên dịch đang khởi động...")
        logger.info(f"📋 Token: {self.token[:10]}...")
        
        if webhook_url or os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('RENDER') or os.getenv('VERCEL'):
            # Chế độ webhook cho production
            logger.info("🌐 Chạy ở chế độ webhook (production)")
            self.run_webhook(application, webhook_url, port)
        else:
            # Chế độ polling cho development
            logger.info("🔄 Chạy ở chế độ polling (development)")
            application.run_polling(drop_pending_updates=True)
    
    def run_webhook(self, application, webhook_url, port):
        """Chạy bot với webhook mode (Run bot with webhook mode)"""
        app = Flask(__name__)
        
        @app.route('/webhook', methods=['POST'])
        async def webhook():
            """Xử lý webhook từ Telegram (Handle webhook from Telegram)"""
            try:
                update = Update.de_json(request.get_json(), application.bot)
                await application.process_update(update)
                return 'OK'
            except Exception as e:
                logger.error(f"Lỗi xử lý webhook: {e}")
                return 'Error', 500
        
        @app.route('/health', methods=['GET'])
        def health():
            """Health check endpoint"""
            return 'Bot is running!'
        
        @app.route('/', methods=['GET'])
        def home():
            """Home endpoint"""
            return 'Telegram Translation Bot is running!'
        
        # Set webhook
        if not webhook_url:
            # Tự động detect domain từ môi trường
            if os.getenv('RAILWAY_STATIC_URL'):
                webhook_url = f"https://{os.getenv('RAILWAY_STATIC_URL')}/webhook"
            elif os.getenv('RENDER_EXTERNAL_URL'):
                webhook_url = f"{os.getenv('RENDER_EXTERNAL_URL')}/webhook"
            elif os.getenv('VERCEL_URL'):
                webhook_url = f"https://{os.getenv('VERCEL_URL')}/webhook"
        
        if webhook_url:
            logger.info(f"🔗 Setting webhook: {webhook_url}")
            asyncio.run(application.bot.set_webhook(webhook_url))
        
        # Khởi động Flask app
        logger.info(f"🚀 Starting webhook server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)

def main():
    """Hàm chính để chạy bot (Main function to run the bot)"""
    try:
        bot = TranslationBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot đã được dừng bởi người dùng")
    except Exception as e:
        logger.error(f"Lỗi khởi động bot: {e}")

if __name__ == '__main__':
    main()