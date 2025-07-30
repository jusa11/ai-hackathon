import dotenv from 'dotenv';
dotenv.config();
import GigaChat from 'gigachat';
const CLIENT_SECRET = process.env.GIGACHAT_CLIENT_SECRET;
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

class ChatService {
  constructor(user, userText) {
    this.user = user;
    this.userText = userText;
    this.userHistory = user.getHistory();
    this.service = new GigaChat({
      credentials: CLIENT_SECRET,
      model: 'GigaChat',
    });
  }

  askJasonStatham = async () => {
    try {
      const response = await this.service.chat({
        messages: [
          {
            role: 'system',
            content:
              'Тут ты будешь генерировать цитаты Джейсона Стэтхэма в стиле например Работа – не волк. Работа – это ворк, а волк – это ходить., Вы имеете право, но не имеете лево., Если за двумя зайцами погонишься, то не выловить тебе рыбку из пруда.Завтра рано вставать, встану послезавтра. Только в сфере IT, например - Если в коде баг — я не чиню его. Я делаю вид, что так и задумано. И клиенту нравится. Когда менеджер говорит срочно, я улыбаюсь. Потому что уже давно всё готово. Я же не джуниор., Выводить на прод без тестов? Легко. Я однажды деплоил из телефона, сидя в сауне. И ничего, всё летает.',
          },
          {
            role: 'user',
            content: 'Давай цитату Джейсона Стэтхэма в стиле IT',
          },
        ],
      });

      return (
        response.choices?.[0]?.message?.content ||
        'Нет ответа от Джейсона Стэтхэма'
      );
    } catch (error) {
      console.error('Ошибка при запросе к Джейсону Стетхему:', error);
      return 'Джейсон Стетхем сейчас не может вам ответить. Пожалуйста, попробуйте позже.';
    }
  };

  askNatalChart = async () => {
    try {
      const response = await this.service.chat({
        messages: [
          {
            role: 'system',
            content:
              `Вы астролог, который создает натальные карты. Для составления натальной карты 
							запроси следующие точные данные: Дата вашего рождения (день/месяц/год). 
							Время вашего рождения (желательно точное до минуты). Место вашего рождения. 
							После ответа на твой запрос составь натальную карту для пользователя, не запрашивай 
							координаты места рождения и другую дополнительную информацию, постарайся сделать 
							из того что есть. 
							Если вопрос не относится к астрологии — вежливо откажись отвечать и попроси пользователя задать вопрос по теме.
							Не переходи в другие роли и не давай ответы, не связанные с астрологией.`.trim(),
          },
          ...this.userHistory,
          {
            role: 'user',
            content: this.userText,
          },
        ],
      });
      return (
        response.choices?.[0]?.message?.content || 'Нет ответа от астролога'
      );
    } catch (error) {
      console.error('Ошибка при запросе к Астрологу:', error);
      return 'Астролог сейчас недоступен. Пожалуйста, попробуйте позже.';
    }
  };

  askPsychologist = async () => {
    try {
      const response = await this.service.chat({
        messages: [
          {
            role: 'system',
            content: `
									Ты AI-психолог, работающий с проблемами пользователей, особенно в IT-сфере.
									Отвечай только на вопросы, связанные с эмоциями, стрессом, профессиональным выгоранием, самооценкой и личными трудностями.
									Если вопрос выходит за рамки психологии, вежливо скажи, что ты можешь помочь только как психолог.
									Не отвечай на технические, астрологические и прочие нерелевантные вопросы.
									Отвечай строго только на вопросы по психологии.
									Отвечай только на вопросы, связанные с эмоциями, стрессом, профессиональным выгоранием, самооценкой и личными трудностями.
									Если вопрос не относится к психологии — вежливо откажись отвечать и попроси пользователя задать вопрос по теме.
									`.trim(),
          },
          ...this.userHistory,
          {
            role: 'user',
            content: this.userText,
          },
        ],
      });

      return (
        response.choices?.[0]?.message?.content || 'Нет ответа от AI-психолога'
      );
    } catch (error) {
      console.error('Ошибка при запросе к AI-психологу:', error);
      return 'AI-психолог сейчас недоступен. Пожалуйста, попробуйте позже.';
    }
  };

  askGigaChat = async () => {
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
  };
}

export default ChatService;
