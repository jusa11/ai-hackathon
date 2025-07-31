import GigaChat from 'gigachat';
import dotenv from 'dotenv';
dotenv.config();
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
import { JS_SET, NATAL_CHART_SET, PSYCHOLOGIST_SET } from './config.js';
import { setMessage } from './utils/setMessage.js';
const CLIENT_SECRET = process.env.GIGACHAT_CLIENT_SECRET;

class ChatService {
  constructor(user, userText, mode) {
    this.user = user;
    this.userText = userText;
    this.mode = mode;
    this.userHistory = user.getHistory(mode);
    this.service = new GigaChat({
      credentials: CLIENT_SECRET,
      model: 'GigaChat',
    });
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
      default:
        return 'Пожалуйста, выберите функцию через меню.';
    }
    console.log(this.mode);
    console.log(systemPrompt);
    return await setMessage(
      systemPrompt,
      this.userText,
      this.mode,
      this.service,
      this.userHistory
    );
  };

  /* askGigaChat = async () => {
    try {
      const response = await this.service.chat({
        messages: [
          ...this.userHistory,
          {
            role: 'user',
            content: this.userText,
          },
        ],
      });

      return (
        response.choices?.[0]?.message?.content || 'Нет ответа от GigaChat'
      );
    } catch (error) {
      console.error('Ошибка при запросе к GigaChat:', error);
      return 'Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.';
    }
  }; */
}

export default ChatService;
