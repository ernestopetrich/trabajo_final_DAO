import React, { useState } from "react";

// tipoPatente = "nueva" => AA 123 AA
// tipoPatente = "vieja" => AAA 123
const empty = {
  tipoPatente: "nueva",
  p1: "",
  p2: "",
  p3: "",
  marca: "",
  modelo: "",
  nombre: "",
  precio_diario: ""
};

export default function VehiculoForm({ onSubmit }) {
  const [form, setForm] = useState(empty);
  const [error, setError] = useState("");

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

  function validarYConstruirPatente() {
    const { tipoPatente, p1, p2, p3 } = form;
    const onlyLetters = /^[A-Za-z]+$/;
    const onlyDigits = /^[0-9]+$/;

    if (tipoPatente === "nueva") {
      // AA 123 AA
      if (p1.length !== 2 || !onlyLetters.test(p1)) {
        return { ok: false, msg: "En patente nueva, el primer bloque debe ser 2 letras (AA)." };
      }
      if (p2.length !== 3 || !onlyDigits.test(p2)) {
        return { ok: false, msg: "En patente nueva, el bloque central debe ser 3 números." };
      }
      if (p3.length !== 2 || !onlyLetters.test(p3)) {
        return { ok: false, msg: "En patente nueva, el último bloque debe ser 2 letras." };
      }
      return { ok: true, patente: `${p1}${p2}${p3}` };
    } else {
      // vieja: AAA 123
      if (p1.length !== 3 || !onlyLetters.test(p1)) {
        return { ok: false, msg: "En patente vieja, el primer bloque debe ser 3 letras (AAA)." };
      }
      if (p2.length !== 3 || !onlyDigits.test(p2)) {
        return { ok: false, msg: "En patente vieja, el segundo bloque debe ser 3 números." };
      }
      return { ok: true, patente: `${p1}${p2}` };
    }
  }

  const submit = async (e) => {
    e.preventDefault();
    setError("");

    const { marca, modelo, nombre, precio_diario } = form;

    const res = validarYConstruirPatente();
    if (!res.ok) {
      setError(res.msg);
      return;
    }

    const precioNum = Number(precio_diario);
    if (!precio_diario || Number.isNaN(precioNum)) {
      setError("El precio diario debe ser un número.");
      return;
    }

    const payload = {
      patente: res.patente,
      marca,
      modelo,
      nombre,
      precio_diario: precioNum
    };

    await onSubmit(payload);
    setForm(empty);
  };

  return (
    <form className="card form" onSubmit={submit}>
      {/* Tipo de patente */}
      <label>Tipo de patente</label>
      <select
        name="tipoPatente"
        value={form.tipoPatente}
        onChange={changeTipoPatente}
      >
        <option value="nueva">Patente nueva (AA 123 AA)</option>
        <option value="vieja">Patente vieja (AAA 123)</option>
      </select>

      {/* Partes de la patente según tipo */}
      {form.tipoPatente === "nueva" ? (
        <>
          <label>Patente nueva (AA 123 AA)</label>
          <div className="row">
            <input
              placeholder="AA"
              value={form.p1}
              onChange={changeLetters("p1", 2)}
            />
            <input
              placeholder="123"
              value={form.p2}
              onChange={changeDigits("p2", 3)}
            />
            <input
              placeholder="AA"
              value={form.p3}
              onChange={changeLetters("p3", 2)}
            />
          </div>
        </>
      ) : (
        <>
          <label>Patente vieja (AAA 123)</label>
          <div className="row">
            <input
              placeholder="AAA"
              value={form.p1}
              onChange={changeLetters("p1", 3)}
            />
            <input
              placeholder="123"
              value={form.p2}
              onChange={changeDigits("p2", 3)}
            />
          </div>
        </>
      )}

      {/* Resto de campos */}
      <input
        name="marca"
        value={form.marca}
        onChange={changeField}
        placeholder="Marca"
      />
      <input
        name="modelo"
        value={form.modelo}
        onChange={changeField}
        placeholder="Modelo"
      />
      <input
        name="nombre"
        value={form.nombre}
        onChange={changeField}
        placeholder="Nombre"
      />
      <input
        name="precio_diario"
        value={form.precio_diario}
        onChange={changeField}
        placeholder="Precio diario (solo números)"
        type="number"
        step="any"
      />

      {error && (
        <p style={{ color: "red", fontSize: "0.8rem", marginTop: "4px" }}>
          {error}
        </p>
      )}

      <button className="btn primary" type="submit">
        Crear Vehículo
      </button>
    </form>
  );
}
