import GigaChat from 'gigachat';
import dotenv from 'dotenv';
dotenv.config();
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

const askGigaChat = async (userText, clientSecret) => {
  const giga = new GigaChat({
    credentials: clientSecret,
    model: 'GigaChat',
  });

  try {
    const response = await giga.chat({
      messages: [
        {
          role: 'user',
          content: userText,
        },
      ],
    });
    return response.choices?.[0]?.message?.content || 'Нет ответа от GigaChat';
  } catch (error) {
    console.error('Ошибка при запросе к GigaChat:', error);
    return 'Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.';
  }
};

export default askGigaChat;
