# Hướng Dẫn Deploy Telegram Bot

Hướng dẫn chi tiết để deploy bot Telegram lên các dịch vụ hosting miễn phí.

## 📋 Chuẩn Bị Trước Khi Deploy

### 1. Kiểm Tra Files Cần Thiết
- ✅ `main.py` - File chính của bot (hỗ trợ webhook)
- ✅ `requirements.txt` - Danh sách thư viện (bao gồm Flask)
- ✅ `.env.example` - Mẫu biến môi trường
- ✅ `.gitignore` - Bảo vệ thông tin nhạy cảm
- ✅ `Procfile` - Cấu hình cho Heroku
- ✅ `runtime.txt` - Phiên bản Python cho Heroku
- ✅ `vercel.json` - Cấu hình cho Vercel
- ✅ `railway.toml` - Cấu hình cho Railway
- ✅ `render.yaml` - Cấu hình cho Render
- ✅ `README.md` - Hướng dẫn sử dụng

### 2. Tạo Repository GitHub
```bash
# Khởi tạo Git repository
git init
git add .
git commit -m "Initial commit: Telegram bot with webhook support"

# Tạo repository trên GitHub và push
git remote add origin https://github.com/username/telegram-bot.git
git branch -M main
git push -u origin main
```

## 🚀 Các Dịch Vụ Hosting Miễn Phí

### 1. Railway (Khuyến Nghị)

**Ưu điểm:**
- Miễn phí $5/tháng credit
- Hỗ trợ Python tự động
- Webhook URL tự động
- Dễ sử dụng

**Các bước deploy:**

