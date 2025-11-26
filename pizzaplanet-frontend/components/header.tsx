import Link from "next/link";

export default function Header() {
    return (
        <header className="w-full py-7 px-12 bg-gray-950 text-white flex items-center justify-around shadow-lg shadow-green-500/20">
            <h1 className="font-bold text-2xl tracking-wide text-green-400">Pizza Planet</h1>
            <nav className="flex gap-4">
                <Link href="/"
                    className="font-medium border border-transparent hover:text-green-400 hover:border-green-400 transition duration-300 py-2 px-5 rounded-md active:bg-green-400 active:text-gray-950">
                    Home
                </Link>
                <Link href="/cardapio"
                    className="font-medium border border-transparent hover:text-green-400 hover:border-green-400 transition duration-300 py-2 px-5 rounded-md active:bg-green-400 active:text-gray-950">
                    Cardápio
                </Link>
                <Link href="/pedido"
                    className="font-medium border border-transparent hover:text-green-400 hover:border-green-400 transition duration-300 py-2 px-5 rounded-md active:bg-green-400 active:text-gray-950">
                    Pedido
                </Link>
            </nav>
        </header>
    );
}