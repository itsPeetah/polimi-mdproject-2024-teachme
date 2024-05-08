export function SideMenuBtn({ text, action }) {
    return (
        <button
            onClick={action}
            className='bg-violet-700 hover:bg-violet-600 text-white font-bold text-sm text-center w-full h-16 rounded transition duration-300 ease-in-out'
        >
            {text}
        </button>
    )
}