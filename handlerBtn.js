// Обработка нажатия на кнопки
import UserHistory from './UserHistory.js';
import ChatService from './ChatService.js';
import botStart from './botStart.js';
import Quiz from './Quiz.js';
import setMode from './utils/setMode.js';

export default function handlerBtn(bot, users, userModes) {
  bot.on('callback_query', async (callbackQuery) => {
    const chatId = callbackQuery.message.chat.id;
    const data = callbackQuery.data;
    const userId = callbackQuery.from.id;
    const userText = callbackQuery.message.text;

    userModes.set(userId, data);

    const mode = userModes.get(userId);
    const user = setMode(users, userId);

    // console.log('Текущий режим: ' + mode);

    /*  if (data === 'clear') {
      new UserHistory(userId).clearHistory();
      users.delete(userId);
      bot.sendMessage(chatId, 'История сообщений очищена.');
    } */
    if (data === 'quiz') {
      if (!users.has(userId)) {
        users.set(userId, new UserHistory(userId));
      }

      const user = users.get(userId);
      const quiz = new Quiz(user);
      quiz.startQuiz();
      user.setQuiz(quiz);
      const reply = quiz.getQuestion();

      console.log(reply);
      bot.sendMessage(chatId, reply);
      return;
    }
    if (data === 'menu') {
      botStart(bot, chatId, userId, users); // 👈 это покажет приветственное меню заново
      return;
    }
    if (data === 'ask') {
      const reply = await new ChatService(user, userText, mode).askGigaChat();
      bot.sendMessage(chatId, reply);
    } else {
      if (!users.has(userId)) {
        users.set(userId, new UserHistory(userId));
      }

      const reply = await new ChatService(user, '', mode).ask();
      bot.sendMessage(chatId, reply);
    }

    bot.answerCallbackQuery(callbackQuery.id);
  });
}
