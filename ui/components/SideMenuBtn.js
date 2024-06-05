import { FiChevronRight, FiChevronLeft } from "react-icons/fi";

export function SideMenuBtn(props) {
    return (<button onClick={props.toggleMenu} className='side-menu-btn'>
        {props.showMenu ? <FiChevronLeft size={24} /> : <FiChevronRight size={24} />}
    </button>);
}
