import React, { useState, useEffect } from "react";

const years = Array.from({ length: 2025 - 1980 + 1 }, (_, i) => 1980 + i);

const empty = {
  tipoPatente: "nueva",
  p1: "",
  p2: "",
  p3: "",
  marca: "",
  modelo: "",
  nombre: "",
  precio_diario: "",
  estado: "disponible"
};

export default function VehiculoForm({ onSubmit, initialData = null, onCancel }) {
  const [form, setForm] = useState(empty);
  const [error, setError] = useState("");

  // --- EFECTO: Cargar datos al editar ---
  useEffect(() => {
    if (initialData) {
      // Intentamos detectar si es patente nueva o vieja para rellenar los inputs
      const p = initialData.patente || "";
      let parsedPatente = { tipoPatente: "nueva", p1: "", p2: "", p3: "" };

      // Regex Patente Nueva (AA 123 BB)
      const matchNueva = p.match(/^([A-Z]{2})([0-9]{3})([A-Z]{2})$/);
      // Regex Patente Vieja (AAA 123)
      const matchVieja = p.match(/^([A-Z]{3})([0-9]{3})$/);

      if (matchNueva) {
        parsedPatente = { 
          tipoPatente: "nueva", 
          p1: matchNueva[1], 
          p2: matchNueva[2], 
          p3: matchNueva[3] 
        };
      } else if (matchVieja) {
        parsedPatente = { 
          tipoPatente: "vieja", 
          p1: matchVieja[1], 
          p2: matchVieja[2], 
          p3: "" 
        };
      } else {
        // Si no matchea ninguna (ej: patente antigua o formato raro), 
        // la ponemos toda en p1 para que no se pierda
        parsedPatente = { tipoPatente: "vieja", p1: p, p2: "", p3: "" };
      }

      setForm({
        ...initialData,
        ...parsedPatente,
        precio_diario: initialData.precio_diario.toString()
      });
    } else {
      setForm(empty);
    }
    setError("");
  }, [initialData]);

  // --- MANEJADORES DE INPUTS ---

  const changeField = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const changeLetters = (name, maxLen) => (e) => {
    const value = e.target.value.replace(/[^A-Za-z]/g, "").toUpperCase();
    setForm({ ...form, [name]: value.slice(0, maxLen) });
  };

  const changeDigits = (name, maxLen) => (e) => {
    const value = e.target.value.replace(/\D/g, "");
    setForm({ ...form, [name]: value.slice(0, maxLen) });
  };

  const changeTipoPatente = (e) => {
    setForm({
      ...form,
      tipoPatente: e.target.value,
      p1: "",
      p2: "",
      p3: ""
    });
    setError("");
  };

  // --- VALIDACIÓN ---

  function validarYConstruirPatente() {
    const { tipoPatente, p1, p2, p3 } = form;
    const onlyLetters = /^[A-Za-z]+$/;
    const onlyDigits = /^[0-9]+$/;

    if (tipoPatente === "nueva") {
      // AA 123 AA
      if (p1.length !== 2 || !onlyLetters.test(p1)) {
        return { ok: false, msg: "Patente nueva: 1° bloque debe ser 2 letras (AA)." };
      }
      if (p2.length !== 3 || !onlyDigits.test(p2)) {
        return { ok: false, msg: "Patente nueva: 2° bloque debe ser 3 números." };
      }
      if (p3.length !== 2 || !onlyLetters.test(p3)) {
        return { ok: false, msg: "Patente nueva: 3° bloque debe ser 2 letras." };
      }
      return { ok: true, patente: `${p1}${p2}${p3}` };
    } else {
      // vieja: AAA 123
      // (Relajamos un poco la validación por si acaso estamos editando algo raro)
      if (p1.length < 1) { 
        return { ok: false, msg: "Patente vieja: falta la parte de letras." };
      }
      return { ok: true, patente: `${p1}${p2}` };
    }
  }

  // --- SUBMIT ---

  const submit = async (e) => {
    e.preventDefault();
    setError("");

    const { marca, modelo, nombre, precio_diario, estado } = form;

    const res = validarYConstruirPatente();
    if (!res.ok) {
      setError(res.msg);
      return;
    }

    const precioNum = Number(precio_diario);
    if (!precio_diario || Number.isNaN(precioNum)) {
      setError("El precio diario debe ser un número válido.");
      return;
    }

    const payload = {
      patente: res.patente,
      marca,
      modelo,
      nombre,
      precio_diario: precioNum,
      estado: estado || "disponible"
    };

    await onSubmit(payload);
    
    // Solo limpiamos si NO estamos editando (para crear otro seguido)
    if (!initialData) setForm(empty);
  };

  return (
    <form className="card form" onSubmit={submit}>
      <h3>{initialData ? "Editar Vehículo" : "Nuevo Vehículo"}</h3>

      {/* Selector de Tipo de Patente */}
      <div style={{marginBottom: '10px'}}>
        <label style={{display: 'block', marginBottom: '5px'}}>Formato de Patente</label>
        <select
            name="tipoPatente"
            value={form.tipoPatente}
            onChange={changeTipoPatente}
            style={{padding: '5px', width: '100%'}}
        >
            <option value="nueva">Patente nueva (AA 123 AA)</option>
            <option value="vieja">Patente vieja (AAA 123)</option>
        </select>
      </div>

      {/* Inputs de Patente */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
        {form.tipoPatente === "nueva" ? (
          <>
            <input style={{flex: 1}} placeholder="AA" value={form.p1} onChange={changeLetters("p1", 2)} />
            <input style={{flex: 2}} placeholder="123" value={form.p2} onChange={changeDigits("p2", 3)} />
            <input style={{flex: 1}} placeholder="AA" value={form.p3} onChange={changeLetters("p3", 2)} />
          </>
        ) : (
          <>
            <input style={{flex: 1}} placeholder="AAA" value={form.p1} onChange={changeLetters("p1", 3)} />
            <input style={{flex: 1}} placeholder="123" value={form.p2} onChange={changeDigits("p2", 3)} />
          </>
        )}
      </div>

      {/* Resto de campos */}
      <div style={{display: 'grid', gap: '10px'}}>
        <input name="marca" value={form.marca} onChange={changeField} placeholder="Marca (ej. Ford)" required />
        <select name="modelo" value={form.modelo} onChange={changeField} required style={{ padding: '5px' }} >
            <option value="">Modelo</option>
            {years.map(y => (
                <option key={y} value={y}>{y}</option>
            ))}
        </select>
        <input name="nombre" value={form.nombre} onChange={changeField} placeholder="Nombre (ej. Ranger)" />
        
        <div style={{display: 'flex', gap: '10px'}}>
            <input 
                name="precio_diario" 
                value={form.precio_diario} 
                onChange={changeField} 
                placeholder="Precio diario" 
                type="number" 
                step="any" 
                required 
                style={{flex: 1}}
            />
            <select name="estado" value={form.estado} onChange={changeField} style={{flex: 1}}>
                <option value="disponible">Disponible</option>
                <option value="mantenimiento">Mantenimiento</option>
            </select>
        </div>
      </div>

      {error && (
        <p style={{ color: "red", fontSize: "0.9rem", marginTop: "10px" }}>
          ⚠️ {error}
        </p>
      )}

      <div style={{ marginTop: "20px", display: "flex", gap: "10px" }}>
        <button type="submit" style={{backgroundColor: initialData ? '#F59E0B' : '#10B981', flex: 1, color: 'white', border: 'none', padding: '10px', borderRadius: '5px', cursor: 'pointer'}}>
          {initialData ? "Guardar Cambios" : "Crear Vehículo"}
        </button>
        
        {onCancel && (
            <button type="button" onClick={onCancel} style={{backgroundColor: '#6B7280', flex: 0.5, color: 'white', border: 'none', padding: '10px', borderRadius: '5px', cursor: 'pointer'}}>
                Cancelar
            </button>
        )}
      </div>
    </form>
  );
}