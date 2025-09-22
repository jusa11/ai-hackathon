import MetricChart from './MetricChart';

const ChatWithLLM = ({ chatHistory, isChat, setIsChat }) => {
	console.log(chatHistory);
  return (
    <div className={`${isChat ? 'mt-4 flex flex-col gap-2' : 'hidden'} px-4 pb-48`}>
      <button className="fixed left-[93%] top-[3%] z-40" onClick={() => setIsChat(false)}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="40px"
          viewBox="0 -960 960 960"
          width="40px"
          fill="#434343"
        >
          <path d="m251.33-204.67-46.66-46.66L433.33-480 204.67-708.67l46.66-46.66L480-526.67l228.67-228.66 46.66 46.66L526.67-480l228.66 228.67-46.66 46.66L480-433.33 251.33-204.67Z" />
        </svg>
      </button>
      {chatHistory.map((msg) => (
        <div
          key={msg.id}
          className={`${msg.type === 'user' ? 'text-right' : 'text-left'}`}
        >
          <div
            className={`inline-block p-2 rounded-2xl max-w-[1000px] ${
              msg.type === 'user' ? 'bg-blue-200' : 'bg-blue-50'
            }`}
          >
            <p>{msg.text}</p>
            {msg.result && msg.hasPlot && (
              <div className="h-[200px] mt-2">
                <MetricChart data={msg} big={false} />
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ChatWithLLM;
