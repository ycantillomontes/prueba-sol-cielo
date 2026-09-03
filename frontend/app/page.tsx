import Header from "@/components/Header";
import Link from "next/link";

export default function Home() {
  return (
    <>
      <Header />
      <main className="page-shell">
        <section className="hero">
          <div className="hero-copy">
            <h1 className="hero-title">
              Radicar
              <br />
              <span>PQRS</span>
            </h1>
            <p className="hero-text">
              Sistema de Peticiones, Quejas, Reclamos y Sugerencias.
            </p>

            <div className="actions">
              <Link href="/radicar" className="btn btn-primary">
                Radicar PQRS
              </Link>
              <Link href="/consulta" className="btn btn-outline">
                Consultar estado
              </Link>
            </div>
          </div>

          <div className="hero-art" aria-hidden="true">
            <div className="art-shape" />
            <div className="sun-art" />
            <div className="solar-field">
              {Array.from({ length: 18 }).map((_, index) => (
                <i key={index} />
              ))}
            </div>
            <div className="leaves" />
          </div>
        </section>
      </main>
    </>
  );
}
