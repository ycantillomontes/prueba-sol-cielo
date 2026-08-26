"use client";

import { FormEvent, useState } from "react";

export default function Home() {
  const [formData, setFormData] = useState({
    applicant_name: "",
    applicant_email: "",
    category: "PETICION",
    subject: "",
    description: "",
  });

  const [loading, setLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [attachments, setAttachments] = useState<File[]>([]);

  const handleChange = (
    event: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = event.target;

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    setLoading(true);
    setSuccessMessage("");
    setErrorMessage("");

    const dataToSend = new FormData();

    dataToSend.append("applicant_name", formData.applicant_name);
    dataToSend.append("applicant_email", formData.applicant_email);
    dataToSend.append("category", formData.category);
    dataToSend.append("subject", formData.subject);
    dataToSend.append("description", formData.description);

    attachments.forEach((file) => {
      dataToSend.append("attachments", file);
    });

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/pqrs/",
        {
          method: "POST",
          body: dataToSend,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "No fue posible radicar la PQRS."
        );
      }

      setSuccessMessage(
        `Solicitud radicada correctamente. Número de radicado: ${data.ticket_code}`
      );

      setFormData({
        applicant_name: "",
        applicant_email: "",
        category: "PETICION",
        subject: "",
        description: "",
      });

      setAttachments([]);
    } catch (error) {
      if (error instanceof TypeError) {
        setErrorMessage(
          "No fue posible conectar con el servidor. Verifica que el backend de Django esté ejecutándose."
        );
      } else if (error instanceof Error) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage("Ocurrió un error inesperado.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-100 px-4 py-10">
      <div className="mx-auto max-w-2xl rounded-lg bg-white p-8 shadow">
        <h1 className="mb-2 text-3xl font-bold text-gray-900">
          Radicación de PQRS
        </h1>

        <p className="mb-8 text-gray-600">
          Registra tu petición, queja, reclamo o sugerencia.
        </p>

        <form onSubmit={handleSubmit} className="space-y-6">
          {successMessage && (
            <div className="rounded-md bg-green-100 p-4 text-green-800">
              {successMessage}
            </div>
          )}

          {errorMessage && (
            <div className="rounded-md bg-red-100 p-4 text-red-800">
              {errorMessage}
            </div>
          )}

          <div>
            <label
              htmlFor="applicant_name"
              className="mb-2 block font-medium text-gray-700"
            >
              Nombre completo
            </label>

            <input
              id="applicant_name"
              name="applicant_name"
              type="text"
              value={formData.applicant_name}
              onChange={handleChange}
              required
              className="w-full rounded-md border border-gray-300 px-4 py-2 outline-none focus:border-blue-500"
              placeholder="Ingresa tu nombre completo"
            />
          </div>

          <div>
            <label
              htmlFor="applicant_email"
              className="mb-2 block font-medium text-gray-700"
            >
              Correo electrónico
            </label>

            <input
              id="applicant_email"
              name="applicant_email"
              type="email"
              value={formData.applicant_email}
              onChange={handleChange}
              required
              className="w-full rounded-md border border-gray-300 px-4 py-2 outline-none focus:border-blue-500"
              placeholder="correo@ejemplo.com"
            />
          </div>

          <div>
            <label
              htmlFor="category"
              className="mb-2 block font-medium text-gray-700"
            >
              Categoría
            </label>

            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="w-full rounded-md border border-gray-300 px-4 py-2 outline-none focus:border-blue-500"
            >
              <option value="PETICION">Petición</option>
              <option value="QUEJA">Queja</option>
              <option value="RECLAMO">Reclamo</option>
              <option value="SUGERENCIA">Sugerencia</option>
            </select>
          </div>

          <div>
            <label
              htmlFor="subject"
              className="mb-2 block font-medium text-gray-700"
            >
              Asunto
            </label>

            <input
              id="subject"
              name="subject"
              type="text"
              value={formData.subject}
              onChange={handleChange}
              required
              className="w-full rounded-md border border-gray-300 px-4 py-2 outline-none focus:border-blue-500"
              placeholder="Asunto de la solicitud"
            />
          </div>

          <div>
            <label
              htmlFor="description"
              className="mb-2 block font-medium text-gray-700"
            >
              Descripción
            </label>

            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              required
              rows={6}
              className="w-full rounded-md border border-gray-300 px-4 py-2 outline-none focus:border-blue-500"
              placeholder="Describe detalladamente tu solicitud"
            />
          </div>

          <div>
            <label
              htmlFor="attachments"
              className="mb-2 block font-medium text-gray-700"
            >
              Anexos
            </label>

            <input
              id="attachments"
              name="attachments"
              type="file"
              multiple
              onChange={(event) => {
                setAttachments(
                  event.target.files
                    ? Array.from(event.target.files)
                    : []
                );
              }}
              className="w-full rounded-md border border-gray-300 px-4 py-2"
            />

            <p className="mt-1 text-sm text-gray-500">
              Puedes seleccionar uno o varios archivos.
            </p>

            {attachments.length > 0 && (
              <p className="mt-2 text-sm text-gray-600">
                {attachments.length} archivo(s) seleccionado(s).
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-md bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
          >
            {loading ? "Radicando..." : "Radicar PQRS"}
          </button>
        </form>
      </div>
    </main>
  );
}