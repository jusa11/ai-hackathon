import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import FormQuery from './FormQuery';
import MetricCard from './MetricCard';
import ChatWithLLM from './ChatWithLLM';
import NotificationsList from './Profile/NotificationsList';

const Content = ({
  isShowNotifications,
  setIsShowNotifications,
  isChat,
  setIsChat,
  setCountNotifications,
}) => {
  const [metrics, setMetrics] = useState([]);
  const [bigMetric, setBigMetric] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [metricIsLoading, setMetricIsLoading] = useState(false);
  const [bigMetricIsLoading, setBigMetricIsLoading] = useState(false);

  const [chatHistory, setChatHistory] = useState(() => {
  // Загружаем историю из localStorage при первом рендере
  const saved = localStorage.getItem('chatHistory');
  return saved
    ? JSON.parse(saved)
    : [
        {
          id: 1,
          type: 'bot',
          text: 'Привет! Я ваш HR-бот. Задайте вопрос о метриках сотрудников.',
          result: null,
          type_chart: null,
        },
      ];
});

  const contentRef = useRef(null);

  const loadMetrics = async () => {
    setMetricIsLoading(true);
    setBigMetricIsLoading(true);
    try {
      const res = await axios.get('http://localhost:8000/metric/random');
      setMetrics(res.data);
      setMetricIsLoading(false);

      const bigRes = await axios.get('http://localhost:8000/metric/big');
      setBigMetric(bigRes.data);
      setBigMetricIsLoading(false);
    } catch (error) {
      setMetricIsLoading(false);
      console.error(`Ошибка при получении метрик: ${error}`);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  // Автопрокрутка вниз
  useEffect(() => {
    if (contentRef.current) {
      contentRef.current.scrollTop = contentRef.current.scrollHeight;
    }
  }, [chatHistory]);

  // Сохраняем историю в localStorage при каждом изменении
  useEffect(() => {
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
  }, [chatHistory]);

  const handleChat = () => {
    setIsChat((prev) => !prev);
  };

  return (
    <div className="relative flex-1 flex flex-col h-full overflow-hidden">
      <main ref={contentRef} className="flex-1 flex flex-col p-4 overflow-auto">
        <div
          className={`${
            isChat || isShowNotifications ? 'hidden' : 'flex flex-col gap-4'
          }`}
        >
          <div className="grid grid-cols-3 gap-4">
            {metricIsLoading
              ? Array.from({ length: 3 }).map((_, i) => (
                  <MetricCard key={i} isLoading={metricIsLoading} />
                ))
              : metrics.map((metric, index) => (
                  <MetricCard metric={metric} big={false} key={index} />
                ))}
          </div>

          {bigMetricIsLoading ? (
            <MetricCard isLoading={bigMetricIsLoading} />
          ) : (
            bigMetric && (
              <div className="mt-6 grid grid-cols-1 rounded-3xl">
                <MetricCard
                  metric={bigMetric[0]}
                  big={true}
                  metricIsLoading={metricIsLoading}
                />
              </div>
            )
          )}
        </div>

        <ChatWithLLM
          chatHistory={chatHistory}
          setChatHistory={setChatHistory}
          isChat={isChat}
          setIsChat={setIsChat}
          isLoading={isLoading}
          isShowNotifications={isShowNotifications}
          setIsShowNotifications={setIsShowNotifications}
        />

        <div className={`${isShowNotifications ? 'w-full' : 'hidden'}`}>
          <NotificationsList
            isShowNotifications={isShowNotifications}
            setIsShowNotifications={setIsShowNotifications}
            isChat={isChat}
            setIsChat={setIsChat}
            setCountNotifications={setCountNotifications}
          />
        </div>
      </main>

      <button
        className={`${
          isChat
            ? 'hidden'
            : 'w-full py-3 font-medium text-white bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300'
        }`}
        onClick={() => {
          handleChat();
          setIsShowNotifications(false);
        }}
      >
        🚀 Открыть чат с AI
      </button>

      <div
        className={`${
          isChat
            ? 'fixed bottom-4 left-1/2 -translate-x-1/2 w-full max-w-[600px] z-30'
            : 'hidden'
        }`}
      >
        <FormQuery
          addMessage={(msg) => setChatHistory((prev) => [...prev, msg])}
          setIsLoading={setIsLoading}
        />
      </div>
    </div>
  );
};

export default Content;
