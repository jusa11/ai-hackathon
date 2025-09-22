import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import FormQuery from './FormQuery';
import MetricCard from './MetricCard';
import MetricChart from './MetricChart';
import ChatWithLLM from './ChatWithLLM';

const Content = () => {
  const [metrics, setMetrics] = useState([]);
  const [bigMetric, setBigMetric] = useState(null);
  const [isChat, setIsChat] = useState(false);
  const [chatHistory, setChatHistory] = useState([
    {
      id: 1,
      type: 'bot',
      text: 'Привет! Я ваш HR-бот. Задайте вопрос о метриках сотрудников.',
      result: null,
      type_chart: null,
    },
  ]);

  const contentRef = useRef(null);

  // Загружаем обычные и big метрики
  const loadMetrics = async () => {
    try {
      const res = await axios.get('http://localhost:8000/metric/random');
      setMetrics(res.data);

      const bigRes = await axios.get('http://localhost:8000/metric/big');
      setBigMetric(bigRes.data);
    } catch (error) {
      console.error(`Ошибка при получении метрик: ${error}`);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  // Автопрокрутка вниз при добавлении нового сообщения
  useEffect(() => {
    if (contentRef.current) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const handleChat = () => {
    isChat ? setIsChat(false) : setIsChat(true);
    console.log(isChat);
  };

  return (
    <div className="relative flex-1 flex flex-col h-full overflow-hidden">
      {/* Контент с прокруткой */}
      <main ref={contentRef} className="flex-1 flex flex-col p-4 overflow-auto">
        {/* Метрики */}
        <div className={`${isChat ? 'hidden' : 'flex flex-col gap-4'}`}>
          <div className="grid grid-cols-3 gap-4">
            {metrics.map((metric, index) => (
              <MetricCard metric={metric} big={false} key={index} />
            ))}
          </div>

          {bigMetric && (
            <div className="mt-6 grid grid-cols-1 rounded-3xl">
              <MetricCard metric={bigMetric[0]} big={true} />
            </div>
          )}
        </div>

        <ChatWithLLM
          chatHistory={chatHistory}
          isChat={isChat}
          setIsChat={setIsChat}
        />
      </main>

      <button
        className={`${
          isChat ? 'hidden' : 'w-full bg-blue-700 text-white py-2 '
        }`}
        onClick={handleChat}
      >
        Открыть чат
      </button>

      {/* Форма ввода — всегда внизу поверх переписки */}
      <div
        className={`${
          isChat
            ? 'fixed bottom-4 left-1/2 -translate-x-1/2 w-full max-w-[600px] z-20'
            : 'hidden'
        }`}
      >
        <FormQuery
          addMessage={(msg) => setChatHistory((prev) => [...prev, msg])}
        />
      </div>
    </div>
  );
};

export default Content;
