import UserCard from './Profile/UserCard';

const SideBar = ({
  collapsed,
  setCollapsed,
  isShowNotifications,
  setIsShowNotifications,
  setIsChat,
  countNotifications,
}) => {
  const chats = [
    'Новый чат',
    'Средний опыт сотрудников',
    'Текучесть кадров',
    'Количество увольнений...',
  ];

  return (
    <aside
      className={`bg-zinc-900 text-slate-200 shadow-xl shadow-zinc-800/50 flex flex-col transition-all duration-300
      ${collapsed ? 'w-16 p-2 items-center' : 'w-64 p-4'}`}
    >
      {/* Лого и кнопка */}
      <div
        className={`pt-4 logo flex ${
          collapsed ? 'flex-col gap-3 ' : 'justify-between'
        }`}
      >
        {collapsed ? (
          <img src="../img/logo-collapsed.png" className="w-7" alt="Logo" />
        ) : (
          <img src="../img/logo.png" className="w-40" alt="Logo" />
        )}

        <button
          onClick={() => setCollapsed(!collapsed)}
          className="hover:bg-zinc-800 rounded-lg"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 -960 960 960"
            width="24px"
            fill="#B7B7B7"
            className={`transition-transform duration-300 ${
              collapsed ? 'rotate-180' : ''
            }`}
          >
            <path d="M440-240 200-480l240-240 56 56-183 184 183 184-56 56Zm264 0L464-480l240-240 56 56-183 184 183 184-56 56Z" />
          </svg>
        </button>
      </div>

      <div
        className={`mt-10 w-full text-sm text-gray-500 ${
          collapsed && 'hidden'
        }`}
      >
        {collapsed ? 'Ч' : 'Чаты'}
      </div>

      <nav className="mt-4 space-y-2 text-sm">
        {chats.map((chat, idx) => (
          <div key={idx} className="relative group">
            <button className="p-2 hover:bg-zinc-800 rounded-lg w-full text-left">
              {collapsed ? (
                <span className="text-lg font-bold">{chat[0]}</span>
              ) : (
                chat
              )}
            </button>

            {collapsed && (
              <span
                className="absolute left-full top-1/2 -translate-y-1/2 ml-2 whitespace-nowrap 
                bg-zinc-800 text-slate-200 text-xs px-2 py-1 rounded-md opacity-0 group-hover:opacity-100 
                transition-opacity duration-200 pointer-events-none z-50"
              >
                {chat}
              </span>
            )}
          </div>
        ))}
      </nav>

      <UserCard
        collapsed={collapsed}
        isShowNotifications={isShowNotifications}
        setIsShowNotifications={setIsShowNotifications}
        setIsChat={setIsChat}
        countNotifications={countNotifications}
      />
    </aside>
  );
};

export default SideBar;
