import UserCard from './UserCard';

const SideBar = () => {
  return (
    <aside className="bg-zinc-900 col-span-2 bg- p-4 text-slate-200 shadow-xl shadow-zinc-800/50 flex flex-col">
      <div className="pt-4 logo flex justify-between items-center">
        <img src="../img/logo.png" className="w-40" alt="Logo"></img>

        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 -960 960 960"
          width="24px"
          fill="#B7B7B7"
        >
          <path d="M440-240 200-480l240-240 56 56-183 184 183 184-56 56Zm264 0L464-480l240-240 56 56-183 184 183 184-56 56Z" />
        </svg>
      </div>

      <div className="mt-10 w-full text-left text-sm text-gray-500 ">Чаты</div>
      <nav className="mt-4 space-y-2 text-sm">
        <button className="w-full text-left p-2 hover:bg-zinc-800 rounded-lg">
          <div className="new-chat flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="20px"
              viewBox="0 -960 960 960"
              width="20px"
              fill="#EFEFEF"
            >
              <path d="M96-96v-696q0-29.7 21.15-50.85Q138.3-864 168-864h624q29.7 0 50.85 21.15Q864-821.7 864-792v480q0 29.7-21.15 50.85Q821.7-240 792-240H240L96-96Zm114-216h582v-480H168v522l42-42Zm-42 0v-480 480Z" />
            </svg>
            <p className="ml-1">Новый чат</p>
          </div>
        </button>
        <button className="w-full text-left p-2 hover:bg-zinc-800 rounded-lg">
          Средний опыт сотрудников
        </button>
        <button className="w-full text-left p-2 hover:bg-zinc-800 rounded-lg">
          Текучесть кадров
        </button>
        <button className="w-full text-left p-2 hover:bg-zinc-800 rounded-lg">
          Количество увольнений...
        </button>
      </nav>

      <UserCard />
    </aside>
  );
};

export default SideBar;
