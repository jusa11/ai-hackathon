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

    userModes.set(userId, data);

    const mode = userModes.get(userId);
    const user = setMode(users, userId);

    if (data === 'clear') {
      const user = users.get(userId);
      if (user) {
        user.clearHistory();
      }

      bot.sendMessage(chatId, 'История сообщений очищена.');
      return;
    }

    if (data === 'quiz') {
      if (!users.has(userId)) {
        users.set(userId, new UserHistory(userId));
      }

      const user = users.get(userId);
      const quiz = new Quiz(user);
      quiz.startQuiz();
      user.setQuiz(quiz);
      const first = quiz.getQuestion();

      if (first) {
        bot.sendMessage(chatId, first.text, {
          reply_markup: {
            parse_mode: 'Markdown',
            inline_keyboard: first.options,
          },
        });
      }
      return;
    }
    if (data === 'menu') {
      botStart(bot, chatId, userId, users);
      return;
    }
    if (data === 'ask') {
      bot.sendMessage(chatId, 'Введите ваш вопрос, и я постараюсь помочь!', {
        parse_mode: 'Markdown',
      });
      return;
    }
    if (data.startsWith('quiz_answer_')) {
      const user = users.get(userId);
      const quiz = user.getQuiz();

      if (!quiz) {
        bot.sendMessage(
          chatId,
          'Викторина ещё не началась. Нажмите "Начать викторину".',
          { parse_mode: 'Markdown' }
        );
        return;
      }

      const answer = parseInt(data.replace('quiz_answer_', ''));
      const result = quiz.checkAnswer(answer);

      if (result) {
        await bot.sendMessage(chatId, result.text, {
          reply_markup: {
            inline_keyboard: result.options,
          },
        });
      }

      return;
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
