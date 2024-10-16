import Image from "next/image";

const Navbar = () => {
  return (
    <div className="navbar">
      <a className="btn">
        <Image src="/icons/news.svg" height={40} width={40} alt="news icon" />
      </a>
    </div>
  );
};

export default Navbar;
