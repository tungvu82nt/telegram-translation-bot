# 🚀 Hướng Dẫn Deploy Nhanh Bot Telegram

## 📋 Checklist Trước Khi Deploy

- [ ] Đã có Telegram Bot Token từ @BotFather
- [ ] Đã có OpenAI API Key (hoặc GLM/Cerebras)
- [ ] Đã test bot ở local thành công
- [ ] Đã tạo GitHub repository

## ⚡ Deploy Nhanh Nhất - Railway (Khuyến nghị)

### Bước 1: Chuẩn bị code
```bash
# Clone hoặc tải project về
git clone <your-repo-url>
cd telegram-bot

# Tạo file .env từ mẫu
cp .env.example .env
# Điền thông tin vào .env
```

### Bước 2: Push lên GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Bước 3: Deploy trên Railway
1. Truy cập [railway.app](https://railway.app)
2. Đăng nhập bằng GitHub
3. Nhấn "New Project" → "Deploy from GitHub repo"
4. Chọn repository của bạn
5. Thêm Environment Variables:
   - `TELEGRAM_BOT_TOKEN=your_bot_token`
   - `OPENAI_API_KEY=your_openai_key`
   - `DEFAULT_TRANSLATOR=openai`

### Bước 4: Kiểm tra
- Vào tab "Deployments" xem logs
- Bot sẽ tự động chạy với webhook
- Test bằng cách gửi tin nhắn cho bot

## 🎯 Các Lựa Chọn Khác

| Platform | Ưu điểm | Nhược điểm | Thời gian setup |
|----------|---------|------------|------------------|
| **Railway** | Dễ dùng, ổn định | Có giới hạn free | 5 phút |
| **Render** | Miễn phí 750h/tháng | Service "ngủ" | 7 phút |
| **Heroku** | Ổn định, nhiều tính năng | Có phí | 10 phút |
| **Vercel** | Nhanh, global CDN | Chỉ serverless | 15 phút |

## 🔧 Troubleshooting

### Bot không phản hồi?
1. Kiểm tra logs trong dashboard
2. Đảm bảo `TELEGRAM_BOT_TOKEN` đúng
3. Kiểm tra `OPENAI_API_KEY` có credits

### Webhook không hoạt động?
1. Kiểm tra domain có HTTPS
2. Xem logs có lỗi gì
3. Test health endpoint: `https://your-domain.com/health`

### Lỗi dependencies?
1. Kiểm tra `requirements.txt`
2. Đảm bảo Python version đúng (3.11)
3. Xem build logs chi tiết

## 📞 Hỗ Trợ

Nếu gặp vấn đề, kiểm tra:
1. File `README_DEPLOYMENT.md` - Hướng dẫn chi tiết
2. Logs trong dashboard của platform
3. File `.env.example` - Mẫu cấu hình

---

**Lưu ý:** Bot sẽ tự động chuyển từ polling (local) sang webhook (production) khi deploy.