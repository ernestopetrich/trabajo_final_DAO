import React, {useState} from "react";

export default function AlquilerForm({onSubmit, clientes=[], vehiculos=[]}){
  const [form, setForm] = useState({ id_cliente:"", id_vehiculo:"", id_empleado:"1", fecha_hora_inicio:"", fecha_hora_fin_prevista:"" });
  const change = (e) => setForm({...form, [e.target.name]: e.target.value});
  const submit = async (e) => { e.preventDefault(); await onSubmit(form); setForm({ id_cliente:"", id_vehiculo:"", id_empleado:"1", fecha_hora_inicio:"", fecha_hora_fin_prevista:"" }); };

  return (
    <form className="card form" onSubmit={submit}>
      <select name="id_cliente" value={form.id_cliente} onChange={change} required>
        <option value="">Cliente</option>
        {clientes.map(c => <option key={c.id_cliente} value={c.id_cliente}>{c.nombre} {c.apellido}</option>)}
      </select>
      <select name="id_vehiculo" value={form.id_vehiculo} onChange={change} required>
        <option value="">Vehículo</option>
        {vehiculos.map(v => <option key={v.id_vehiculo} value={v.id_vehiculo}>{v.patente} {v.nombre||v.modelo}</option>)}
      </select>
      <label>Inicio</label>
      <input name="fecha_hora_inicio" type="datetime-local" value={form.fecha_hora_inicio} onChange={change} required />
      <label>Fin previsto</label>
      <input name="fecha_hora_fin_prevista" type="datetime-local" value={form.fecha_hora_fin_prevista} onChange={change} required />
      <button className="btn primary" type="submit">Crear Alquiler</button>
    </form>
  );
}
