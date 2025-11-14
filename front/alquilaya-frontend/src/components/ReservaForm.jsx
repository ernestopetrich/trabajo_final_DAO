import React, {useState} from "react";
import { localToIso } from "../api/api.js";

export default function ReservaForm({onSubmit, clientes = [], vehiculos = []}){
  const [form, setForm] = useState({ id_cliente: "", id_vehiculo: "", fecha_inicio: "", fecha_fin: "" });

  const change = (e) => setForm({...form, [e.target.name]: e.target.value});

  const submit = async (e) => {
    e.preventDefault();
    // datetime-local inputs (date only) → we expect date only; here using date inputs
    await onSubmit({
      id_cliente: Number(form.id_cliente),
      id_vehiculo: Number(form.id_vehiculo),
      fecha_inicio: form.fecha_inicio, // expects YYYY-MM-DD or dd/mm/yyyy. Backend's to_iso will normalize
      fecha_fin: form.fecha_fin
    });
    setForm({ id_cliente: "", id_vehiculo: "", fecha_inicio: "", fecha_fin: "" });
  };

  return (
    <form className="card form" onSubmit={submit}>
      <select name="id_cliente" value={form.id_cliente} onChange={change} required>
        <option value="">Seleccione cliente</option>
        {clientes.map(c => <option key={c.id_cliente} value={c.id_cliente}>{c.nombre} {c.apellido}</option>)}
      </select>
      <select name="id_vehiculo" value={form.id_vehiculo} onChange={change} required>
        <option value="">Seleccione vehículo</option>
        {vehiculos.map(v => <option key={v.id_vehiculo} value={v.id_vehiculo}>{v.patente} - {v.nombre || v.modelo}</option>)}
      </select>
      <label>Fecha inicio (YYYY-MM-DD)</label>
      <input name="fecha_inicio" value={form.fecha_inicio} onChange={change} placeholder="2025-02-15" required />
      <label>Fecha fin (YYYY-MM-DD)</label>
      <input name="fecha_fin" value={form.fecha_fin} onChange={change} placeholder="2025-02-17" required />
      <button className="btn primary" type="submit">Crear Reserva</button>
    </form>
  );
}
