import Link from "next/link";
import Image from "next/image";
import { useState } from "react";
import "animate.css";
import getData from "@/services/getData";
import { HeadingL, HeadingXL } from "@/components/headings";
import {
  FiChevronRight,
  FiChevronLeft,
  FiPlusSquare,
  FiUserPlus,
} from "react-icons/fi";

export async function getStaticProps() {
  const data = await getData();
  return { props: { data } };
}
export default function TeacherPage({ data }) {
  // Side-Menu Handler
  const [showMenu, setShowMenu] = useState(true);
  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };
  return (
    <div className="flex min-h-screen w-full flex-col bg-art md:flex-row">
      {/* Toggle Side-Menu Button*/}
      <button
        onClick={toggleMenu}
        className='sticky top-0 z-50 h-screen bg-slate-900/40 p-4 text-white backdrop-blur-lg'
      >
        {showMenu ? <FiChevronLeft size={24} /> : <FiChevronRight size={24} />}
      </button>
      {/* Side-Menu */}
      {/* Personal Settings */}
      <div
        className={`
                    animate__animated flex h-screen w-3/12 flex-col items-center 
                    overflow-y-scroll border-l-2 
                    border-slate-800 bg-slate-900/40
                    p-6
                    backdrop-blur-lg transition-all duration-300 
                    ease-linear
                    ${showMenu
          ? "animate__slideInLeft absolute top-0 left-0 lg:sticky"
            : "animate__slideOutLeft absolute"
          }`}
      >
        <HeadingXL text={"Profile"} />
        <Image
          src="/img/profile.jpg"
          alt="Profile"
          width={100}
          height={100}
          className="rounded-full"
        />
        <h2 className="my-8 text-xl font-bold">Name</h2>
      </div>
      {/* Dashboard */}
      <div className="flex flex-1 flex-col items-center overflow-y-scroll border-r-2 border-slate-900 px-20 py-6">
        <HeadingXL text={"Teacher Dashboard"} />
        {/* Materials Section */}
        <section className="my-10">
          <HeadingL text={"Materials"} />
          <ul className="flex flex-row flex-wrap items-center justify-center gap-5">
            {Object.keys(data).map((item, index) => (
              <li key={index}>
                <Link
                  href={"/teacher/" + item}
                  className="flex h-28 w-56 items-center justify-center rounded-2xl border-black bg-slate-900/70 text-center backdrop-blur"
                >
                  {item}
                </Link>
              </li>
            ))}
            <li>
              <Link
                href={"/teacher/create"}
                className="flex h-28 w-56 items-center justify-center rounded-2xl bg-slate-900/40 text-center backdrop-blur"
              >
                <FiPlusSquare size={32} />
              </Link>
            </li>
            {/* <li className="h-28 w-56" /> */}
            {/* <li className="h-28 w-56" /> */}
            {/* <li className="h-28 w-56" /> */}
          </ul>
        </section>
        {/* Students Section */}
        <section className="my-10">
          <HeadingL text={"Students"} />
          <ul className="flex flex-row flex-wrap items-center justify-center gap-5">
            {/* Add Student Button */}
            <li>
              <Link
                href={"/teacher/"}
                className="mb-4 flex h-24 w-24 items-center justify-center rounded-full bg-slate-900/40 text-center backdrop-blur"
              >
                <FiUserPlus size={28} />
              </Link>
            </li>
          </ul>
        </section>
      </div>
    </div>
  );
}
