import { useState, useEffect } from 'react';
import axios from 'axios';
import FormQuery from './FormQuery';
import MetricCard from './MetricCard';

const Content = () => {
  const [metrics, setmertrics] = useState([]);

  const loadMetrics = async () => {
    try {
      const res = await axios.get('http://localhost:8000/metric/random');
      const metric = res.data;
      setmertrics(metric);
    } catch (error) {
      console.error(`Произошла ошибка при получении метрики - ${error}`);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  useEffect(() => {
    console.log(metrics);
  }, [metrics]);

  return (
    <main className="p-4 flex flex-col h-full">
      {/* Блоки метрик в grid */}
      <div className="flex-1">
        <div className="grid grid-cols-3 gap-4 ">
          {metrics &&
            metrics.map((metric, index) => {
              return <MetricCard metric={metric} key={index} />;
            })}
        </div>
        <div className="mt-4 rounded-3xl  grid grid-cols-1">
          <div className="border border-gray-300">{
						<MetricCard metric={metrics[1]}/>}</div>
        </div>
      </div>

      <div className="mx-auto min-w-0">
        <FormQuery />
      </div>
    </main>
  );
};

export default Content;
