export default function Home() {
  return (
    <div className="min-h-screen bg-gray-950 p-[clamp(20px,2vw,80px)]">

      <div className="w-full bg-gray-1050 shadow-2xl shadow-green-500/40 rounded-lg 
      p-[clamp(40px,4vw,100px)] flex min-h-[calc(100vh-200px)]">

        <div className="w-1/2 pr-[clamp(20px,3vw,60px)]">
          <h2 className="text-[clamp(32px,3vw,56px)] font-extrabold tracking-wider text-white">
            Bem-vindo ao
            <b className="ml-2 text-green-400 animate-pulse">Pizza Planet!</b>
          </h2>

          <p className="text-[clamp(20px,1.8vw,32px)] font-semibold text-green-400 mb-6 tracking-wide">
            Sistema Interno de Pedidos e Gestão
          </p>

          <p className="text-gray-300 text-[clamp(16px,1.2vw,22px)] leading-relaxed mb-8 tracking-wide">
            Aqui você tem acesso rápido a todas as ferramentas necessárias para garantir que
            a melhor pizza da galáxia chegue ao nosso cliente.
          </p>

          <div className="flex gap-4 mt-10">
            <a
              href="/cardapio"
              className="bg-green-500 hover:bg-green-600 transition-all 
    px-8 py-3 rounded-md font-semibold text-gray-900 
    text-lg shadow-lg shadow-green-500/40"
            >
              Abrir Cardápio
            </a>

            <a
              href="/pedido"
              className="bg-gray-800 border border-green-500 hover:bg-gray-700 transition-all 
    px-8 py-3 rounded-md font-semibold text-green-400 
    text-lg shadow-lg shadow-green-500/20"
            >
              Fazer Pedido
            </a>
          </div>
        </div>

        <div className="w-1/2 flex items-center justify-center rounded-md overflow-hidden p-6">
          <div className="shadow-xl shadow-green-500/40 rounded-md max-h-[600px]">
            <img
              src="/astronauta.png"
              alt="Pizza"
              className="object-contain w-full h-full rounded-md"
            />
          </div>
        </div>

      </div>
    </div>
  );
}