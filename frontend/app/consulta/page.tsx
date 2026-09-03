"use client";

import Header from "@/components/Header";
import { getTicket, Ticket } from "@/lib/api";
import { useSearchParams } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";

const statusOrder = ["NUEVO", "EN_REVISION", "RESUELTO", "CERRADO"];

const statusLabels: Record<string, string> = {
  NUEVO: "Nuevo",
  EN_REVISION: "En revisión",
  RESUELTO: "Resuelto",
  CERRADO: "Cerrado",
};

function statusIndex(status: string) {
  return statusOrder.indexOf(status);
}

export default function ConsultaPage() {
  const params = useSearchParams();
  const initialTicket = params.get("ticket") ?? "";

  const [code, setCode] = useState(initialTicket);
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const consult = async (value: string) => {
    if (!value.trim()) {
      setError("Ingresa un número de radicado.");
      return;
    }

    setLoading(true);
    setError("");
    setTicket(null);

    try {
      setTicket(await getTicket(value));
    } catch (err) {
      setError(err instanceof Error ? err.message : "No fue posible consultar el estado.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (initialTicket) {
      void consult(initialTicket);
    }
  }, [initialTicket]);

  const submit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    void consult(code);
  };

  const currentIndex = ticket ? statusIndex(ticket.status) : -1;

  return (
    <>
      <Header />
      <main className="consult-page">
        <section className="consult-card">
          <div className="form-heading">
            <h1>Consultar estado</h1>
            <p>Ingresa el número de radicado de tu PQRS.</p>
          </div>

          <form onSubmit={submit} className="search-row">
            <input
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Ej. PQRS-1001"
              aria-label="Número de radicado"
            />
            <button className="btn btn-primary" type="submit" disabled={loading}>
              {loading ? "Consultando..." : "Consultar"}
            </button>
          </form>

          {error && <div className="error-box">{error}</div>}

          {ticket && (
            <section className="result-card">
              <div className="result-head">
                <h2>{ticket.ticket_code}</h2>
                <span className={`status status-${ticket.status}`}>
                  {statusLabels[ticket.status] ?? ticket.status}
                </span>
              </div>

              <div className="steps">
                {statusOrder.map((status, index) => (
                  <div
                    className={`step ${index <= currentIndex ? "active" : ""}`}
                    key={status}
                  >
                    <div className="step-dot" />
                    <span>{statusLabels[status]}</span>
                  </div>
                ))}
              </div>

              <div className="result-info">
                <div>
                  <small>Asunto</small>
                  <strong>{ticket.subject}</strong>
                </div>
                <div>
                  <small>Fecha de radicación</small>
                  <strong>
                    {new Date(ticket.created_at).toLocaleString("es-CO", {
                      dateStyle: "short",
                      timeStyle: "short",
                    })}
                  </strong>
                </div>
                <div>
                  <small>Categoría</small>
                  <strong>{ticket.category}</strong>
                </div>
                <div>
                  <small>Solicitante</small>
                  <strong>{ticket.applicant_name}</strong>
                </div>
              </div>
            </section>
          )}
        </section>
      </main>
    </>
  );
}
