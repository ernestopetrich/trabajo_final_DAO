import React from "react";

export default function VehiculoList({items = [], onDelete}){
  return (
    <div className="card">
      <h3>Vehículos</h3>
      <table className="table">
        <thead><tr><th>ID</th><th>Patente</th><th>Modelo</th><th>Precio</th><th>Estado</th><th>Acciones</th></tr></thead>
        <tbody>
          {items.map(v => (
            <tr key={v.id_vehiculo}>
              <td>{v.id_vehiculo}</td>
              <td>{v.patente}</td>
              <td>{v.marca} {v.modelo}</td>
              <td>{v.precio_diario}</td>
              <td>{v.estado}</td>
              <td>
                <div style={{display: 'flex', gap: '5px'}}>
                  <button 
                      disabled={a.estado === 'eliminado'} // <--- AQUÍ ESTÁ LA MAGIA
                      style={{
                          // Cambiamos el color a gris si está eliminado, si no azul
                          backgroundColor: a.estado === 'eliminado' ? '#ccc' : '#1D4ED8', 
                          color: 'white',
                          cursor: a.estado === 'eliminado' ? 'not-allowed' : 'pointer'
                      }}
                      onClick={() => {onDevolver(a.id_alquiler)}}
                  >
                    Devolver
                  </button>
                  {/* Botón Eliminar: Se deshabilita si es 'eliminado' */}
                  <button 
                      disabled={a.estado === 'eliminado'} // <--- AQUÍ ESTÁ LA MAGIA
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
