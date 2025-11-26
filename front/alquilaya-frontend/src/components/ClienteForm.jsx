import React, {useState, useEffect} from "react";

const empty = { tipo_dni:"", dni:"", nombre:"", apellido:"", telefono:"", email:"", direccion:"" };

export default function ClienteForm({onSubmit, initialData = null, onCancel}){
  const [form, setForm] = useState(empty);
  const [errors, setErrors] = useState({}); // Estado para mensajes de error

  // EFECTO: Si llegan datos iniciales (modo edición), rellenamos el formulario
  useEffect(() => {
    if (initialData) {
      setForm(initialData);
    } else {
      setForm(empty);
    }
    setErrors({}); // Limpiar errores al cambiar de modo
  }, [initialData]);

  function change(e){ 
    const { name, value } = e.target;
    let newValue = value;

    // --- 1. VALIDACIÓN DNI o telefono: Solo permitir números ---
    if (name === 'dni' || name === 'telefono') {
        newValue = value.replace(/[^0-9]/g, "");
    }

    setForm({...form, [name]: newValue});
    
    // Limpiamos el error visual si el usuario empieza a corregirlo
    if (errors[name]) {
        setErrors({...errors, [name]: ""});
    }
  }

  async function submit(e){
    e.preventDefault();
    
    const newErrors = {};

    // --- 2. VALIDACIÓN DNI (Mínimo 7 caracteres) ---
    if (form.dni && form.dni.length < 7) {
        newErrors.dni = "El DNI debe tener al menos 7 números.";
    }

    // --- 3. VALIDACIÓN EMAIL ---
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (form.email && !emailRegex.test(form.email)) {
        newErrors.email = "El formato del email no es válido (ej: usuario@mail.com)";
    }

    // Si hay errores, los mostramos y detenemos el envío
    if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        return;
    }

    await onSubmit(form);
    
    // Solo limpiamos el formulario si estamos creando uno nuevo.
    if (!initialData) setForm(empty);
    setErrors({});
  }

  return (
    <form className="card form" onSubmit={submit}>
      <h3>{initialData ? "Editar Cliente" : "Nuevo Cliente"}</h3>
      
      <select 
        name="tipo_dni" 
        value={form.tipo_dni} 
        onChange={change} 
        required
        style={{marginBottom: '10px'}}
      >
        <option value="" disabled>Seleccione tipo de documento</option>
        <option value="DNI">DNI</option>
        <option value="PAS">Pasaporte</option>
        <option value="CI">Cédula</option>
      </select>

      {/* Campo DNI con manejo de errores */}
      <div style={{marginBottom: '10px'}}>
        <input 
            name="dni" 
            value={form.dni} 
            onChange={change} 
            placeholder="DNI (Solo números)" 
            required 
            style={{
                width: '100%',
                border: errors.dni ? '1px solid #EF4444' : '1px solid #ccc',
                outline: errors.dni ? 'none' : undefined,
                padding: '8px' // Mantener estilo consistente si tenías CSS global
            }}
        />
        {errors.dni && (
            <span style={{color: '#EF4444', fontSize: '0.8rem', marginTop: '2px', display: 'block'}}>
                ⚠️ {errors.dni}
            </span>
        )}
      </div>
      
      <input name="nombre" value={form.nombre} onChange={change} placeholder="Nombre" required />
      <input name="apellido" value={form.apellido} onChange={change} placeholder="Apellido" required />
      
      <div className="row">
        <input 
            name="telefono" 
            value={form.telefono} 
            onChange={change} 
            placeholder="Teléfono (Solo números)" 
        />
        
        {/* Contenedor para el Email y su mensaje de error */}
        
            <input 
                name="email" 
                value={form.email} 
                onChange={change} 
                placeholder="Email" 
                style={{
                    border: errors.email ? '1px solid #EF4444' : '1px solid #ccc',
                    outline: errors.email ? 'none' : undefined
                }}
            />
            {errors.email && (
                <span style={{color: '#EF4444', fontSize: '0.8rem', marginTop: '2px'}}>
                    ⚠️ {errors.email}
                </span>
            )}
        
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