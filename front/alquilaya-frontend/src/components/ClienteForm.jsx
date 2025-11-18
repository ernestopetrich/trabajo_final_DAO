import React, {useState} from "react";

const empty = { tipo_dni:"", dni:"", nombre:"", apellido:"", telefono:"", email:"", direccion:"" };

export default function ClienteForm({onSubmit}){
  const [form, setForm] = useState(empty);

  function change(e){ setForm({...form, [e.target.name]: e.target.value}); }

  async function submit(e){
    e.preventDefault();
    await onSubmit(form);
    setForm(empty);
  }

  return (
    <form className="card form" onSubmit={submit}>
      <select 
        name="tipo_dni" 
        value={form.tipo_dni} 
        onChange={change} 
        required
      >
        <option value="" disabled>Seleccione tipo de documento</option>
        <option value="DNI">DNI</option>
        <option value="PAS">Pasaporte</option>
        <option value="CI">Cédula</option>
</select>
      <input name="dni" value={form.dni} onChange={change} placeholder="DNI" />
      <input name="nombre" value={form.nombre} onChange={change} placeholder="Nombre" required />
      <input name="apellido" value={form.apellido} onChange={change} placeholder="Apellido" required />
      <div className="row">
        <input name="telefono" value={form.telefono} onChange={change} placeholder="Teléfono" />
        <input name="email" value={form.email} onChange={change} placeholder="Email" />
      </div>
      <input name="direccion" value={form.direccion} onChange={change} placeholder="Dirección" />
      <button className="btn primary" type="submit">Crear</button>
    </form>
  );
}
