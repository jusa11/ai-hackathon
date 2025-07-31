// Обработка нажатия на кнопки
import UserHistory from './UserHistory.js';
import ChatService from './ChatService.js';
import setMode from './utils/setMode.js';

export default function handlerBtn(bot, users, userModes) {
  bot.on('callback_query', async (callbackQuery) => {
    const chatId = callbackQuery.message.chat.id;
    const data = callbackQuery.data;
    const userId = callbackQuery.from.id;
    const userText = callbackQuery.message.text;

    if (data === 'clear') {
      new UserHistory(userId).clearHistory();
      users.delete(userId);
      bot.sendMessage(chatId, 'История сообщений очищена.');
    } else {
      if (!users.has(userId)) {
        users.set(userId, new UserHistory(userId));
      }

      userModes.set(userId, data);

      const mode = userModes.get(userId);
      const user = setMode(users, userId);

      console.log('Текущий мод: ' + mode);

      const reply = await new ChatService(user, userText, mode).ask();
      bot.sendMessage(chatId, reply);
    }

    bot.answerCallbackQuery(callbackQuery.id);
  });
}
