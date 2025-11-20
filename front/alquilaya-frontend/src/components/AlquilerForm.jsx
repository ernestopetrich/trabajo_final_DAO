import React, { useState } from "react";

export default function AlquilerForm({ onSubmit, clientes = [], vehiculos = [] }) {

  const [form, setForm] = useState({
    id_cliente: "",
    id_vehiculo: "",
    id_empleado: "1",
    fecha_hora_inicio: "",
    fecha_hora_fin_prevista: ""
  });

  const [errors, setErrors] = useState({
    inicio: "",
    fin: ""
  });

  const pad = (n) => String(n).padStart(2, "0");

  // ==============================
  //   VALIDACIÓN EN TIEMPO REAL
  // ==============================
  function validar(inicioStr, finStr) {
    let errInicio = "";
    let errFin = "";

    const now = new Date();
    const inicio = inicioStr ? new Date(inicioStr) : null;
    const fin = finStr ? new Date(finStr) : null;

    // Validar fecha de inicio
    if (inicio && inicio < now) {
      errInicio = "La fecha de inicio no puede ser anterior a la actual.";
    }

    // Validar fecha de fin
    if (inicio && fin) {
      if (fin < inicio) {
        errFin = "La fecha de fin no puede ser anterior al inicio.";
      } else {
        const diff = (fin - inicio) / (1000 * 60 * 60);
        if (diff < 1) {
          errFin = "La fecha de fin debe ser al menos 1 hora después del inicio.";
        }
      }
    }

    setErrors({ inicio: errInicio, fin: errFin });
  }

  // ==============================
  //  CAMBIO DE FECHA INICIO
  //  (y seteo automático +1 hora)
  // ==============================
  const handleInicioChange = (e) => {
    const value = e.target.value;

    // Desarmar fecha EXACTA sin timezone
    const [fecha, hora] = value.split("T");
    const [y, m, d] = fecha.split("-").map(Number);
    const [hh, mm] = hora.split(":").map(Number);
    const inicio = new Date(y, m - 1, d, hh, mm);

    // Sumar 1 hora EXACTA
    const fin = new Date(inicio.getTime() + 60 * 60 * 1000);

    const finLocal =
      `${fin.getFullYear()}-${pad(fin.getMonth() + 1)}-${pad(fin.getDate())}` +
      `T${pad(fin.getHours())}:${pad(fin.getMinutes())}`;

    const newForm = {
      ...form,
      fecha_hora_inicio: value,
      fecha_hora_fin_prevista: finLocal
    };

    setForm(newForm);
    validar(newForm.fecha_hora_inicio, newForm.fecha_hora_fin_prevista);
  };

  // ==============================
  // CAMBIO GENÉRICO DE CAMPOS
  // ==============================
  const change = (e) => {
    const newForm = { ...form, [e.target.name]: e.target.value };
    setForm(newForm);

    if (e.target.name === "fecha_hora_fin_prevista") {
      validar(newForm.fecha_hora_inicio, newForm.fecha_hora_fin_prevista);
    }
  };

  // ==============================
  // SUBMIT
  // ==============================
  const submit = async (e) => {
    e.preventDefault();

    if (errors.inicio || errors.fin) return; // no debería pasar

    await onSubmit(form);
    
    // Limpieza si se creó bien
    setForm({
      id_cliente: "",
      id_vehiculo: "",
      id_empleado: "1",
      fecha_hora_inicio: "",
      fecha_hora_fin_prevista: ""
    });
  };

  return (
    <form className="card form" onSubmit={submit}>
      <h3>Nuevo Alquiler</h3>
      {/* Cliente */}
      <select name="id_cliente" value={form.id_cliente} onChange={change} required>
        <option value="">Cliente</option>
        {clientes.map(c => (
          <option key={c.id_cliente} value={c.id_cliente}>
            {c.nombre} {c.apellido}
          </option>
        ))}
      </select>

      {/* Vehículo */}
      <select name="id_vehiculo" value={form.id_vehiculo} onChange={change} required>
        <option value="">Vehículo</option>
        {vehiculos.map(v => (
          <option key={v.id_vehiculo} value={v.id_vehiculo}>
            {v.patente} — {v.marca} {v.nombre} {v.modelo}
          </option>
        ))}
      </select>

      {/* Inicio */}
      <label>Inicio</label>
      <input
        name="fecha_hora_inicio"
        type="datetime-local"
        value={form.fecha_hora_inicio}
        onChange={handleInicioChange}
        required
      />
      <div className="error-msg">{errors.inicio}</div>

      {/* Fin previsto */}
      <label>Fin previsto</label>
      <input
        name="fecha_hora_fin_prevista"
        type="datetime-local"
        value={form.fecha_hora_fin_prevista}
        onChange={change}
        required
      />
      <div className="error-msg">{errors.fin}</div>

      {/* Botón */}
      <div style={{ marginTop: "20px", display: "flex", gap: "10px" }}>
        <button type="submit" style={{backgroundColor: '#10B981', flex: 1, color: 'white', border: 'none', padding: '10px', borderRadius: '5px', cursor: 'pointer'}}>
          {"Crear Alquiler"}
        </button>
      </div>
    </form>
  );
}
