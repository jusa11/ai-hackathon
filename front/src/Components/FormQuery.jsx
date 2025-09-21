import { useEffect, useState } from 'react';
import AutoResizeTextarea from './AutoResizeTextArea';
import axios from 'axios';

const FormQuery = ({ setLlmResponse }) => {
  const [query, setQuery] = useState('');

  const handleSend = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      const res = await axios.post('http://localhost:8000/llm/query', {
        user_query: query,
      });
      setLlmResponse(res.data); 
    } catch (error) {
      console.error(error);
      setLlmResponse({ error: 'Ошибка при запросе к LLM' });
    }

    setQuery('');
  };

  useEffect(() => {
    console.log(query);
  }, [query]);

  return (
    <div className="relative w-[800px]">
      <form onSubmit={handleSend}>
        <AutoResizeTextarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          type="submit"
          className="absolute right-2 bottom-3 
                     bg-blue-500 hover:bg-blue-600 text-white 
                     w-10 h-10 rounded-full shadow-md flex items-center justify-center"
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