1. **Tạo tài khoản Railway**
   - Truy cập [railway.app](https://railway.app)
   - Đăng nhập bằng GitHub

2. **Deploy từ GitHub**
   ```bash
   # Tạo repository mới trên GitHub
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/username/telegram-bot.git
   git push -u origin main
   ```

3. **Kết nối với Railway**
   - Nhấn "New Project" → "Deploy from GitHub repo"
   - Chọn repository của bạn
   - Railway sẽ tự động detect file `railway.toml` và build

4. **Cấu hình biến môi trường**
   - Vào tab "Variables"
   - Thêm các biến từ file `.env.example`:
     - `TELEGRAM_BOT_TOKEN`
     - `OPENAI_API_KEY`
     - `GLM_API_KEY` (tùy chọn)
     - `CEREBRAS_API_KEY` (tùy chọn)
     - `DEFAULT_TRANSLATOR=openai`

5. **Kiểm tra deployment**
   - Vào tab "Deployments" để xem logs
   - Bot sẽ tự động chạy ở chế độ webhook
   - Kiểm tra URL domain được cấp để test health endpoint

### 2. Render

**Ưu điểm:**
- ✅ Miễn phí với 750 giờ/tháng
- ✅ Tự động deploy từ Git
- ✅ SSL certificate miễn phí
- ✅ Logs chi tiết
- ✅ Hỗ trợ file cấu hình render.yaml

**Nhược điểm:**
- ❌ Service "ngủ" sau 15 phút không hoạt động
- ❌ Khởi động lại chậm (30-60 giây)

1. **Tạo tài khoản Render**
   - Truy cập [render.com](https://render.com)
   - Đăng nhập bằng GitHub

2. **Deploy từ GitHub**
   - Push code lên GitHub repository
   - Render sẽ tự động detect file `render.yaml`

3. **Tạo Web Service**
   - Nhấn "New" → "Web Service"
   - Connect GitHub repository
   - Render sẽ đọc cấu hình từ `render.yaml`

4. **Cấu hình biến môi trường**
   - Thêm các biến environment trong dashboard:
     - `TELEGRAM_BOT_TOKEN`
     - `OPENAI_API_KEY`
     - `GLM_API_KEY` (tùy chọn)
     - `CEREBRAS_API_KEY` (tùy chọn)

5. **Deploy và kiểm tra**
   - Render sẽ tự động build và deploy
   - Bot chạy ở chế độ webhook với domain được cấp

### 3. Heroku (Có phí)

**Lưu ý:** Heroku đã ngừng free tier từ 2022

**Cấu hình cần thêm:**

Tạo file `Procfile`:
```
web: python main.py
```

Tạo file `runtime.txt`:
```
python-3.11.0
```

### 4. Vercel (Serverless)

**Ưu điểm:**
- ✅ Miễn phí cho hobby projects
- ✅ Deploy cực nhanh
- ✅ Global CDN
- ✅ Tự động HTTPS
- ✅ Hỗ trợ file cấu hình vercel.json

**Nhược điểm:**
- ❌ Chỉ hỗ trợ serverless functions
- ❌ Giới hạn thời gian execution (10s cho free plan)
- ❌ Phức tạp hơn cho bot Telegram

1. **Tạo tài khoản Vercel**
   - Truy cập [vercel.com](https://vercel.com)
   - Đăng nhập bằng GitHub

2. **Deploy từ GitHub**
   - Push code lên GitHub repository
   - Import project từ Vercel dashboard

3. **Cấu hình tự động**
   - Vercel sẽ đọc file `vercel.json`
   - Tự động setup routes và environment

4. **Thêm Environment Variables**
   - Vào Project Settings → Environment Variables
   - Thêm các biến cần thiết:
     - `TELEGRAM_BOT_TOKEN`
     - `OPENAI_API_KEY`
     - `GLM_API_KEY` (tùy chọn)
     - `CEREBRAS_API_KEY` (tùy chọn)

5. **Deploy và test**
   - Vercel tự động deploy khi có commit mới
   - Bot chạy ở chế độ serverless với webhook

**Cấu hình:**

Tạo file `vercel.json`:
```json
{
  "functions": {
    "main.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    {
      "src": "/webhook",
      "dest": "/main.py"
    }
  ]
}
```

**Lưu ý:** Vercel phù hợp cho bot với traffic thấp do giới hạn serverless.

## 🔧 Cấu Hình Webhook

### Cập Nhật Code Cho Webhook

Bot hiện tại đã hỗ trợ webhook. Khi deploy, bot sẽ tự động:
1. Detect môi trường production
2. Sử dụng webhook thay vì polling
3. Set webhook URL tự động

### Biến Môi Trường Cần Thiết

```env
# Bắt buộc
TELEGRAM_BOT_TOKEN=your_bot_token

# API Keys (ít nhất 1 cái)
OPENAI_API_KEY=your_openai_key
GLM_API_KEY=your_glm_key
CEREBRAS_API_KEY=your_cerebras_key

# Tùy chọn
DEFAULT_TRANSLATOR=openai
PORT=8000
WEBHOOK_URL=https://your-app.railway.app/webhook
```

## 🔍 Kiểm Tra Sau Khi Deploy

### 1. Kiểm Tra Logs
- Railway: Dashboard → Deployments → Logs
- Render: Dashboard → Logs
- Heroku: `heroku logs --tail`

### 2. Test Bot
1. Mở Telegram
2. Tìm bot của bạn
3. Gửi `/start`
4. Test các lệnh dịch

### 3. Kiểm Tra Webhook
```bash
# Kiểm tra webhook status
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
```

## 🐛 Troubleshooting

### Lỗi Thường Gặp

1. **Bot không phản hồi:**
   - Kiểm tra webhook URL
   - Kiểm tra logs
   - Verify bot token

2. **Import errors:**
   - Kiểm tra `requirements.txt`
   - Đảm bảo Python version tương thích

3. **API errors:**
   - Kiểm tra API keys
   - Kiểm tra quota/limits

### Debug Commands

```bash
# Xem webhook info
curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo

# Xóa webhook (để test local)
curl https://api.telegram.org/bot<TOKEN>/deleteWebhook

# Set webhook thủ công
curl -X POST https://api.telegram.org/bot<TOKEN>/setWebhook \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-app.railway.app/webhook"}'
```

## 💡 Tips Tối Ưu

1. **Monitoring:**
   - Sử dụng logging để track errors
   - Monitor API usage
   - Set up alerts

2. **Performance:**
   - Cache responses khi có thể
   - Optimize API calls
   - Use async/await

3. **Security:**
   - Không commit `.env` file
   - Sử dụng webhook secret
   - Validate incoming requests

## 📞 Hỗ Trợ

Nếu gặp vấn đề:
1. Kiểm tra logs
2. Đọc documentation của hosting service
3. Kiểm tra Telegram Bot API docs
4. Search Stack Overflow

---

**Lưu ý:** Đảm bảo không bao giờ commit file `.env` chứa API keys lên GitHub!