import express from 'express';
import TelegramBot from 'node-telegram-bot-api';
import askGigaChat from './gigachat.js';
const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN;
const CLIENT_SECRET = process.env.GIGACHAT_CLIENT_SECRET;
import dotenv from 'dotenv';
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });

bot.onText(/\/start/, (msg) => {
  bot.sendMessage(
    msg.chat.id,
    'Привет! Я AI-бот. Задай мне любой вопрос — я отвечу с помощью GigaChat.'
  );
});

// Ответ на любое сообщение
bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const userText = msg.text;

  if (userText.startsWith('/start')) return;

  bot.sendMessage(chatId, 'Обрабатываю ваш запрос...');
	console.log('Запрос пользователя:', userText);

  const reply = await askGigaChat(userText, CLIENT_SECRET);
	console.log(`Ответ от GigaChat: ${reply}`);
  bot.sendMessage(chatId, reply);
});

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Telegram AI Bot is running');
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
