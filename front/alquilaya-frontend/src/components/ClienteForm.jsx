import React, {useState, useEffect} from "react";

const empty = { tipo_dni:"", dni:"", nombre:"", apellido:"", telefono:"", email:"", direccion:"" };

export default function ClienteForm({onSubmit, initialData = null, onCancel}){
  const [form, setForm] = useState(empty);

  // EFECTO: Si llegan datos iniciales (modo edición), rellenamos el formulario
  useEffect(() => {
    if (initialData) {
      setForm(initialData);
    } else {
      setForm(empty);
    }
  }, [initialData]);

  function change(e){ setForm({...form, [e.target.name]: e.target.value}); }

  async function submit(e){
    e.preventDefault();
    await onSubmit(form);
    
    // Solo limpiamos el formulario si estamos creando uno nuevo.
    // Si estamos editando, dejamos los datos o esperamos a que se cierre el modal.
    if (!initialData) setForm(empty);
  }

  return (
    <form className="card form" onSubmit={submit}>
      <h3>{initialData ? "Editar Cliente" : "Nuevo Cliente"}</h3>
      
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

      <input name="dni" value={form.dni} onChange={change} placeholder="DNI" required />
      <input name="nombre" value={form.nombre} onChange={change} placeholder="Nombre" required />
      <input name="apellido" value={form.apellido} onChange={change} placeholder="Apellido" required />
      
      <div className="row">
        <input name="telefono" value={form.telefono} onChange={change} placeholder="Teléfono" />
        <input name="email" value={form.email} onChange={change} placeholder="Email" />
      </div>
      
      <input name="direccion" value={form.direccion} onChange={change} placeholder="Dirección" />
      
      <div style={{ marginTop: "20px", display: "flex", gap: "10px" }}>
        <button 
            type="submit" 
            style={{
                backgroundColor: initialData ? '#F59E0B' : '#10B981', // Naranja para editar, Verde para crear
                flex: 1, 
                color: 'white', 
                border: 'none', 
                padding: '10px', 
                borderRadius: '5px', 
                cursor: 'pointer',
                fontWeight: 'bold'
            }}
        >
          {initialData ? "Guardar Cambios" : "Crear Cliente"}
        </button>

        {/* Botón Cancelar (solo aparece si estamos editando) */}
        {onCancel && (
            <button 
                type="button" 
                onClick={onCancel} 
                style={{
                    backgroundColor: '#6B7280', 
                    flex: 0.5, 
                    color: 'white', 
                    border: 'none', 
                    padding: '10px', 
                    borderRadius: '5px', 
                    cursor: 'pointer',
                    fontWeight: 'bold'
                }}
            >
                Cancelar
            </button>
        )}
      </div>
    </form>
  );
}