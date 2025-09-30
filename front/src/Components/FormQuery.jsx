import { useState } from 'react';
import AutoResizeTextarea from './AutoResizeTextArea';
import axios from 'axios';

const FormQuery = ({ addMessage, setIsLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setQuery('');
    if (!query.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: query,
      metricResult: null,
      isLoading: true,
    };
    addMessage(userMessage);

    setIsLoading(true);

    try {
      const res = await axios.post('http://localhost:8000/llm/query', {
        user_query: query,
      });

      // const res = await axios.get('http://localhost:8000/metric/random');
      console.log(res.data);
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: res.data.result_text,
        result: res.data.result,
        type_chart: res.data.type_chart,
        hasPlot: res.data.has_plot,
        isLoading: false,
      };
      addMessage(botMessage);
      setIsLoading(false);
    } catch (error) {
      console.error(error);
      setIsLoading(false);
      addMessage({
        id: Date.now() + 2,
        type: 'bot',
        text: 'Что-то сломалось 💥, попробуйте повторить позже или задать вопрос по-другому',
        metricResult: null,
        chartData: null,
        isLoading: false,
      });
    }
  };

  return (
    <div className="relative w-[800px]">
      <form onSubmit={handleSubmit}>
        <AutoResizeTextarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          handleSubmit={handleSubmit}
          setQuery={setQuery}
        />
        <button
          type="submit"
          className="absolute right-2 bottom-3 bg-blue-500 hover:bg-blue-600 text-white w-10 h-10 rounded-full flex items-center justify-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 -960 960 960"
            width="24px"
            fill="#EFEFEF"
          >
            <path d="M440-160v-487L216-423l-56-57 320-320 320 320-56 57-224-224v487h-80Z" />
          </svg>
        </button>
      </form>
    </div>
  );
};

export default FormQuery;
