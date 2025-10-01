import { useRef, useEffect } from 'react';
import MetricChart from './MetricChart';

const ChatWithLLM = ({
  chatHistory,
  isChat,
  setIsChat,
  isLoading,
}) => {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  return (
    <div
      className={`${
        isChat ? 'flex flex-col gap-3' : 'hidden'
      } h-[70vh] overflow-y-auto px-4 pt-4 pb-4 relative scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100`}
    >
      <button
        className="fixed right-[5%] top-[3%] z-40 bg-white p-2 rounded-full shadow hover:bg-gray-100 transition"
        onClick={() => {
          setIsChat(false);
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="25px"
          viewBox="0 -960 960 960"
          width="25px"
          fill="#434343"
        >
          {' '}
          <path d="m251.33-204.67-46.66-46.66L433.33-480 204.67-708.67l46.66-46.66L480-526.67l228.67-228.66 46.66 46.66L526.67-480l228.66 228.67-46.66 46.66L480-433.33 251.33-204.67Z" />{' '}
        </svg>
      </button>

      {chatHistory.map((msg) => (
        <div
          key={msg.id}
          className={`flex items-start gap-2 ${
            msg.type === 'user' ? 'justify-end' : 'justify-start'
          }`}
        >
          {msg.type !== 'user' && (
            <div className="w-7 h-7 flex items-center justify-center rounded-full bg-blue-500 text-white text-sm">
              🤖
            </div>
          )}

          <div
            className={`p-2 rounded-xl max-w-[80%] text-base leading-relaxed shadow-sm ${
              msg.type === 'user'
                ? 'bg-blue-600 text-white rounded-br-none'
                : 'bg-gray-100 text-gray-900 rounded-bl-none'
            }`}
          >
            <p>{msg.text}</p>

            {msg.result && msg.hasPlot && (
              <div className="h-[200px] mt-2 rounded-lg overflow-hidden border border-gray-200 bg-white">
                <MetricChart data={msg} big={false} />
              </div>
            )}
          </div>

          {msg.type === 'user' && (
            <div className="w-7 h-7 flex items-center justify-center rounded-full bg-gray-300 text-gray-700 text-sm">
              <img src="../img/user-logo.png" />
            </div>
          )}
        </div>
      ))}
      {isLoading && (
        <div className="flex gap-1 ml-7">
          <span className="animate-bounce">.</span>
          <span className="animate-bounce delay-150">.</span>
          <span className="animate-bounce delay-300">.</span>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatWithLLM;
