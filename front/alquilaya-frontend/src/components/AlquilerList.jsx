import { on } from "events";
import React from "react";

export default function AlquilerList({items = [], vehiculos = [], clientes = [], onDevolver, onDelete}){
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
              <td>
                <div style={{display: 'flex', gap: '5px'}}>
                {/* Botón Devolver */}
                <button 
                    // 1. Lógica corregida: Se deshabilita si NO es 'activo'
                    disabled={a.estado !== 'activo'}
                    
                    style={{
                        // 2. Lógica de color: Azul (#1D4ED8) si es activo, Gris (#ccc) si no
                        backgroundColor: a.estado === 'activo' ? '#1D4ED8' : '#ccc',
                        color: 'white',
                        
                        // Cursor: Manito si es activo, Prohibido si no
                        cursor: a.estado === 'activo' ? 'pointer' : 'not-allowed',
                        
                        // 3. IMPORTANTE: Aseguramos que no tenga bordes raros ni herencias
                        border: 'none',
                        padding: '5px 10px',
                        borderRadius: '4px'
                    }}>
                    Devolver
                  </button>
                  {/* Botón Eliminar: Se deshabilita si es 'eliminado' */}
                  <button 
                      disabled={a.estado === 'eliminado'}
                      style={{
                          // Cambiamos el color a gris si está eliminado, si no rojo
                          backgroundColor: a.estado === 'eliminado' ? '#ccc' : '#dc3545', 
                          color: 'white',
                          cursor: a.estado === 'eliminado' ? 'not-allowed' : 'pointer'
                      }}
                      onClick={() => {
                          // Solo ejecuta si no está eliminado
                          if(a.estado !== 'eliminado' && window.confirm('¿Estás seguro de eliminar este alquiler?')) {
                              onDelete(a.id_alquiler);
                          }
                      }}
                  >
                      Eliminar
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
