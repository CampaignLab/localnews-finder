import Articles from "./Articles";
import Search from "./Search";
const Main = () => {
  return (
    <>
      <div className="flex flex-col overflow-y-hidden justify-center items-center">
        <Search />
        <Articles />
      </div>
    </>
  );
};

export default Main;
