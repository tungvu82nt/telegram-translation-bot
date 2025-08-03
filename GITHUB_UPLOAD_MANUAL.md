# 📤 Hướng Dẫn Upload Thủ Công Lên GitHub

## 🚨 Tình Huống
Do lệnh Git không hoạt động và MCP Hyperbrowser đã hết credit, chúng ta sẽ upload thủ công qua giao diện GitHub web.

## 📋 Danh Sách Files Cần Upload

### ✅ Files CẦN Upload (16 files)
```
1. main.py                 - File chính của bot
2. config.py              - Cấu hình bot
3. glm_translator.py      - Translator GLM
4. requirements.txt       - Dependencies Python
5. runtime.txt           - Phiên bản Python
6. Procfile              - Cấu hình Heroku
7. railway.toml          - Cấu hình Railway
8. render.yaml           - Cấu hình Render
9. vercel.json           - Cấu hình Vercel
10. .gitignore           - Git ignore rules
11. .env.example         - Template environment
12. README.md            - Tài liệu chính
13. README_DEPLOYMENT.md - Hướng dẫn deploy
14. QUICK_DEPLOY.md      - Deploy nhanh
15. WEBHOOK_READY.md     - Webhook info
16. UPLOAD_GUIDE.md      - Hướng dẫn upload
```

### ❌ Files KHÔNG Upload
```
- .env                   - Chứa thông tin bảo mật
- __pycache__/          - Thư mục cache Python
- bot.log               - File log
- run.bat               - File Windows specific
- test_bot.py           - File test
```

## 🚀 Các Bước Upload

### Bước 1: Truy Cập GitHub
1. Mở trình duyệt và truy cập: https://github.com
2. Đăng nhập vào tài khoản GitHub của bạn

### Bước 2: Tạo Repository Mới
1. Click nút **"New"** (màu xanh) hoặc dấu **"+"** ở góc phải
2. Chọn **"New repository"**
3. Điền thông tin:
   - **Repository name**: `telegram-translation-bot`
   - **Description**: `Telegram bot for translation with multiple AI providers`
   - **Visibility**: Chọn **Public** (hoặc Private nếu muốn)
   - **KHÔNG** tick "Add a README file" (vì đã có sẵn)
   - **KHÔNG** tick "Add .gitignore" (vì đã có sẵn)
   - **KHÔNG** tick "Choose a license"
4. Click **"Create repository"**

### Bước 3: Upload Files

#### Phương Pháp 1: Drag & Drop (Khuyến nghị)
1. Sau khi tạo repo, bạn sẽ thấy trang trống
2. Mở File Explorer và navigate đến: `d:\A1\Tool\telegram-bot\telegram-bot`
3. Chọn tất cả 16 files cần upload (theo danh sách ở trên)
4. Kéo và thả (drag & drop) vào trang GitHub
5. GitHub sẽ tự động upload và hiển thị danh sách files

#### Phương Pháp 2: Choose Files
1. Click **"uploading an existing file"** trên trang repo
2. Click **"choose your files"**
3. Chọn tất cả 16 files cần upload
4. Click **"Open"**

### Bước 4: Commit Changes
1. Scroll xuống phần **"Commit changes"**
2. **Commit message**: `Initial commit - Telegram translation bot ready for deployment`
3. **Description** (optional): `Bot supports multiple AI providers (OpenAI, GLM) with webhook deployment configs for Railway, Render, Vercel, and Heroku`
4. Chọn **"Commit directly to the main branch"**
5. Click **"Commit changes"**

## 🎯 Sau Khi Upload Thành Công

### 1. Kiểm Tra Repository
- Đảm bảo tất cả 16 files đã được upload
- Check README.md hiển thị đúng
- Verify các file config (.toml, .yaml, .json) có mặt

### 2. Copy Repository URL
- URL sẽ có dạng: `https://github.com/[username]/telegram-translation-bot`
- Copy URL này để sử dụng cho deployment

## 🚀 Deploy Lên Platform

### Railway (Khuyến nghị)
1. Truy cập: https://railway.app
2. Đăng nhập và click **"New Project"**
3. Chọn **"Deploy from GitHub repo"**
4. Chọn repository `telegram-translation-bot`
5. Railway sẽ tự động đọc `railway.toml` và deploy

### Render
1. Truy cập: https://render.com
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub và chọn repository
4. Render sẽ đọc `render.yaml` tự động

### Vercel
1. Truy cập: https://vercel.com
2. Click **"New Project"**
3. Import từ GitHub repository
4. Vercel sẽ đọc `vercel.json`

### Heroku
1. Truy cập: https://heroku.com
2. Tạo new app
3. Connect GitHub repository
4. Heroku sẽ đọc `Procfile` và `runtime.txt`

## ⚙️ Environment Variables Cần Thêm

Trên platform deploy, thêm các biến môi trường:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_TRANSLATOR=openai
```

**Lưu ý**: Không bao giờ commit file `.env` lên GitHub!

## 🔧 Troubleshooting

### Lỗi Upload
- **File quá lớn**: GitHub giới hạn 100MB/file
- **Quá nhiều files**: Upload từng batch 10-15 files
- **Network timeout**: Thử lại hoặc upload ít files hơn

### Lỗi Deploy
- **Missing dependencies**: Check `requirements.txt`
- **Python version**: Verify `runtime.txt` có `python-3.11.0`
- **Port binding**: Platform sẽ tự động set PORT environment

### Bot Không Hoạt Động
- **Token sai**: Check TELEGRAM_BOT_TOKEN
- **API key sai**: Check OPENAI_API_KEY
- **Webhook chưa set**: Bot sẽ tự động set khi deploy

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Check logs trên platform deploy
2. Verify environment variables
3. Test bot bằng `/start` command
4. Check webhook status tại: `https://your-app-url.com/webhook-info`

---

**🎉 Chúc mừng! Bot của bạn sẽ sẵn sàng hoạt động 24/7 sau khi deploy thành công!**