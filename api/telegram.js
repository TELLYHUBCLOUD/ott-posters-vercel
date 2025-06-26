import { Telegraf } from 'telegraf';
import { connectToDatabase } from '../../lib/db.js';
import mongoose from 'mongoose';
import puppeteer from 'puppeteer';
import ottConfig from '../../ott-posters.json' assert { type: "json" };

const bot = new Telegraf(process.env.BOT_TOKEN);
let botStartTime = Date.now();

const userSchema = new mongoose.Schema({
  telegramId: Number,
  firstName: String,
  username: String,
  joinedAt: { type: Date, default: Date.now }
});
const User = mongoose.models.User || mongoose.model('User', userSchema);

await connectToDatabase();

bot.start(async (ctx) => {
  const { id, first_name, username } = ctx.from;
  await User.updateOne(
    { telegramId: id },
    { telegramId: id, firstName: first_name, username },
    { upsert: true }
  );
  ctx.reply(`👋 Welcome ${first_name}! Type /help to see available OTT commands.`);
});

bot.command('help', (ctx) => {
  const commands = Object.keys(ottConfig).map(cmd => `/${cmd}`).join('\n');
  ctx.reply(`🎥 Available OTT Platforms:\n${commands}\n\n/stats — see bot stats`);
});

// Dynamic scraper commands
Object.keys(ottConfig).forEach(platform => {
  bot.command(platform, async (ctx) => {
    const { url, selector } = ottConfig[platform];
    ctx.reply(`🔍 Scraping ${platform} posters...`);
    
    let browser;
    try {
      browser = await puppeteer.launch({ 
        headless: "new", 
        args: ['--no-sandbox', '--disable-setuid-sandbox'] 
      });
      const page = await browser.newPage();
      await page.goto(url, { waitUntil: 'networkidle2' });
      await page.waitForSelector(selector);
      const posters = await page.$$eval(selector, imgs => imgs.map(img => img.src));
      await browser.close();

      if (posters.length) {
        await ctx.replyWithMediaGroup(posters.slice(0, 5).map(p => ({ type: 'photo', media: p })));
      } else {
        ctx.reply('❌ No posters found.');
      }
    } catch (err) {
      console.error(err);
      if (browser) await browser.close();
      ctx.reply('❌ Scrape failed.');
    }
  });
});

bot.command('stats', async (ctx) => {
  const totalUsers = await User.countDocuments();
  const uptime = Math.floor((Date.now() - botStartTime) / 1000);
  ctx.reply(`📊 Users: ${totalUsers}\n⏱️ Uptime: ${uptime}s`);
});

bot.command('broadcast', async (ctx) => {
  if (ctx.from.id != process.env.BOT_OWNER) return ctx.reply('❌ Unauthorized.');
  const msg = ctx.message.text.replace('/broadcast', '').trim();
  if (!msg) return ctx.reply('Usage: /broadcast your message here');
  const users = await User.find();
  users.forEach(user => {
    bot.telegram.sendMessage(user.telegramId, `📢 ${msg}`).catch(() => {});
  });
  ctx.reply(`✅ Broadcast sent to ${users.length} users.`);
});

export const config = { api: { bodyParser: false } };

export default async function handler(req, res) {
  if (req.query.secret !== process.env.TELEGRAM_WEBHOOK_SECRET) return res.status(403).send('Forbidden');
  await bot.handleUpdate(req.body);
  res.status(200).send('OK');
}
