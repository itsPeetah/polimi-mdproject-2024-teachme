import Image from "next/image";
import { HeadingXL } from "@/components/Headings";
import { useRouter } from "next/router";
import { deleteCookie } from 'cookies-next';

export function SideMenu(props) {
    const router = useRouter();
    // Logout
    const logout = () => {
        deleteCookie('id');
        deleteCookie('role');
        deleteCookie('email');
        router.push('/auth/login');
    };
    return (
        <div
            className={
                'side-menu animate__animated ' +
                (
                    props.showMenu
                        ? "animate__slideInLeft fixed lg:sticky"
                        : "animate__slideOutLeft fixed"
                )
            }
        >
            <HeadingXL text={"Profile"} />
            <Image src="/img/profile.jpg" alt="Profile" width={100} height={100} className="rounded-full" />
            <h2 className="my-8 text-xl font-bold">
                {props.name}
            </h2>
            <button className="w-52 py-4 my-2 mt-auto text-white bg-rose-800 rounded-xl hover:bg-rose-700 transition-all" onClick={logout}>
                Logout
            </button>
        </div>
    );
}
