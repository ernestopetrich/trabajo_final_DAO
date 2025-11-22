import React, { useState, useEffect } from "react";

const empty = { tipo_dni: "DNI", dni: "", nombre: "", apellido: "" };

export default function EmpleadoForm({ onSubmit, initialData = null, onCancel }) {
  const [form, setForm] = useState(empty);

  useEffect(() => {
    if (initialData) {
      setForm(initialData);
    } else {
      setForm(empty);
    }
  }, [initialData]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await onSubmit(form);
    if (!initialData) setForm(empty);
  };

  return (
    <form className="card form" onSubmit={handleSubmit}>
      <h3>{initialData ? "Editar Empleado" : "Nuevo Empleado"}</h3>
      
      <div className="form-group">
        <div style={{display: 'flex', gap: '10px', marginBottom: '10px'}}>
            <select 
                name="tipo_dni" 
                value={form.tipo_dni} 
                onChange={handleChange} 
                style={{width: '100px', padding: '8px'}}
                required
            >
                <option value="DNI">DNI</option>
                <option value="PAS">PAS</option>
                <option value="CI">CI</option>
            </select>
            <input 
                name="dni" 
                value={form.dni} 
                onChange={handleChange} 
                placeholder="Número Documento" 
                required 
                style={{flex: 1, padding: '8px'}}
            />
        </div>

        <div style={{display: 'flex', gap: '10px'}}>
            <input 
                name="nombre" 
                value={form.nombre} 
                onChange={handleChange} 
                placeholder="Nombre" 
                required 
                style={{flex: 1, padding: '8px'}}
            />
            <input 
                name="apellido" 
                value={form.apellido} 
                onChange={handleChange} 
                placeholder="Apellido" 
                required 
                style={{flex: 1, padding: '8px'}}
            />
        </div>
      </div>
      
      <div style={{ marginTop: "20px", display: "flex", gap: "10px" }}>
        <button 
            type="submit" 
            style={{
                backgroundColor: initialData ? '#F59E0B' : '#10B981',
                flex: 1, color: 'white', border: 'none', padding: '10px', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold'
            }}
        >
          {initialData ? "Guardar Cambios" : "Crear Empleado"}
        </button>

        {onCancel && (
            <button 
                type="button" 
                onClick={onCancel} 
                style={{
                    backgroundColor: '#6B7280',
                    flex: 0.5, color: 'white', border: 'none', padding: '10px', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold'
                }}
            >
                Cancelar
            </button>
        )}
      </div>
    </form>
  );
}