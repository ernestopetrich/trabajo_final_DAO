import React from "react";

export default function AlquilerList({items = [], onDevolver}){
  // Convertir fecha ISO de la API en formato legible
  const format = (iso) => {
    if (!iso) return "—";
    const d = new Date(iso);
    return d.toLocaleString(); // Muestra fecha + hora según región
  };
  return (
    <div className="card">
      <h3>Alquileres</h3>
      <table className="table">
        <thead><tr><th>ID</th><th>Cliente</th><th>Vehículo</th><th>Inicio</th><th>Fin Prev</th><th>Fin Real</th><th>Estado</th><th>Acciones</th></tr></thead>
        <tbody>
          {items.map(a => (
            <tr key={a.id_alquiler}>
              <td>{a.id_alquiler}</td>
              <td>{a.id_cliente}</td>
              <td>{a.id_vehiculo}</td>
              <td>{a.fecha_hora_inicio}</td>
              <td>{a.fecha_hora_fin_prevista}</td>
              <td>{format(a.fecha_hora_fin_real)}</td>
              <td>{a.estado}</td>
              <td>{a.estado === 'activo' ? <button onClick={()=>onDevolver(a.id_alquiler)}>Devolver</button> : "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
