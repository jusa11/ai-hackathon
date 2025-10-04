import { useEffect, useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';

const NotificationsList = ({
  isShowNotifications,
  setIsShowNotifications,
  setCountNotifications,
}) => {
  const [notifications, setIsNotifications] = useState([]);
  const [expanded, setExpanded] = useState({});
  const [isShowNotificationsLoading, setIsNotificationsLoading] =
    useState(true);

  const loadNotifications = async () => {
    try {
      const res = await axios.get(
        'http://server:8000/recommendations/query/'
      );
      const newData = res.data?.recommendations || [];
      console.log(res.data.recommendations.length);
      setCountNotifications(res.data.recommendations.length);
      setIsNotifications(res.data);
      setIsNotificationsLoading(false);

      let i = 0;
      const interval = setInterval(() => {
        const msg = newData[i];
        toast(`${msg.message}`, {
          type:
            msg.level === 'critical'
              ? 'error'
              : msg.level === 'warning'
              ? 'warning'
              : msg.level === 'info'
              ? 'info'
              : 'success',
        });

        i++;
        if (i >= newData.length) clearInterval(interval);
      }, 3000);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      loadNotifications();
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  const toggleExpand = (index) => {
    setExpanded((prev) => ({ ...prev, [index]: !prev[index] }));
  };

  return (
    <div
      className={`${
        isShowNotifications ? 'flex flex-col gap-5' : 'hidden'
      } h-[70vh] overflow-y-auto px-6 pt-6 pb-10 relative scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100`}
    >
      <button
        className="fixed right-[5%] top-[3%] z-40 bg-white p-2 rounded-full shadow hover:bg-gray-100 transition"
        onClick={() => {
          setIsShowNotifications(false);
        }}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="25px"
          viewBox="0 -960 960 960"
          width="25px"
          fill="#434343"
        >
          <path d="m251.33-204.67-46.66-46.66L433.33-480 204.67-708.67l46.66-46.66L480-526.67l228.67-228.66 46.66 46.66L526.67-480l228.66 228.67-46.66 46.66L480-433.33 251.33-204.67Z" />
        </svg>
      </button>

      {isShowNotificationsLoading ? (
        Array.from({ length: 5 }).map((_, i) => (
          <div
            key={i}
            className="bg-gray-200 p-4 shadow-md rounded-3xl border border-gray-300 animate-pulse"
          >
            <div className="h-5 animate-pulse"></div>
          </div>
        ))
      ) : notifications.recommendations?.length > 0 ? (
        notifications.recommendations.map((msg, index) => {
          const colors =
            msg.level === 'critical'
              ? 'border-red-300 bg-red-50/60'
              : msg.level === 'warning'
              ? 'border-yellow-300 bg-yellow-50/60'
              : msg.level === 'info'
              ? 'border-blue-300 bg-blue-50/60'
              : 'border-green-300 bg-green-50/60';

          return (
            <div
              key={index}
              className={`flex items-start gap-4 p-5 rounded-2xl shadow-sm border ${colors} transition-all duration-300 hover:shadow-md hover:translate-y-[-2px]`}
            >
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-white font-bold text-lg shadow-md">
                  🤖
                </div>
              </div>

              <div className="flex flex-col flex-1">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-sm font-semibold text-gray-900">
                    HR Bot
                  </span>
                  <span className="text-xs px-2 py-0.5 rounded-full bg-white/70 border text-gray-700">
                    {msg.level === 'critical'
                      ? 'Критично'
                      : msg.level === 'warning'
                      ? 'Предупреждение'
                      : msg.level === 'info'
                      ? 'Инфо'
                      : 'Успех'}
                  </span>
                </div>

                <h4 className="text-base font-semibold text-gray-900 mb-1">
                  {msg.message}
                </h4>

                <p
                  className={`text-sm text-gray-700 leading-relaxed transition-all ${
                    expanded[index] ? '' : 'line-clamp-1'
                  }`}
                >
                  {msg.comment}
                </p>

                {msg.comment?.length > 80 && (
                  <button
                    onClick={() => toggleExpand(index)}
                    className="mt-2 inline-flex items-center gap-1 text-indigo-600 text-sm font-semibold hover:text-indigo-800 transition-colors duration-200"
                  >
                    <span>{expanded[index] ? 'Скрыть' : 'Подробнее'}</span>
                    <span
                      className={`inline-block w-2 h-2 border-r-2 border-b-2 border-indigo-600 transform transition-transform duration-200 ${
                        expanded[index] ? 'rotate-45' : 'rotate-135'
                      }`}
                    ></span>
                  </button>
                )}
              </div>
            </div>
          );
        })
      ) : (
        <div className="text-center text-gray-500 py-10 italic">
          Уведомлений пока нет
        </div>
      )}
    </div>
  );
};

export default NotificationsList;
