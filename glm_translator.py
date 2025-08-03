import openai
import asyncio
import logging
from typing import Optional, Tuple
from langdetect import detect, DetectorFactory
from config import BotConfig

# Đặt seed cho langdetect để có kết quả ổn định (Set seed for langdetect for consistent results)
DetectorFactory.seed = 0

class GLMTranslator:
    """Lớp xử lý dịch thuật sử dụng GLM AI API (Translation handler using GLM AI API)"""
    
    def __init__(self):
        """Khởi tạo translator với cấu hình GLM AI (Initialize translator with GLM AI configuration)"""
        self.client = openai.OpenAI(
            api_key=BotConfig.GLM_API_KEY,
            base_url=BotConfig.GLM_API_URL
        )
        self.model = BotConfig.GLM_MODEL
        self.logger = logging.getLogger(__name__)
    
    def detect_language(self, text: str) -> str:
        """Phát hiện ngôn ngữ của văn bản (Detect language of text)"""
        try:
            # Loại bỏ khoảng trắng và kiểm tra độ dài (Remove whitespace and check length)
            text = text.strip()
            if len(text) < 3:
                return 'unknown'
            
            detected_lang = detect(text)
            self.logger.info(f"Phát hiện ngôn ngữ (Detected language): {detected_lang} cho văn bản (for text): {text[:50]}...")
            return detected_lang
        except Exception as e:
            self.logger.error(f"Lỗi phát hiện ngôn ngữ (Language detection error): {e}")
            return 'unknown'
    
    async def translate_text(self, text: str, target_language: str) -> Optional[str]:
        """Dịch văn bản sang ngôn ngữ đích sử dụng GLM AI (Translate text to target language using GLM AI)"""
        try:
            # Kiểm tra độ dài văn bản (Check text length)
            if len(text) > BotConfig.TRANSLATION_SETTINGS['max_text_length']:
                return None
            
            # Tạo prompt dịch thuật (Create translation prompt)
            language_names = {
                'vi': 'tiếng Việt (Vietnamese)',
                'zh': 'tiếng Trung (Chinese)',
                'en': 'tiếng Anh (English)'
            }
            
            target_lang_name = language_names.get(target_language, target_language)
            
            # Tạo prompt dịch thuật với phong cách cụ thể (Create translation prompt with specific style)
            style_instructions = {
                'vi': "Dịch sang tiếng Việt với giọng điệu Sài Gòn, phong cách tự nhiên, giản dị, dễ hiểu. Sử dụng từ ngữ thân thiện, gần gũi như cách nói chuyện hàng ngày của người Sài Gòn.",
                'zh': "翻译成中文，使用北京话语调，风格自然朴实，通俗易懂。用词亲切自然，如同北京人日常交流的方式。",
                'en': "Translate to English in a natural, simple, and easy-to-understand style."
            }
            
            style_instruction = style_instructions.get(target_language, "Translate naturally and simply.")
            
            prompt = f"""{style_instruction}

Văn bản cần dịch: {text}

Bản dịch:"""
            
            # Gọi API GLM (Call GLM API)
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Bạn là một chuyên gia dịch thuật chuyên nghiệp với khả năng dịch theo phong cách địa phương cụ thể. Khi dịch sang tiếng Việt, hãy sử dụng giọng điệu Sài Gòn tự nhiên, giản dị. Khi dịch sang tiếng Trung, hãy sử dụng giọng điệu Bắc Kinh tự nhiên, dễ hiểu. Giữ nguyên ý nghĩa và ngữ cảnh của văn bản gốc. QUAN TRỌNG: Chỉ trả về bản dịch thuần túy, KHÔNG sử dụng thẻ XML, không giải thích, không thêm ghi chú."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            # Loại bỏ các thẻ XML không mong muốn (Remove unwanted XML tags)
            import re
            # Loại bỏ thẻ <think>...</think> và nội dung bên trong
            translated_text = re.sub(r'<think>.*?</think>', '', translated_text, flags=re.DOTALL)
            # Loại bỏ các thẻ XML khác
            translated_text = re.sub(r'<[^>]+>', '', translated_text)
            # Làm sạch khoảng trắng thừa
            translated_text = translated_text.strip()
            
            self.logger.info(f"Dịch thành công (Translation successful): {text[:30]}... -> {translated_text[:30]}...")
            return translated_text
            
        except Exception as e:
            self.logger.error(f"Lỗi dịch thuật (Translation error): {e}")
            return None
    
    async def translate_with_retry(self, text: str, target_language: str) -> Optional[str]:
        """Dịch văn bản với cơ chế thử lại (Translate text with retry mechanism)"""
        max_retries = BotConfig.TRANSLATION_SETTINGS['retry_attempts']
        retry_delay = BotConfig.TRANSLATION_SETTINGS['retry_delay']
        
        for attempt in range(max_retries):
            try:
                result = await self.translate_text(text, target_language)
                if result:
                    return result
                
                if attempt < max_retries - 1:
                    self.logger.warning(f"Thử lại lần {attempt + 1} sau {retry_delay}s (Retry attempt {attempt + 1} after {retry_delay}s)")
                    await asyncio.sleep(retry_delay)
                    
            except Exception as e:
                self.logger.error(f"Lỗi trong lần thử {attempt + 1} (Error in attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay)
        
        return None
    
    def should_translate(self, detected_lang: str, target_lang: str) -> bool:
        """Kiểm tra xem có nên dịch hay không (Check if translation is needed)"""
        # Không dịch nếu ngôn ngữ giống nhau (Don't translate if same language)
        if detected_lang == target_lang:
            return False
        
        # Không dịch nếu không phát hiện được ngôn ngữ (Don't translate if language not detected)
        if detected_lang == 'unknown':
            return False
        
        # Xử lý các biến thể ngôn ngữ Trung Quốc (Handle Chinese language variants)
        chinese_variants = ['zh', 'zh-cn', 'zh-tw', 'zh-hans', 'zh-hant']
        if detected_lang in chinese_variants and target_lang == 'zh':
            return False
        
        return True
    
    async def get_translation_info(self, text: str) -> Tuple[str, bool, bool]:
        """Lấy thông tin về việc dịch thuật (Get translation information)"""
        detected_lang = self.detect_language(text)
        
        # Kiểm tra xem có nên dịch sang tiếng Việt và tiếng Trung (Check if should translate to Vietnamese and Chinese)
        should_translate_to_vi = self.should_translate(detected_lang, 'vi')
        should_translate_to_zh = self.should_translate(detected_lang, 'zh')
        
        return detected_lang, should_translate_to_vi, should_translate_to_zh