import React, {useState} from "react";

const empty = { patente:"", marca:"", modelo:"", nombre:"", precio_diario:0 };

export default function VehiculoForm({onSubmit}){
  const [form, setForm] = useState(empty);
  const change = (e) => setForm({...form, [e.target.name]: e.target.value});
  const submit = async (e) => { e.preventDefault(); form.precio_diario = Number(form.precio_diario); await onSubmit(form); setForm(empty); };

  return (
    <form className="card form" onSubmit={submit}>
      <input name="patente" value={form.patente} onChange={change} placeholder="Patente" required />
      <input name="marca" value={form.marca} onChange={change} placeholder="Marca" />
      <input name="modelo" value={form.modelo} onChange={change} placeholder="Modelo" />
      <input name="nombre" value={form.nombre} onChange={change} placeholder="Nombre" />
      <input name="precio_diario" value={form.precio_diario} onChange={change} placeholder="Precio diario" type="number" />
      <button className="btn primary" type="submit">Crear Vehículo</button>
    </form>
  );
}
