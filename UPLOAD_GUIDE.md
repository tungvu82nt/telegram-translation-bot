# 📤 Hướng Dẫn Upload Lên GitHub (Thủ Công)

## 🚨 Vì Git Command Line Không Hoạt Động

Do git.exe không hoạt động trên hệ thống Windows của bạn, chúng ta sẽ upload thủ công qua GitHub web interface.

## 📋 Bước 1: Chuẩn Bị Files

### Files CẦN upload:
✅ `main.py` - Bot chính
✅ `config.py` - Cấu hình
✅ `glm_translator.py` - GLM translator
✅ `requirements.txt` - Dependencies
✅ `Procfile` - Heroku config
✅ `runtime.txt` - Python version
✅ `railway.toml` - Railway config
✅ `render.yaml` - Render config
✅ `vercel.json` - Vercel config
✅ `.env.example` - Mẫu environment
✅ `.gitignore` - Git ignore
✅ `README.md` - Hướng dẫn chính
✅ `README_DEPLOYMENT.md` - Hướng dẫn deploy
✅ `QUICK_DEPLOY.md` - Deploy nhanh
✅ `WEBHOOK_READY.md` - Checklist

### Files KHÔNG upload:
❌ `.env` - Chứa thông tin nhạy cảm
❌ `__pycache__/` - Cache Python
❌ `bot.log` - Log files
❌ `test_bot.py` - File test
❌ `run.bat` - Script local

## 🌐 Bước 2: Upload Lên GitHub

### 2.1 Tạo Repository
1. Truy cập: https://github.com
2. Đăng nhập tài khoản GitHub
3. Nhấn nút **"New"** (màu xanh) hoặc **"+"** → **"New repository"**
4. Điền thông tin:
   - **Repository name**: `telegram-translation-bot`
   - **Description**: `Bot Telegram phiên dịch đa ngôn ngữ với webhook support`
   - Chọn **Public** (hoặc Private nếu muốn)
   - ✅ Tick **"Add a README file"**
   - Chọn **"Python"** trong .gitignore template
5. Nhấn **"Create repository"**

### 2.2 Upload Files
1. Trong repository vừa tạo, nhấn **"uploading an existing file"** hoặc **"Upload files"**
2. **Cách 1 - Kéo thả:**
   - Mở Windows Explorer: `d:\A1\Tool\telegram-bot\telegram-bot`
   - Chọn tất cả files CẦN upload (theo danh sách trên)
   - Kéo thả vào vùng "Drag files here"

3. **Cách 2 - Choose files:**
   - Nhấn **"choose your files"**
   - Navigate đến: `d:\A1\Tool\telegram-bot\telegram-bot`
   - Chọn từng file cần thiết (Ctrl+Click để chọn nhiều)

### 2.3 Commit Changes
1. Scroll xuống phần **"Commit changes"**
2. **Commit message**: `Bot ready for webhook deployment`
3. **Description** (tùy chọn): `Added all necessary files for deployment to Railway, Render, Heroku, and Vercel`
4. Chọn **"Commit directly to the main branch"**
5. Nhấn **"Commit changes"**

## 🚀 Bước 3: Deploy Lên Platform

### 3.1 Railway (Khuyến nghị - Dễ nhất)
1. Truy cập: https://railway.app
2. Đăng nhập bằng GitHub
3. **"New Project"** → **"Deploy from GitHub repo"**
4. Chọn repository `telegram-translation-bot`
5. Railway tự động detect `railway.toml` và build
6. Thêm Environment Variables:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   OPENAI_API_KEY=your_openai_key_here
   DEFAULT_TRANSLATOR=openai
   ```
7. Deploy tự động!

### 3.2 Render (Alternative)
1. Truy cập: https://render.com
2. Đăng nhập bằng GitHub
3. **"New"** → **"Web Service"**
4. Connect GitHub repository
5. Render tự động đọc `render.yaml`
6. Thêm Environment Variables tương tự
7. Deploy!

## ✅ Kiểm Tra Sau Deploy

1. **Xem Logs**: Kiểm tra deployment logs
2. **Test Health**: Truy cập `https://your-domain.com/health`
3. **Test Bot**: Gửi tin nhắn cho bot
4. **Monitor**: Theo dõi logs để debug

## 🎯 Lưu Ý Quan Trọng

- Bot sẽ **tự động chuyển** từ polling (local) sang webhook (production)
- **Không upload file .env** - chứa thông tin nhạy cảm
- **Environment variables** phải được thêm trong dashboard của platform
- **Domain HTTPS** sẽ được cấp tự động cho webhook

## 🆘 Troubleshooting

### Upload thất bại?
- Kiểm tra kích thước files (GitHub giới hạn 100MB/file)
- Đảm bảo không upload files nhạy cảm
- Thử upload từng file một nếu cần

### Deploy thất bại?
- Kiểm tra logs trong platform dashboard
- Verify environment variables
- Đảm bảo `requirements.txt` đúng format

---

**🎉 Sau khi hoàn thành, bot sẽ chạy 24/7 trên cloud với webhook!**