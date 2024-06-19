import Search from "./Search";
const Main = () => {
  return (
    <>
      <div className="flex flex-col justify-center items-center">
        <h1>Local News Finder</h1>
        <div className="divider divider-neutral"></div>

        <Search />
      </div>
    </>
  );
};

export default Main;
