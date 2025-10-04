import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ShareOverlay = ({ setIsShare }) => {
  const handleCopy = () => {
    const link = 'https://example.com/share-link';
    navigator.clipboard.writeText(link).then(() => {
      toast.info('Ссылка скопирована');
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white w-[600px] max-w-[90%] p-6 rounded-3xl shadow-lg relative">
        <button
          className="absolute top-4 right-4 p-1 hover:bg-gray-200 rounded-full"
          onClick={() => setIsShare(false)}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 0 24 24"
            width="24px"
            fill="#434343"
          >
            <path d="M18.3 5.71a1 1 0 0 0-1.42 0L12 10.59 7.12 5.7a1 1 0 0 0-1.41 1.42L10.59 12l-4.88 4.88a1 1 0 1 0 1.41 1.42L12 13.41l4.88 4.88a1 1 0 0 0 1.42-1.42L13.41 12l4.88-4.88a1 1 0 0 0 0-1.41z" />
          </svg>
        </button>

        <h2 className="text-xl font-semibold mb-4 text-gray-800">
          Поделиться ссылкой
        </h2>

        <div className="flex items-center justify-between bg-gray-100 p-3 rounded-xl">
          <span className="text-gray-700 truncate">
            https://example.com/share-link
          </span>
          <button
            className="ml-4 px-4 py-2 bg-blue-500 text-white rounded-xl hover:bg-blue-600"
            onClick={handleCopy}
          >
            Копировать
          </button>
        </div>
      </div>
    </div>
  );
};

export default ShareOverlay;
