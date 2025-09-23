import { useState } from 'react';
import Header from './Components/Header';
import SideBar from './Components/SideBar';
import Content from './Components/Content';
import ShareOverlay from './Components/ShareOverlay';

function App() {
  const [collapsed, setCollapsed] = useState(false);
  const [isShare, setIsShare] = useState(false);

  return (
    <>
      <div
        className={`grid grid-cols-[auto,1fr] min-h-screen font-roboto h-screen  ${
          isShare && 'blur-sm bg-gray-700 shadow-none'
        }`}
      >
        <SideBar collapsed={collapsed} setCollapsed={setCollapsed} />

        <div className="flex flex-col h-screen">
          <Header setIsShare={setIsShare} />
          <Content />
        </div>
      </div>
      {isShare && <ShareOverlay setIsShare={setIsShare} />}
    </>
  );
}

export default App;
