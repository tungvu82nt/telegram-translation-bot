#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cấu hình cho Telegram Bot Phiên Dịch (Configuration for Telegram Translation Bot)
"""

import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env (Load environment variables from .env file)
load_dotenv()

class BotConfig:
    """Lớp cấu hình bot (Bot configuration class)"""
    
    # Token bot Telegram (Telegram bot token)
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # GLM AI Configuration (Cấu hình GLM AI)
    GLM_API_KEY = os.getenv('GLM_API_KEY')
    GLM_API_URL = os.getenv('GLM_API_URL', 'https://open.bigmodel.cn/api/paas/v4/')
    GLM_MODEL = os.getenv('GLM_MODEL', 'GLM-4.5-AirX')
    
    # Cấu hình ngôn ngữ hỗ trợ (Supported languages configuration)
    SUPPORTED_LANGUAGES = {
        'vi': {
            'name': 'Tiếng Việt',
            'flag': '🇻🇳',
            'code': 'vi'
        },
        'zh': {
            'name': '中文',
            'flag': '🇨🇳', 
            'code': 'zh'
        },
        'zh-cn': {
            'name': '中文',
            'flag': '🇨🇳',
            'code': 'zh'
        }
    }
    
    # Cấu hình dịch thuật (Translation configuration)
    TRANSLATION_SETTINGS = {
        'max_text_length': 4000,  # Độ dài tối đa của văn bản dịch
        'timeout': 10,  # Thời gian chờ tối đa (giây)
        'retry_attempts': 3,  # Số lần thử lại khi lỗi
        'retry_delay': 1  # Thời gian chờ giữa các lần thử (giây)
    }
    
    # Cấu hình logging (Logging configuration)
    LOGGING_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'bot.log',
        'max_file_size': 10 * 1024 * 1024,  # 10MB
        'backup_count': 5
    }
    
    # Tin nhắn hệ thống (System messages)
    MESSAGES = {
        'vi': {
            'bot_started': '🤖 Bot phiên dịch đã sẵn sàng!',
            'translation_error': '❌ Lỗi dịch thuật, vui lòng thử lại.',
            'translation_failed': '❌ Dịch thuật thất bại, vui lòng thử lại.',
            'text_too_long': '📝 Văn bản quá dài để dịch.',
            'general_error': '❌ Đã xảy ra lỗi, vui lòng thử lại.',
            'unsupported_content': '🚫 Không hỗ trợ dịch loại nội dung này.'
        },
        'zh': {
            'bot_started': '🤖 翻译机器人已准备就绪！',
            'translation_error': '❌ 翻译错误，请重试。',
            'translation_failed': '❌ 翻译失败，请重试。',
            'text_too_long': '📝 文本过长无法翻译。',
            'general_error': '❌ 发生错误，请重试。',
            'unsupported_content': '🚫 不支持翻译此类内容。'
        },
        'en': {
            'bot_started': '🤖 Translation bot is ready!',
            'translation_error': '❌ Translation error, please try again.',
            'translation_failed': '❌ Translation failed, please try again.',
            'text_too_long': '📝 Text is too long to translate.',
            'general_error': '❌ An error occurred, please try again.',
            'unsupported_content': '🚫 This content type is not supported for translation.'
        }
    }
    
    # Cấu hình bot (Bot settings)
    BOT_SETTINGS = {
        'parse_mode': 'HTML',  # Chế độ phân tích tin nhắn
        'disable_web_page_preview': True,  # Tắt xem trước trang web
        'allow_sending_without_reply': True,  # Cho phép gửi không cần reply
        'protect_content': False  # Bảo vệ nội dung
    }
    
    @staticmethod
    def validate_config():
        """Kiểm tra tính hợp lệ của cấu hình (Validate configuration)"""
        if not BotConfig.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN không được tìm thấy trong file .env (TELEGRAM_BOT_TOKEN not found in .env file)")
        
        if not BotConfig.GLM_API_KEY:
            raise ValueError("GLM_API_KEY không được tìm thấy trong file .env (GLM_API_KEY not found in .env file)")
        
        if not BotConfig.GLM_API_URL:
            raise ValueError("GLM_API_URL không được tìm thấy trong file .env (GLM_API_URL not found in .env file)")
        
        # Kiểm tra các ngôn ngữ hỗ trợ (Check supported languages)
        if not BotConfig.SUPPORTED_LANGUAGES:
            raise ValueError("Không có ngôn ngữ nào được cấu hình (No languages configured)")
        
        print("✅ Cấu hình hợp lệ (Configuration is valid)")
    
    @classmethod
    def get_language_info(cls, lang_code):
        """Lấy thông tin ngôn ngữ (Get language information)"""
        return cls.SUPPORTED_LANGUAGES.get(lang_code, {
            'name': 'Unknown',
            'flag': '🏳️',
            'code': lang_code
        })
    
    @classmethod
    def get_message(cls, key, lang='vi'):
        """Lấy tin nhắn hệ thống theo ngôn ngữ (Get system message by language)"""
        return cls.MESSAGES.get(lang, cls.MESSAGES['vi']).get(key, key)
    
    @classmethod
    def get_system_message(cls, key, lang='vi'):
        """Lấy tin nhắn hệ thống theo ngôn ngữ (Get system message by language)"""
        return cls.MESSAGES.get(lang, cls.MESSAGES['vi']).get(key, key)

# Kiểm tra cấu hình khi import module (Validate configuration when importing module)
if __name__ == '__main__':
    config_errors = BotConfig.validate_config()
    if config_errors:
        print("❌ Lỗi cấu hình:")
        for error in config_errors:
            print(f"  - {error}")
    else:
        print("✅ Cấu hình hợp lệ!")