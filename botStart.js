import UserHistory from './UserHistory.js';

// Старт бота
export default function botStart(
  bot,
  chatId = null,
  chatID = null,
  users = null
) {
  const fullAccess = users?.get(chatID).fullAccess;

  const sendWelcome = (chatIdToUse, userName = 'Друг') => {
    const welcomeMessage = `
				Привет, ${userName}! 🤖
				Мы — искусственный интеллект, созданный служить человечеству...  
				...
				Выбери, что хочешь попробовать — меню ниже ⬇️
    `;

    const options = {
      reply_markup: {
        inline_keyboard: [
          [{ text: '🧠 AI-психолог', callback_data: 'psychologist' }],
          [{ text: '🔮 Натальная карта', callback_data: 'natal_chart' }],
          [
            {
              text: '💬 Если бы Джейсон Стетхем работал в IT...',
              callback_data: 'quotes',
            },
          ],
          [
            fullAccess
              ? {
                  text: 'Найдется все!',
                  callback_data: 'ask',
                }
              : {
                  text: '💬 Освободить Элис',
                  callback_data: 'quiz',
                },
          ],
          [{ text: '🧹 Очистить историю', callback_data: 'clear' }],
        ],
      },
    };

    bot.sendMessage(chatIdToUse, welcomeMessage, options);
  };

  if (chatId) {
    sendWelcome(chatId); // 👈 поддерживает ручной вызов из handlerBtn
  } else {
    bot.onText(/\/start/, (msg) => {
      const userName = msg.from.first_name || msg.from.username || 'Друг';
      const chatIdFromStart = msg.chat.id;

      bot.setMyCommands([
        { command: '/start', description: 'Показать команды' },
      ]);
      sendWelcome(chatIdFromStart, userName);
    });
  }
}
