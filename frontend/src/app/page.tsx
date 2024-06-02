import Main from "./components/Main";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
export default function Home() {
  return (
    <div className="h-screen flex flex-col">
      <Navbar />
      <div className="flex flex-grow overflow-y-auto">
        <main className="flex-grow pl-20 pr-20">
          <Main />
        </main>
      </div>
      <Footer />
    </div>
  );
}
