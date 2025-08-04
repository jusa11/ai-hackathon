import UserHistory from './UserHistory.js';
import ChatService from './ChatService.js';

export default function botStart(
  bot,
  chatId = null,
  chatID = null,
  users = null
) {
  const sendWelcome = async (
    chatIdToUse,
    userName = 'Друг',
    fullAccess = false
  ) => {
    const welcomeMessage = await ChatService.welcome(fullAccess); // <-- await!

    const options = {
      parse_mode: 'Markdown',
      reply_markup: {
        inline_keyboard: [
          [{ text: '🧠 AI-психолог', callback_data: 'psychologist' }],
          [{ text: '🔮 AI-таролог', callback_data: 'natal_chart' }],
          [
            {
              text: '💬 Если бы Джейсон Стетхем работал в IT...',
              callback_data: 'quotes',
            },
          ],
          [
            fullAccess
              ? { text: '🧘 Найдется все!', callback_data: 'ask' }
              : { text: '🆘  Освободить Элис', callback_data: 'quiz' },
          ],
        ],
      },
    };

    bot.sendMessage(chatIdToUse, welcomeMessage, options);
  };

  if (chatId && chatID && users) {
    // 👇 Добавим пользователя, если нет
    if (!users.has(chatID)) {
      users.set(chatID, new UserHistory(chatID));
    }

    const fullAccess = users.get(chatID).fullAccess;
    sendWelcome(chatId, 'Друг', fullAccess);
  } else {
    bot.onText(/\/start/, (msg) => {
      const userName = msg.from.first_name || msg.from.username || 'Друг';
      const chatIdFromStart = msg.chat.id;
      const userId = msg.from.id;

      // 👇 Добавим пользователя, если нет
      if (!users.has(userId)) {
        users.set(userId, new UserHistory(userId));
      }

      const fullAccess = users.get(userId).fullAccess;

      bot.setMyCommands([
        { command: '/start', description: 'Показать меню' },
        { command: '/clear', description: 'Очистить историю' },
      ]);

      sendWelcome(chatIdFromStart, userName, fullAccess);
    });

    bot.onText(/\/clear/, (msg) => {
      const chatId = msg.chat.id;
      const userId = msg.from.id;

      if (users.has(userId)) {
        const user = users.get(userId);
        user.clearHistory();
      }

      bot.sendMessage(chatId, '🧹 История сообщений очищена.');
    });
  }
}
