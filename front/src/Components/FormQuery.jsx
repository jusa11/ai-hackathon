import { useState } from 'react';
import AutoResizeTextarea from './AutoResizeTextArea';

const FormQuery = () => {
  const [query, setQuery] = useState('');
  const [chatVisible, setChatVisible] = useState(false);

  const handleSend = () => {
    setChatVisible(true);
  };

  return (
    <>
      <div className="relative w-[800px]">
        <form action="">
          <AutoResizeTextarea />
          <button
            onClick={handleSend}
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

      {/* Overlay с перепиской */}
      {chatVisible && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-6 rounded shadow-2xl w-3/4 h-3/4 overflow-auto border border-gray-300">
            <h2 className="text-lg font-bold mb-4">Переписка с ботом</h2>
            {/* Здесь будут сообщения бота */}
          </div>
        </div>
      )}
    </>
  );
};

export default FormQuery;
