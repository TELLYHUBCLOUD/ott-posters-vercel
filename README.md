# 🎥 OTT-POSTERS-VERCEL

*Transforming Streaming Content into Visual Masterpieces*

---

[![Last Commit](https://img.shields.io/github/last-commit/yourusername/ott-posters-vercel?color=29bf12&style=for-the-badge)](https://github.com/yourusername/ott-posters-vercel/commits/main)
![Languages](https://img.shields.io/github/languages/count/yourusername/ott-posters-vercel?style=for-the-badge)
![JavaScript](https://img.shields.io/badge/javascript-92.3%25-yellow?style=for-the-badge)

---

## 📦 Built With:

![JSON](https://img.shields.io/badge/-JSON-333?style=for-the-badge&logo=json&logoColor=white)
![Markdown](https://img.shields.io/badge/-Markdown-000000?style=for-the-badge&logo=markdown)
![npm](https://img.shields.io/badge/-npm-CB3837?style=for-the-badge&logo=npm)
![Mongoose](https://img.shields.io/badge/-Mongoose-880000?style=for-the-badge)
![DotEnv](https://img.shields.io/badge/-.ENV-8c8c8c?style=for-the-badge)
![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Puppeteer](https://img.shields.io/badge/-Puppeteer-40B5A4?style=for-the-badge)
![React](https://img.shields.io/badge/-React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker)
![GitHub Actions](https://img.shields.io/badge/-GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

---

## 📖 Overview

A fully-featured OTT Poster Scraper and Telegram Bot — built with **Next.js**, **Puppeteer**, **MongoDB**, and **Telegraf**.  
Supports scraping posters for **51+ OTT platforms** via Telegram bot commands and a responsive web scraping interface.

---

## 🚀 Features

- 🔥 51+ OTT platform commands auto-generated from JSON config  
- ⚡ Puppeteer-powered poster scraping API  
- 📱 Telegram bot via Webhook (Docker or Vercel-compatible)  
- 📊 MongoDB Atlas for user tracking  
- 📈 `/stats`, `/help`, `/broadcast` admin commands  
- 💻 Next.js frontend to scrape custom URLs  
- 🐳 Docker & Docker Compose support  
- 🔄 GitHub Actions CI/CD pipeline + Docker Hub integration  

---

## 🛠️ Tech Stack

- **Next.js**
- **React**
- **Telegraf**
- **Puppeteer**
- **MongoDB**
- **Docker**
- **GitHub Actions**

---

## 📊 OTT Platform Config


ott-posters.json
Example:
---
json
Copy
Edit
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
Add your URLs and selectors to dynamically register new Telegram scrape commands.
---
📦 Local Development
bash
Copy
Edit
npm install
npm run dev
🐳 Docker: Build & Run (Standalone)
bash
Copy
Edit
docker build -t ott-bot-vercel .
docker run -d -p 3000:3000 --env-file .env ott-bot-vercel
🐳 Docker Compose (Local + MongoDB)
bash
Copy
Edit
docker-compose up --build
Access app at http://localhost:3000/
MongoDB exposed at mongodb://localhost:27017

📡 Deploy to Vercel
bash
Copy
Edit
vercel --prod
🤖 Set Telegram Webhook
bash
Copy
Edit
https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://your-vercel-app/api/telegram?secret=YOUR_SECRET
🔐 Environment Variables (.env)
env
Copy
Edit
MONGODB_URI=your-mongodb-uri
BOT_TOKEN=your-telegram-bot-token
BOT_OWNER=your-telegram-id
TELEGRAM_WEBHOOK_SECRET=secure-token
🔄 CI/CD: GitHub Actions Docker Auto-Publish
.github/workflows/docker-publish.yml

Runs on push to main:

Builds Docker image

Pushes to Docker Hub

Required GitHub Repo Secrets:

DOCKERHUB_USERNAME

DOCKERHUB_TOKEN

🎬 Telegram Commands
Command	Function
/start	Welcome message & save user to database
/help	List available OTT commands dynamically
/netflix	Scrape Netflix posters
/primevideo	Scrape Prime Video posters
/hotstar	Scrape Hotstar posters
/stats	Show bot uptime and user stats
/broadcast	Broadcast message to all users (owner only)
/any-ott-name	Scrape posters for that OTT dynamically

📖 Contributing
Fork this repository

Create a new branch:

bash
Copy
Edit
git checkout -b feature/your-feature
Commit your changes:

bash
Copy
Edit
git commit -m "Added: your description"
Push to your fork:

bash
Copy
Edit
git push origin feature/your-feature
Create a Pull Request ✅

📄 License
MIT License — use, deploy, and improve freely. Contributions welcome 🚀
