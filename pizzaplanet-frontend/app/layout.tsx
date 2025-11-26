

import "./globals.css";

import Header from "@/components/header";
export const metadata = {
  title: "Pizzaria",
  description: "Sistema de cardápio e pedidos",

};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-br">
      <body className="bg-neutral-100 min-h-screen">
        <Header />
        <main>{children}</main>
      </body>
    </html>
  );
}