import Articles from "./Articles";
import Search from "./Search";
const Main = () => {
  return (
    <>
      <div className="flex flex-col overflow-y-hidden justify-center items-center">
        <h1>Local News Finder</h1>
        <div className="divider divider-neutral"></div>

        <Search />
        <Articles />
      </div>
    </>
  );
};

export default Main;
