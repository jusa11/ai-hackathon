// Старт бота
export default function botStart(bot) {
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
}
