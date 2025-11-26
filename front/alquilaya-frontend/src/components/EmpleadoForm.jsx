import React, { useState, useEffect } from "react";

const empty = { tipo_dni: "DNI", dni: "", nombre: "", apellido: "" };

export default function EmpleadoForm({ onSubmit, initialData = null, onCancel }) {
  const [form, setForm] = useState(empty);
  const [error, setError] = useState(""); // Estado para manejar mensajes de error

  useEffect(() => {
    if (initialData) {
      setForm(initialData);
    } else {
      setForm(empty);
    }
    setError(""); // Limpiar error al cambiar los datos o resetear
  }, [initialData]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    // Opcional: Limpiar el error apenas el usuario empiece a corregirlo
    if (e.target.name === "dni" || e.target.name === "tipo_dni") {
      setError(""); 
    }
  };

  const validate = () => {
    // 1. Validar que sea solo numérico
    if (!/^\d+$/.test(form.dni)) {
      setError("El documento debe contener solo números.");
      return false;
    }

    // 2. Validar longitud mínima si es DNI
    if (form.tipo_dni === "DNI" && form.dni.length < 7) {
      setError("El DNI debe tener al menos 7 dígitos.");
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Ejecutar validación antes de enviar
    if (!validate()) {
      return; // Si no pasa la validación, detenemos el envío
    }

    await onSubmit(form);
    if (!initialData) setForm(empty);
  };

  return (
    <form className="card form" onSubmit={handleSubmit}>
      <h3>{initialData ? "Editar Empleado" : "Nuevo Empleado"}</h3>
      
      <div className="form-group">
        <div style={{display: 'flex', flexDirection: 'column', marginBottom: '10px'}}>
            <div style={{display: 'flex', gap: '10px'}}>
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
                    style={{
                        flex: 1, 
                        padding: '8px',
                        borderColor: error ? 'red' : '#ccc' // Borde rojo si hay error
                    }}
                />
            </div>
            {/* Mensaje de error debajo del campo */}
            {error && (
                <span style={{ color: 'red', fontSize: '0.8rem', marginTop: '5px' }}>
                    {error}
                </span>
            )}
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