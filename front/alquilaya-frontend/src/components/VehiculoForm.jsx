import React, {useState} from "react";

const empty = { patente:"", marca:"", modelo:"", nombre:"", precio_diario:"" };

export default function VehiculoForm({onSubmit}){
  const [form, setForm] = useState(empty);
  const change = (e) => setForm({...form, [e.target.name]: e.target.value});
  const submit = async (e) => { e.preventDefault(); form.precio_diario = Number(form.precio_diario); await onSubmit(form); setForm(empty); };

  return (
    <form className="card form" onSubmit={submit}>
      <input name="patente" value={form.patente} onChange={change} placeholder="Patente" required />
      <input name="marca" value={form.marca} onChange={change} placeholder="Marca" required/>
      <input name="modelo" value={form.modelo} onChange={change} placeholder="Modelo" required/>
      <input name="nombre" value={form.nombre} onChange={change} placeholder="Nombre" required/>
      <input
        name="precio_diario"
        value={form.precio_diario}
        onChange={change}
        placeholder="Precio diario (solo números)"
        type="number"
        step="any"
      />

      <button className="btn primary" type="submit">Crear Vehículo</button>
    </form>
  );
}
