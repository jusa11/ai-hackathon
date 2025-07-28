import express from 'express';
import TelegramBot from 'node-telegram-bot-api';
import askGigaChat from './gigachat.js';
import UserHistory from './UserHistory.js';

const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN;
const CLIENT_SECRET = process.env.GIGACHAT_CLIENT_SECRET;
import dotenv from 'dotenv';
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

const users = new Map();
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
  const userName = msg.from.username || `id_${chatId}`;

  if (userText.startsWith('/start')) return;

  if (!users.has(userName)) {
    users.set(userName, new UserHistory(userName));
  }

  const user = users.get(userName);

  const reply = await askGigaChat(user, userText, CLIENT_SECRET);
  
  user.addMessage(userText, 'user');
  user.addMessage(reply, 'assistant');

  bot.sendMessage(chatId, reply);

  console.log(user.getHistory(), 'История пользователя:', userName);
});


app.use(express.json());

app.get('/', (req, res) => {
  res.send('Telegram AI Bot is running');
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
