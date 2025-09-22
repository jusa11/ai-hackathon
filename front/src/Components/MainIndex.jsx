// MainIndex.jsx
import Header from './Header';
import SideBar from './SideBar';
import Content from './Content';

const MainIndex = () => {
  return (
    <div className="grid grid-cols-12 min-h-screen font-roboto h-screen">
      <SideBar className="col-span-2" />
      <div className="col-span-10 flex flex-col h-screen">
        <Header />
        <Content />
      </div>
    </div>
  );
};

export default MainIndex;
