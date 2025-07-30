import express from 'express';
import TelegramBot from 'node-telegram-bot-api';
import ChatService from './ChatService.js';
import UserHistory from './UserHistory.js';
import setMode from './setMode.js';

const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN;
import dotenv from 'dotenv';
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

const users = new Map();
const userModes = new Map();
const bot = new TelegramBot(TELEGRAM_TOKEN, { polling: true });

bot.onText(/\/start/, (msg) => {
  const userName = msg.from.first_name || msg.from.username || 'Друг';
  const chatId = msg.chat.id;
  const welcomeMessage = `Привет, ${userName}! Выбери одну из функций:`;

  const options = {
    reply_markup: {
      inline_keyboard: [
        [{ text: 'Цитаты Стетхема', callback_data: 'quotes' }],
        [{ text: 'Натальная карта', callback_data: 'natal_chart' }],
        [{ text: 'AI-психолог', callback_data: 'psychologist' }],
        [{ text: 'Очистить историю', callback_data: 'clear' }],
      ],
    },
  };

  bot.sendMessage(chatId, welcomeMessage, options);
});

// Обработка нажатия на кнопки
bot.on('callback_query', async (callbackQuery) => {
  const chatId = callbackQuery.message.chat.id;
  const data = callbackQuery.data;
  const userId = callbackQuery.from.id;

  if (data === 'quotes') {
    userModes.set(userId, 'quotes');
    const user = setMode(users, userId);
    const reply = await new ChatService(user).askJasonStatham();
    bot.sendMessage(chatId, reply);
  } else if (data === 'natal_chart') {
    if (!users.has(userId)) {
      users.set(userId, new UserHistory(userId));
    }
    userModes.set(userId, 'natal_chart');
    const user = setMode(users, userId);
    const reply = await new ChatService(user).askNatalChart();

    bot.sendMessage(chatId, reply);
  } else if (data === 'psychologist') {
    if (!users.has(userId)) {
      users.set(userId, new UserHistory(userId));
    }
    userModes.set(userId, 'psychologist');
    const user = setMode(users, userId);
    const reply = await new ChatService(user).askPsychologist();

    bot.sendMessage(chatId, reply);
  } else if (data === 'clear') {
    new UserHistory(userId).clearHistory();
    users.delete(userId);
    bot.sendMessage(chatId, 'История сообщений очищена.');
  }

  bot.answerCallbackQuery(callbackQuery.id);
});

// Ответ на любое сообщение
bot.on('message', async (msg) => {
  const chatId = msg.chat.id;
  const userText = msg.text;
  const userId = msg.from.id;

  if (!userText || userText.startsWith('/')) return;

  const user = setMode(users, userId);
  const mode = userModes.get(userId);

  let reply = '';

  if (mode === 'natal_chart') {
    reply = await new ChatService(user, userText).askNatalChart();
  } else if (mode === 'quotes') {
    reply = await new ChatService(user, userText).askJasonStatham();
  } else {
    reply = await new ChatService(user, userText).askGigaChat();
  }

  user.addMessage(userText, 'user');
  user.addMessage(reply, 'assistant');
  console.log(`История пользователя ${userId}:`);
  console.log(user.getHistory());

  bot.sendMessage(chatId, reply);
});

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Telegram AI Bot is running');
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
