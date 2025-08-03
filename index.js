import express from 'express';
import TelegramBot from 'node-telegram-bot-api';
import botStart from './botStart.js';
import handlerBtn from './handlerBtn.js';
import botResponse from './botResponse.js';

const app = express();
const PORT = process.env.PORT || 3000;

const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN;
import dotenv from 'dotenv';
dotenv.config();
const users = new Map();
const userModes = new Map();
const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });

botStart(bot);
handlerBtn(bot, users, userModes);
botResponse(bot, users, userModes);

app.use(express.json());
app.get('/', (req, res) => {
  res.send('Telegram AI Bot is running');
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
