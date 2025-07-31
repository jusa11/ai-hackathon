import ChatService from './ChatService.js';
import logs from './utils/logs.js';
import setMode from './utils/setMode.js';

export default function botResponse(bot, users, userModes) {
  bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const userText = msg.text;
    const userId = msg.from.id;

    if (!userText || userText.startsWith('/')) return;

    const user = setMode(users, userId);
    const mode = userModes.get(userId);
    console.log('ТЕКУЩИЙ МОД' + mode);
    let reply = '';

    if (mode) {
      reply = await new ChatService(user, userText, mode).ask();
    } else {
      reply = 'Пожалуйста, выберите функцию через меню.';
    }

    user.addMessage(userText, 'user', mode);
    user.addMessage(reply, 'assistant', mode);

    logs(user, userId);

    bot.sendMessage(chatId, reply);
  });
}
