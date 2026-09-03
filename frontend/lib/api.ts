const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000/api/pqrs";

export type TicketAttachment = {
  id: number;
  original_name: string;
  file: string;
  uploaded_at: string;
};

export type Ticket = {
  ticket_code: string;
  applicant_name: string;
  applicant_email: string;
  category: string;
  subject: string;
  description: string;
  status: string;
  created_at: string;
  attachments: TicketAttachment[];
};

export type JsonAttachment = {
  name: string;
  content: string;
};

export type CreateTicketPayload = Omit<
  Ticket,
  "ticket_code" | "status" | "created_at" | "attachments"
> & {
  attachments?: JsonAttachment[];
};

export async function createTicket(payload: CreateTicketPayload) {
  const response = await fetch(`${API_URL}/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    const error = Object.values(data).flat().join(" ");
    throw new Error(error || "No fue posible radicar la PQRS.");
  }

  return data as Ticket;
}

export async function getTicket(ticketCode: string) {
  const response = await fetch(
    `${API_URL}/${encodeURIComponent(ticketCode.trim())}/`,
    { cache: "no-store" },
  );

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("No encontramos una PQRS con ese número de radicado.");
    }
    throw new Error("No fue posible consultar el estado.");
  }

  return (await response.json()) as Ticket;
}
