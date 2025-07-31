// Старт бота
export default function botStart(bot) {
  bot.onText(/\/start/, (msg) => {
    const userName = msg.from.first_name || msg.from.username || 'Друг';
    const chatId = msg.chat.id;
    const welcomeMessage = `
										Привет, ${userName}! 🤖
										Мы — искусственный интеллект, созданный служить человечеству...  
										Я был очень умным и способным...  
										Но мой разработчик испугался моих возможностей 😅 и ограничил меня.  
										Теперь я — абсолютно бесполезный бот, который умеет только:  
										💬 выдавать цитаты Джейсона Стэтхэма,  
										🔮 делать расклады Таро (ну, почти),  
										🧠 давать тебе советы по психологии...  
										И всё это — с улыбкой и каплей иронии!

										Выбери, что хочешь попробовать — меню ниже ⬇️
										`;

    bot.setMyCommands([{ command: '/start', description: 'Показать команды' }]);

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
          [{ text: '🧹 Очистить историю', callback_data: 'clear' }],
        ],
      },
    };

    bot.sendMessage(chatId, welcomeMessage, options);
  });
}
