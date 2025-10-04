import { useState } from 'react';
import { ToastContainer, Zoom } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Header from './Components/organisms/Header';
import SideBar from './Components/organisms/SideBar';
import Content from './Components/organisms/Content';
import ShareOverlay from './Components/atoms/ShareOverlay';

function App() {
  const [collapsed, setCollapsed] = useState(false);
  const [isShare, setIsShare] = useState(false);
  const [isShowNotifications, setIsShowNotifications] = useState(false);
  const [isChat, setIsChat] = useState(false);
  const [countNotifications, setCountNotifications] = useState(null);

  return (
    <>
      <div
        className={`grid grid-cols-[auto,1fr] min-h-screen font-roboto h-screen  ${
          isShare && 'blur-sm bg-gray-700 shadow-none'
        }`}
      >
        <SideBar
          collapsed={collapsed}
          setCollapsed={setCollapsed}
          isShowNotifications={isShowNotifications}
          setIsShowNotifications={setIsShowNotifications}
          setIsChat={setIsChat}
          countNotifications={countNotifications}
        />

        <div className="flex flex-col h-screen">
          <Header setIsShare={setIsShare} />
          <Content
            isShowNotifications={isShowNotifications}
            setIsShowNotifications={setIsShowNotifications}
            isChat={isChat}
            setIsChat={setIsChat}
            setCountNotifications={setCountNotifications}
          />
        </div>
      </div>
      {isShare && <ShareOverlay setIsShare={setIsShare} />}
      <ToastContainer
        position="top-right"
        autoClose={4000}
        hideProgressBar
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="colored"
        transition={Zoom}
        onClick={() => setIsShowNotifications(true)}
      />
    </>
  );
}

export default App;
