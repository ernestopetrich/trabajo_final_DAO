import React from "react";

export default function VehiculoList({items = [], onDelete}){
  return (
    <div className="card">
      <h3>Vehículos</h3>
      <table className="table">
        <thead><tr><th>ID</th><th>Patente</th><th>Modelo</th><th>Precio</th><th>Acciones</th></tr></thead>
        <tbody>
          {items.map(v => (
            <tr key={v.id_vehiculo}>
              <td>{v.id_vehiculo}</td>
              <td>{v.patente}</td>
              <td>{v.marca} {v.modelo}</td>
              <td>{v.precio_diario}</td>
              <td><button onClick={()=>onDelete(v.id_vehiculo)}>Eliminar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
