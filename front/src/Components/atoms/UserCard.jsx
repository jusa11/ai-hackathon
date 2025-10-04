import NotificationsIcon from './NotificationsIcon';

const UserCard = ({
  collapsed,
  isShowNotifications,
  setIsShowNotifications,
  setIsChat,
  countNotifications,
}) => {
  return (
    <div
      className={`mt-auto border-t border-zinc-700 flex items-center justify-between ${
        collapsed ? 'p-1' : 'p-2'
      }`}
    >
      <div className="flex items-center gap-3">
        <div className="p-[2px] rounded-full bg-gradient-to-r from-blue-500 via-purple-500 to-red-500">
          <img
            className="w-[40px] rounded-full  bg-zinc-900"
            src="../img/user-logo.png"
            alt="user-logo"
          />
        </div>

        {!collapsed && (
          <div className="flex flex-col">
            <span className="text-sm font-medium text-slate-200">Танос </span>
            <span className="mt-1 text-xs text-slate-400">HR Analyst</span>
          </div>
        )}
      </div>

      {!collapsed && (
        <div className="flex gap-1">
          <button
            className="hover:bg-zinc-800 rounded-lg"
            onClick={() => {
              setIsChat(false);
              isShowNotifications
                ? setIsShowNotifications(false)
                : setIsShowNotifications(true);
            }}
          >
            <NotificationsIcon count={countNotifications} />
          </button>

          <button className="hover:bg-zinc-800 rounded-lg">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="24px"
              viewBox="0 -960 960 960"
              width="24px"
              fill="#EFEFEF"
            >
              <path d="m370-80-16-128q-13-5-24.5-12T307-235l-119 50L78-375l103-78q-1-7-1-13.5v-27q0-6.5 1-13.5L78-585l110-190 119 50q11-8 23-15t24-12l16-128h220l16 128q13 5 24.5 12t22.5 15l119-50 110 190-103 78q1 7 1 13.5v27q0 6.5-2 13.5l103 78-110 190-118-50q-11 8-23 15t-24 12L590-80H370Zm70-80h79l14-106q31-8 57.5-23.5T639-327l99 41 39-68-86-65q5-14 7-29.5t2-31.5q0-16-2-31.5t-7-29.5l86-65-39-68-99 42q-22-23-48.5-38.5T533-694l-13-106h-79l-14 106q-31 8-57.5 23.5T321-633l-99-41-39 68 86 64q-5 15-7 30t-2 32q0 16 2 31t7 30l-86 65 39 68 99-42q22 23 48.5 38.5T427-266l13 106Zm42-180q58 0 99-41t41-99q0-58-41-99t-99-41q-59 0-99.5 41T342-480q0 58 40.5 99t99.5 41Zm-2-140Z" />
            </svg>
          </button>
          <button className="p-1 hover:bg-zinc-800 rounded-lg">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              height="24px"
              viewBox="0 -960 960 960"
              width="24px"
              fill="#EFEFEF"
            >
              <path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h280v80H200v560h280v80H200Zm440-160-55-58 102-102H360v-80h327L585-622l55-58 200 200-200 200Z" />
            </svg>
          </button>
        </div>
      )}
    </div>
  );
};

export default UserCard;
