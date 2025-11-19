import React from "react";

export default function AlquilerList({items = [], vehiculos = [], clientes = [], onDevolver}){
  // Convertir fecha ISO de la API en formato legible
  const format = (iso) => {
    if (!iso) return "—";
    const d = new Date(iso);
    return d.toLocaleString(); // Muestra fecha + hora según región
  };
  const getClienteNombre = (idCliente) => {
    const cliente = clientes.find(c => c.id_cliente === idCliente);
    return cliente ? `${cliente.nombre} ${cliente.apellido}` : "Sin cliente";
  };

  const getVehiculoNombre = (idVehiculo) => {
    const vehiculo = vehiculos.find(v => v.id_vehiculo === idVehiculo);
    return vehiculo ? `${vehiculo.marca} ${vehiculo.modelo}` : "Vehículo no encontrado";
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
              <td>{getClienteNombre(a.id_cliente)}</td>
              <td>{getVehiculoNombre(a.id_vehiculo)}</td>
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
