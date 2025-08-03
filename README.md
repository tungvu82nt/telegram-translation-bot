# Telegram Bot Phiên Dịch Tự Động (Automatic Translation Bot)

Bot Telegram tự động phiên dịch tin nhắn giữa tiếng Trung và tiếng Việt sử dụng GLM AI trong các nhóm chat.

## Tính năng (Features)

- 🔄 Tự động phát hiện ngôn ngữ của tin nhắn
- 🇨🇳 Dịch sang tiếng Trung (Chinese)
- 🇻🇳 Dịch sang tiếng Việt (Vietnamese)
- 📱 Hoạt động trong nhóm chat
- ⚡ Phản hồi nhanh và chính xác

## Cài đặt (Installation)

### 1. Cài đặt Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình Bot Token

File `.env` đã được tạo với token bot. Đảm bảo token hợp lệ:

```env
TELEGRAM_BOT_TOKEN=8028885261:AAF2J5Rge_fYVHYwljD4eK4WuKCq0dT6sWc
```

### 3. Chạy Bot

```bash
python main.py
```

## Cách sử dụng (Usage)

1. **Thêm bot vào nhóm**: Mời bot vào nhóm Telegram của bạn
2. **Cấp quyền admin**: Đảm bảo bot có quyền đọc tin nhắn
3. **Gửi tin nhắn**: Bot sẽ tự động dịch mọi tin nhắn văn bản

## Ví dụ (Examples)

**Tin nhắn tiếng Việt:**
```
Người dùng: Xin chào, hôm nay thế nào?
Bot: 🇨🇳 中文: 你好，今天怎么样？
```

**Tin nhắn tiếng Trung:**
```
Người dùng: 今天天气很好
Bot: 🇻🇳 Tiếng Việt: Hôm nay thời tiết rất đẹp
```

**Tin nhắn tiếng Anh:**
```
Người dùng: Hello, how are you?
Bot: 🇨🇳 中文: 你好，你好吗？
     🇻🇳 Tiếng Việt: Xin chào, bạn khỏe không?
```

## Cấu trúc dự án (Project Structure)

```
telegram-bot/
├── .env                 # Cấu hình bot token
├── main.py             # File chính của bot
├── requirements.txt    # Danh sách thư viện
└── README.md          # Hướng dẫn sử dụng
```

## Lưu ý (Notes)

- Bot sử dụng GLM AI API cho chất lượng dịch thuật cao
- Không dịch các tin nhắn lệnh (bắt đầu bằng `/`)
- Bot chỉ dịch tin nhắn văn bản, không dịch hình ảnh hoặc file
- Cần kết nối internet để hoạt động

## Khắc phục sự cố (Troubleshooting)

### Bot không phản hồi
- Kiểm tra token bot trong file `.env`
- Đảm bảo bot có quyền đọc tin nhắn trong nhóm
- Kiểm tra kết nối internet

### Lỗi dịch thuật
- Google Translate có thể bị giới hạn tần suất
- Thử lại sau vài phút
- Kiểm tra log để xem lỗi cụ thể

## Liên hệ (Contact)

Nếu có vấn đề hoặc góp ý, vui lòng tạo issue trong repository.