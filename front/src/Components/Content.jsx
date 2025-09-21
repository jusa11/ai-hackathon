import { useState, useEffect } from 'react';
import axios from 'axios';
import FormQuery from './FormQuery';
import MetricCard from './MetricCard';

const Content = () => {
  const [metrics, setMetrics] = useState([]);
  const [bigMetric, setBigMetric] = useState(null);
  const [llmResponse, setLlmResponse] = useState("Привет!");

  const loadMetrics = async () => {
    try {
      // Обычные метрики
      const res = await axios.get('http://localhost:8000/metric/random');
      setMetrics(res.data);

      // Big-метрика
      const bigRes = await axios.get('http://localhost:8000/metric/big');
      setBigMetric(bigRes.data);
    } catch (error) {
      console.error(`Ошибка при получении метрик: ${error}`);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

	useEffect(()=> {
		console.log(llmResponse);
	}, [])

  return (
    <main className="p-4 flex flex-col h-screen">
      {/* Метрики */}
      <div className="flex-1 flex flex-col gap-4">
        <div className="flex-1 grid grid-cols-3 gap-4">
          {metrics &&
            metrics.map((metric, index) => (
              <MetricCard metric={metric} big={false} key={index} />
            ))}
        </div>

        {bigMetric && (
          <div className="flex-1 mt-6 grid grid-cols-1 rounded-3xl">
            <MetricCard metric={bigMetric[0]} big={true} />
          </div>
        )}
      </div>

      {/* Блок с ответом от LLM */}
      <div className="h-[10%] bg-gray-100 p-4 rounded mt-4 overflow-auto">
        {JSON.stringify(llmResponse, null, 2)}
      </div>

      
      <div className="mx-auto min-w-0 mt-2">
        <FormQuery setLlmResponse={setLlmResponse} />
      </div>
    </main>
  );
};

export default Content;
