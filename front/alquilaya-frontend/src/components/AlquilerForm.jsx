import React, { useState, useEffect } from "react";

export default function AlquilerForm({ onSubmit, clientes = [], vehiculos = [], empleados = [], initialData = null, onCancel }) {

  const emptyState = {
    id_cliente: "",
    id_vehiculo: "",
    id_empleado: "", // Ahora empieza vacío para obligar a seleccionar
    fecha_hora_inicio: "",
    fecha_hora_fin_prevista: ""
  };

  const [form, setForm] = useState(emptyState);

  const [errors, setErrors] = useState({
    inicio: "",
    fin: ""
  });

  // --- EFECTO: Cargar datos si estamos editando ---
  useEffect(() => {
    if (initialData) {
      // Función auxiliar para cortar la fecha ISO (YYYY-MM-DDTHH:MM:SS) a lo que pide el input (YYYY-MM-DDTHH:MM)
      const formatForInput = (isoStr) => isoStr ? isoStr.substring(0, 16) : "";

      setForm({
        ...initialData,
        id_cliente: initialData.id_cliente || "",
        id_vehiculo: initialData.id_vehiculo || "",
        id_empleado: initialData.id_empleado || "",
        fecha_hora_inicio: formatForInput(initialData.fecha_hora_inicio),
        fecha_hora_fin_prevista: formatForInput(initialData.fecha_hora_fin_prevista)
      });
    } else {
      setForm(emptyState);
    }
  }, [initialData]);


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

    // Validar fecha de inicio (solo si es nuevo alquiler, al editar permitimos fechas pasadas)
    if (!initialData && inicio && inicio < now) {
      // Damos un margen de 5 minutos por si acaso
      if ((now - inicio) > 5 * 60 * 1000) {
          errInicio = "La fecha de inicio no puede ser anterior a la actual.";
      }
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
    if(!value) return;

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
      // Solo autocompletamos el fin si no estamos editando (para no pisar datos reales)
      fecha_hora_fin_prevista: initialData ? form.fecha_hora_fin_prevista : finLocal
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

    if (errors.inicio || errors.fin) return; 

    await onSubmit(form);
    
    // Limpieza solo si es creación nueva
    if (!initialData) {
        setForm(emptyState);
    }
  };

  return (
    <form className="card form" onSubmit={submit}>
      <h3>{initialData ? `Editar Alquiler #${initialData.id_alquiler}` : "Nuevo Alquiler"}</h3>
      
      {/* Fila 1: Cliente y Empleado */}
      <div style={{display: 'flex', gap: '10px'}}>
          <select name="id_cliente" value={form.id_cliente} onChange={change} required style={{flex: 1}}>
            <option value="">Seleccione Cliente</option>
            {/* AGREGAMOS LA VERIFICACIÓN AQUÍ */}
            {Array.isArray(clientes) && clientes.map(c => {
              if (c.estado === 'eliminado') return null;
              return (
                <option key={c.id_cliente} value={c.id_cliente}>
                  {c.nombre} {c.apellido}
                </option>
              );
            })}
          </select>

          <select name="id_empleado" value={form.id_empleado} onChange={change} required style={{flex: 1}}>
            <option value="">Seleccione Empleado</option>
            {/* AGREGAMOS LA VERIFICACIÓN AQUÍ */}
            {Array.isArray(empleados) && empleados.map(e => {
              if (e.activo === false) return null;
              return (
                <option key={e.id_empleado} value={e.id_empleado}>
                    {e.nombre} {e.apellido}
                </option>
            )})}
          </select>
      </div>

      {/* Vehículo */}
      <select name="id_vehiculo" value={form.id_vehiculo} onChange={change} required>
        <option value="">Seleccione Vehículo</option>
        {/* AGREGAMOS LA VERIFICACIÓN AQUÍ */}
        {Array.isArray(vehiculos) && vehiculos.map(v => {
          // ... tu lógica de filtrado ...
          const isSameVehicle = initialData && String(v.id_vehiculo) === String(initialData.id_vehiculo);
          if (v.estado !== 'disponible' && !isSameVehicle) return null;

          return (
            <option key={v.id_vehiculo} value={v.id_vehiculo}>
              {v.patente} — {v.marca} {v.nombre} {v.modelo} (${v.precio_diario}/día)
            </option>
          );
        })}
      </select>

      {/* Fechas */}
      <div style={{display: 'flex', gap: '10px'}}>
          <div style={{flex: 1}}>
            <label style={{fontSize: '0.85rem', display: 'block', marginBottom: '4px'}}>Inicio</label>
            <input
                name="fecha_hora_inicio"
                type="datetime-local"
                value={form.fecha_hora_inicio}
                onChange={handleInicioChange}
                required
                style={{width: '100%'}}
            />
            <div className="error-msg" style={{color: 'red', fontSize: '0.8rem'}}>{errors.inicio}</div>
          </div>

          <div style={{flex: 1}}>
            <label style={{fontSize: '0.85rem', display: 'block', marginBottom: '4px'}}>Fin Previsto</label>
            <input
                name="fecha_hora_fin_prevista"
                type="datetime-local"
                value={form.fecha_hora_fin_prevista}
                onChange={change}
                required
                style={{width: '100%'}}
            />
            <div className="error-msg" style={{color: 'red', fontSize: '0.8rem'}}>{errors.fin}</div>
          </div>
      </div>

      {/* Botones */}
      <div style={{ marginTop: "20px", display: "flex", gap: "10px" }}>
        <button type="submit" style={{backgroundColor: initialData ? '#F59E0B' : '#10B981', flex: 1, color: 'white', border: 'none', padding: '10px', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold'}}>
          {initialData ? "Guardar Cambios" : "Crear Alquiler"}
        </button>
        
        {onCancel && (
            <button type="button" onClick={onCancel} style={{backgroundColor: '#6B7280', flex: 0.5, color: 'white', border: 'none', padding: '10px', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold'}}>
                Cancelar
            </button>
        )}
      </div>
    </form>
  );
}