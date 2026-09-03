import Image from "next/image";
import Link from "next/link";

export default function Header() {
  return (
    <header className="site-header">
      <Link href="/" className="brand" aria-label="Sol&Cielo">
        <Image src="/logo.svg" alt="Sol&Cielo" width={165} height={43} priority />
      </Link>

      <nav className="main-nav">
        <Link href="/" className="nav-link">
          Inicio
        </Link>
        <Link href="/radicar" className="nav-link">
          Radicar PQRS
        </Link>
        <Link href="/consulta" className="nav-link">
          Consultar estado
        </Link>
      </nav>
    </header>
  );
}
