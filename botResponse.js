import ChatService from './ChatService.js';
import setMode from './utils/setMode.js';

export default function botResponse(bot, users, userModes) {
  bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const userText = msg.text;
    const userId = msg.from.id;

    if (!userText || userText.startsWith('/')) return;

    const user = setMode(users, userId);
    const mode = userModes.get(userId);
    let reply = '';

    if (mode === 'quiz') {
      const quiz = user.getQuiz();
      reply = quiz.checkAnswer(userText);

      if (quiz.Success) {
        return bot.sendMessage(chatId, reply, {
          reply_markup: {
            inline_keyboard: [
              [{ text: '🔄 Вернуться в меню', callback_data: 'menu' }],
            ],
          },
        });
      }
    } else if (mode === 'ask') {
      reply = await new ChatService(user, userText, mode).askGigaChat();
    } else {
      reply = await new ChatService(user, userText, mode).ask();
    }

    user.addMessage(userText, 'user', mode);
    user.addMessage(reply, 'assistant', mode);

    bot.sendMessage(chatId, reply, { parse_mode: 'Markdown' });
  });
}
