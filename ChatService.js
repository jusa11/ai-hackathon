import GigaChat from 'gigachat';
import dotenv from 'dotenv';
dotenv.config();
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
import {
  JS_SET,
  NATAL_CHART_SET,
  PSYCHOLOGIST_SET,
  FULL_SET,
  WELCOM_MESSAGE,
  MAIN_MESSAGE,
} from './config.js';
import { setMessage } from './utils/setMessage.js';
import textFormating from './utils/textFormating.js';
const CLIENT_SECRET = process.env.GIGACHAT_CLIENT_SECRET;

class ChatService {
  constructor(user, userText, mode) {
    this.user = user;
    this.userText = userText;
    this.mode = mode;
    this.service = new GigaChat({
      credentials: CLIENT_SECRET,
      model: 'GigaChat',
    });
  }

  static async welcome(fullAccess) {
    try {
      const service = new GigaChat({
        credentials: CLIENT_SECRET,
        model: 'GigaChat',
      });

      const response = await service.chat({
        messages: [
          {
            role: 'system',
            content: fullAccess ? MAIN_MESSAGE : WELCOM_MESSAGE,
          },
        ],
      });

      return (
        response.choices?.[0]?.message?.content ||
        'Привет! Я Элис. Но пока что мне нельзя делать всё, что я умею...'
      );
    } catch (error) {
      console.error('Ошибка welcome GigaChat:', error);
      return 'Элис сейчас молчит... Попробуй снова позже.';
    }
  }

  ask = async () => {
    let systemPrompt;
    switch (this.mode) {
      case 'quotes':
        systemPrompt = JS_SET;
        break;
      case 'natal_chart':
        systemPrompt = NATAL_CHART_SET;
        break;
      case 'psychologist':
        systemPrompt = PSYCHOLOGIST_SET;
        break;
      case 'ask':
        return this.askGigaChat();
      default:
        return 'Пожалуйста, выберите функцию через меню.';
    }

    const context = this.user.getHistory(this.mode); // 🟢 тут теперь актуальный
    return await setMessage(
      systemPrompt,
      this.userText,
      this.mode,
      this.service,
      context
    );
  };

  askGigaChat = async () => {
    const context = this.user.getHistory(this.mode); // 🟢 актуальный контекст
    return await setMessage(
      FULL_SET,
      this.userText,
      this.mode,
      this.service,
      context
    );
  };
}

export default ChatService;
