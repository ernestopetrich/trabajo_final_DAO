import React from "react";

export default function ReservaList({items = [], onConvert, onConfirmar}){
  return (
    <div className="card">
      <h3>Reservas</h3>
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Vehículo</th>
            <th>Inicio</th>
            <th>Fin</th>
            <th>Estado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {items.map(r => (
            <tr key={r.id_reserva}>
              <td>{r.id_reserva}</td>
              <td>{r.id_cliente}</td>
              <td>{r.id_vehiculo}</td>
              <td>{r.fecha_inicio}</td>
              <td>{r.fecha_fin}</td>
              <td>{r.estado}</td>
              <td>
                <button onClick={()=>onConvert(r.id_reserva, 1)}>Convertir (empleado 1)</button>
                <a> </a>
                <button onClick={()=>onConfirmar(r.id_reserva)}>Confirmar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
