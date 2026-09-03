"use client";

import Header from "@/components/Header";
import { createTicket } from "@/lib/api";
import { ChangeEvent, FormEvent, useRef, useState } from "react";

const categories = [
  ["PETICION", "Petición"],
  ["QUEJA", "Queja"],
  ["RECLAMO", "Reclamo"],
  ["SUGERENCIA", "Sugerencia"],
];

const MAX_FILES = 5;
const MAX_FILE_SIZE = 5 * 1024 * 1024;

export default function RadicarPage() {
  const [form, setForm] = useState({
    applicant_name: "",
    applicant_email: "",
    category: "PETICION",
    subject: "",
    description: "",
  });

  const [files, setFiles] = useState<File[]>([]);
  const [ticketCode, setTicketCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFiles = (event: ChangeEvent<HTMLInputElement>) => {
    const selected = Array.from(event.target.files ?? []);

    if (selected.length === 0) {
      return;
    }

    setError("");

    // Verificar cantidad total
    if (files.length + selected.length > MAX_FILES) {
      setError(`Puedes adjuntar máximo ${MAX_FILES} archivos PDF.`);
      event.target.value = "";
      return;
    }

    // Verificar formato
    const invalidFile = selected.find(
      (file) => !file.name.toLowerCase().endsWith(".pdf"),
    );

    if (invalidFile) {
      setError(`El archivo "${invalidFile.name}" no es un PDF.`);
      event.target.value = "";
      return;
    }

    // Verificar tamaño
    const largeFile = selected.find(
      (file) => file.size > MAX_FILE_SIZE,
    );

    if (largeFile) {
      setError(
        `El archivo "${largeFile.name}" supera el límite de 5 MB.`,
      );
      event.target.value = "";
      return;
    }

    // Evitar archivos repetidos
    const newFiles = selected.filter(
      (newFile) =>
        !files.some(
          (existingFile) =>
            existingFile.name === newFile.name &&
            existingFile.size === newFile.size &&
            existingFile.lastModified === newFile.lastModified,
        ),
    );

    if (newFiles.length === 0) {
      setError("Los archivos seleccionados ya fueron agregados.");
      event.target.value = "";
      return;
    }

    if (files.length + newFiles.length > MAX_FILES) {
      setError(`Puedes adjuntar máximo ${MAX_FILES} archivos PDF.`);
      event.target.value = "";
      return;
    }

    setFiles((currentFiles) => [...currentFiles, ...newFiles]);

    // Permite volver a seleccionar el mismo archivo si se elimina
    event.target.value = "";
  };

  const removeFile = (index: number) => {
    setFiles((currentFiles) =>
      currentFiles.filter((_, fileIndex) => fileIndex !== index),
    );

    setError("");
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setLoading(true);
    setError("");
    setTicketCode("");

    try {
      const attachments = await Promise.all(
        files.map(
          (file) =>
            new Promise<{ name: string; content: string }>(
              (resolve, reject) => {
                const reader = new FileReader();

                reader.onload = () => {
                  resolve({
                    name: file.name,
                    content: String(reader.result),
                  });
                };

                reader.onerror = () => {
                  reject(
                    new Error(`No fue posible leer ${file.name}.`),
                  );
                };

                reader.readAsDataURL(file);
              },
            ),
        ),
      );

      const ticket = await createTicket({
        ...form,
        attachments,
      });

      setTicketCode(ticket.ticket_code);

      setForm({
        applicant_name: "",
        applicant_email: "",
        category: "PETICION",
        subject: "",
        description: "",
      });

      setFiles([]);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "No fue posible radicar la PQRS.",
      );
    } finally {
      setLoading(false);
    }
  };

  if (ticketCode) {
    return (
      <>
        <Header />

        <main className="form-page">
          <section className="form-card success-card">
            <div className="success-icon">✓</div>

            <h1>Solicitud radicada correctamente</h1>

            <p
              className="hero-text"
              style={{ margin: "8px auto" }}
            >
              Tu solicitud ha sido registrada.
            </p>

            <div className="ticket-box">
              <span className="ticket-label">
                Número de radicado
              </span>

              <strong className="ticket-code">
                {ticketCode}
              </strong>
            </div>

            <div
              className="actions"
              style={{ justifyContent: "center" }}
            >
              <a
                href={`/consulta?ticket=${encodeURIComponent(
                  ticketCode,
                )}`}
                className="btn btn-primary"
              >
                Consultar estado
              </a>

              <button
                type="button"
                className="btn btn-outline"
                onClick={() => setTicketCode("")}
              >
                Radicar otra solicitud
              </button>
            </div>
          </section>
        </main>
      </>
    );
  }

  return (
    <>
      <Header />

      <main className="form-page">
        <section className="form-card">
          <div className="form-heading">
            <h1>Radicar PQRS</h1>

            <p>
              Completa el formulario para radicar tu solicitud.
            </p>
          </div>

          {error && <div className="error-box">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="form-grid">

              <div className="field">
                <label htmlFor="applicant_name">
                  Nombre completo *
                </label>

                <input
                  id="applicant_name"
                  value={form.applicant_name}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      applicant_name: e.target.value,
                    })
                  }
                  required
                  placeholder="Ej. Juan Pérez"
                />
              </div>

              <div className="field">
                <label htmlFor="applicant_email">
                  Correo electrónico *
                </label>

                <input
                  id="applicant_email"
                  type="email"
                  value={form.applicant_email}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      applicant_email: e.target.value,
                    })
                  }
                  required
                  placeholder="Ej. juan@gmail.com"
                />
              </div>

              <div className="field">
                <label htmlFor="category">
                  Tipo de solicitud *
                </label>

                <select
                  id="category"
                  value={form.category}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      category: e.target.value,
                    })
                  }
                >
                  {categories.map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </select>
              </div>

              <div className="field">
                <label htmlFor="subject">
                  Asunto *
                </label>

                <input
                  id="subject"
                  value={form.subject}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      subject: e.target.value,
                    })
                  }
                  required
                  placeholder="Ej. Consulta sobre factura"
                />
              </div>

              <div className="field full">
                <label htmlFor="description">
                  Descripción *
                </label>

                <textarea
                  id="description"
                  rows={7}
                  value={form.description}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      description: e.target.value,
                    })
                  }
                  required
                  placeholder="Cuéntanos tu solicitud con el mayor detalle posible..."
                />
              </div>

              <div className="field full">
                <label>Documentos de soporte (PDF)</label>

                <input
                  ref={fileInputRef}
                  id="attachments"
                  type="file"
                  accept="application/pdf,.pdf"
                  multiple
                  onChange={handleFiles}
                  hidden
                />

                <button
                  type="button"
                  className="file-add-button"
                  onClick={() =>
                    fileInputRef.current?.click()
                  }
                  disabled={files.length >= MAX_FILES}
                >
                  + Agregar archivo
                </button>

                <span className="file-note">
                  Máximo 5 archivos, 5 MB por archivo.
                </span>

                {files.length > 0 && (
                  <div className="file-list">
                    {files.map((file, index) => (
                      <div
                        className="file-row"
                        key={`${file.name}-${file.size}-${file.lastModified}`}
                      >
                        <span
                          className="file-name"
                          title={file.name}
                        >
                          📄 {file.name}
                        </span>

                        <button
                          type="button"
                          className="file-remove"
                          onClick={() => removeFile(index)}
                          aria-label={`Eliminar ${file.name}`}
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div className="form-actions">
              <button
                className="btn btn-primary"
                type="submit"
                disabled={loading}
              >
                {loading
                  ? "Radicando..."
                  : "Radicar solicitud"}
              </button>
            </div>
          </form>
        </section>
      </main>
    </>
  );
}