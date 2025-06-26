 🎥 OTT-POSTERS-VERCEL  
*Transforming Streaming Content into Visual Masterpieces*  

[![Last Commit](https://img.shields.io/github/last-commit/yourusername/ott-posters-vercel?color=29bf12&style=for-the-badge)](https://github.com/yourusername/ott-posters-vercel/commits/main) 
![Languages](https://img.shields.io/github/languages/count/yourusername/ott-posters-vercel?style=for-the-badge) 
![JavaScript](https://img.shields.io/badge/javascript-92.3%25-yellow?style=for-the-badge)

📦 Built With
<div align="center">
  <img src="https://img.shields.io/badge/-JSON-333?style=for-the-badge&logo=json&logoColor=white">
  <img src="https://img.shields.io/badge/-Markdown-000000?style=for-the-badge&logo=markdown">
  <img src="https://img.shields.io/badge/-npm-CB3837?style=for-the-badge&logo=npm">
  <img src="https://img.shields.io/badge/-Mongoose-880000?style=for-the-badge">
  <img src="https://img.shields.io/badge/-.ENV-8c8c8c?style=for-the-badge">
  <img src="https://img.shields.io/badge/-JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
  <img src="https://img.shields.io/badge/-Puppeteer-40B5A4?style=for-the-badge">
  <img src="https://img.shields.io/badge/-React-61DAFB?style=for-the-badge&logo=react&logoColor=black">
  <img src="https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker">
  <img src="https://img.shields.io/badge/-GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white">
</div>

 📖 Overview
A fully-featured OTT Poster Scraper and Telegram Bot built with **Next.js**, **Puppeteer**, **MongoDB**, and **Telegraf**. Supports scraping posters for **51+ OTT platforms** via Telegram bot commands and a responsive web scraping interface.

 🚀 Features
- 🔥 51+ OTT platform commands auto-generated from JSON config
- ⚡ Puppeteer-powered poster scraping API
- 📱 Telegram bot via Webhook (Docker or Vercel-compatible)
- 📊 MongoDB Atlas for user tracking
- 📈 Admin commands: `/stats`, `/help`, `/broadcast`
- 💻 Next.js frontend for custom URL scraping
- 🐳 Docker & Docker Compose support
- 🔄 GitHub Actions CI/CD with Docker Hub integration

🛠️ Tech Stack
- **Frontend**: Next.js, React
- **Backend**: Node.js, Telegraf
- **Scraping**: Puppeteer
- **Database**: MongoDB
- **DevOps**: Docker, GitHub Actions

📊 OTT Platform Configuration
```
{
  "netflix": {
    "url": "https://example.com/netflix",
    "selector": ".poster-img"
  },
  "primevideo": {
    "url": "https://example.com/primevideo",
    "selector": ".poster-img"
  }
}
```
🛠️ Installation

📦 Local Development
```
git clone https://github.com/yourusername/ott-posters-vercel.git
cd ott-posters-vercel
npm install
npm run dev
```
🐳 Docker Setup
```
# Standalone
docker build -t ott-bot-vercel .
docker run -d -p 3000:3000 --env-file .env ott-bot-vercel

# With Docker Compose
docker-compose up --build
```
🌐 Deployment
Vercel
```
vercel --prod
```
Telegram Webhook
```
https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://your-vercel-app/api/telegram?secret=YOUR_SECRET
```
🔐 Environment Variables
Create .env file with:

```
MONGODB_URI=your-mongodb-uri
BOT_TOKEN=your-telegram-bot-token
BOT_OWNER=your-telegram-id
TELEGRAM_WEBHOOK_SECRET=secure-token

```
🤖 Telegram Commands
Command	Description

```
/start	Welcome message & user registration
/help	List available OTT commands
/netflix	Scrape Netflix posters
/primevideo	Scrape Prime Video posters
/stats	Show bot statistics (admin only)
/broadcast	Broadcast message (admin only)
/any-ott-name	Scrape posters for specified OTT

```
🔄 CI/CD Pipeline
GitHub Actions workflow automatically builds and pushes Docker image to Docker Hub when pushing to main branch.

🤝 Contributing
Fork the repository

```
Create your feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add some amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

```
📄 License
MIT 
https://img.shields.io/badge/License-MIT-blue.svg


```
npm run dev

```
