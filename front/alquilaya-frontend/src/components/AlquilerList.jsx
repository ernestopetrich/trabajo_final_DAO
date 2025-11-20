import React, { useState, useMemo } from "react";

export default function AlquilerList({ items = [], vehiculos = [], clientes = [], onDevolver, onDelete }) {
  
  // 1. Estados para Búsqueda y Ordenamiento
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  // --- Helpers de Formato y Nombres ---
  const format = (iso) => {
    if (!iso) return "—";
    try { return new Date(iso).toLocaleString(); } catch (e) { return iso; }
  };

  const getClienteNombre = (idCliente) => {
    const cliente = clientes.find(c => c.id_cliente === idCliente);
    return cliente ? `${cliente.nombre} ${cliente.apellido}` : "Sin cliente";
  };

  const getVehiculoNombre = (idVehiculo) => {
    const vehiculo = vehiculos.find(v => v.id_vehiculo === idVehiculo);
    return vehiculo ? `${vehiculo.marca} ${vehiculo.nombre || ''} ${vehiculo.modelo}` : "Vehículo no encontrado";
  };

  // --- Lógica de Ordenamiento (Click en cabecera) ---
  const requestSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  // Helper visual para mostrar flechita
  const getClassNamesFor = (name) => {
    if (!sortConfig.key) return;
    return sortConfig.key === name ? sortConfig.direction : undefined;
  };

  // --- Procesamiento de Datos (Filtrar y Ordenar) ---
  const processedItems = useMemo(() => {
    // A. Enriquecer los datos
    let data = items.map(item => ({
      ...item,
      clienteNombre: getClienteNombre(item.id_cliente),
      vehiculoNombre: getVehiculoNombre(item.id_vehiculo)
    }));

    // B. Filtrar (Buscador)
    if (searchTerm) {
      const lowerTerm = searchTerm.toLowerCase();
      data = data.filter(item => 
        item.clienteNombre.toLowerCase().includes(lowerTerm) ||
        item.vehiculoNombre.toLowerCase().includes(lowerTerm) ||
        item.fecha_hora_inicio.includes(lowerTerm) ||
        String(item.id_alquiler).includes(lowerTerm)
      );
    }

    // C. Ordenar
    if (sortConfig.key) {
      data.sort((a, b) => {
        const valA = a[sortConfig.key] ? a[sortConfig.key].toString().toLowerCase() : "";
        const valB = b[sortConfig.key] ? b[sortConfig.key].toString().toLowerCase() : "";

        if (valA < valB) return sortConfig.direction === 'asc' ? -1 : 1;
        if (valA > valB) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return data;
  }, [items, searchTerm, sortConfig, clientes, vehiculos]);


  return (
    <div className="card">
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px', flexWrap: 'wrap', gap: '10px'}}>
        {/* Título con contador */}
        <h3>Alquileres ({processedItems.length})</h3>
        
        {/* INPUT DE BÚSQUEDA */}
        <input 
          type="text" 
          placeholder="🔍 Buscar cliente, vehículo, fecha..." 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            padding: '8px 12px',
            borderRadius: '6px',
            border: '1px solid #ccc',
            width: '100%',
            maxWidth: '300px',
            fontSize: '0.9rem'
          }}
        />
      </div>

      <div style={{overflowX: 'auto'}}>
        <table className="table">
            <thead>
            <tr>
                {/* Cabeceras interactivas */}
                <th onClick={() => requestSort('id_alquiler')} style={{cursor: 'pointer', userSelect: 'none'}}>
                    ID {getClassNamesFor('id_alquiler') === 'asc' ? '▲' : getClassNamesFor('id_alquiler') === 'desc' ? '▼' : ''}
                </th>
                
                <th onClick={() => requestSort('clienteNombre')} style={{cursor: 'pointer', userSelect: 'none'}}>
                    Cliente {getClassNamesFor('clienteNombre') === 'asc' ? '▲' : getClassNamesFor('clienteNombre') === 'desc' ? '▼' : ''}
                </th>
                
                <th onClick={() => requestSort('vehiculoNombre')} style={{cursor: 'pointer', userSelect: 'none'}}>
                    Vehículo {getClassNamesFor('vehiculoNombre') === 'asc' ? '▲' : getClassNamesFor('vehiculoNombre') === 'desc' ? '▼' : ''}
                </th>
                
                <th onClick={() => requestSort('fecha_hora_inicio')} style={{cursor: 'pointer', userSelect: 'none'}}>
                    Inicio {getClassNamesFor('fecha_hora_inicio') === 'asc' ? '▲' : getClassNamesFor('fecha_hora_inicio') === 'desc' ? '▼' : ''}
                </th>
                
                <th>Fin Previsto</th>
                <th>Fin Real</th>
                
                <th onClick={() => requestSort('estado')} style={{cursor: 'pointer', userSelect: 'none'}}>
                    Estado {getClassNamesFor('estado') === 'asc' ? '▲' : getClassNamesFor('estado') === 'desc' ? '▼' : ''}
                </th>
                
                <th>Acciones</th>
            </tr>
            </thead>
            <tbody>
            {processedItems.length > 0 ? (
                processedItems.map(a => (
                <tr key={a.id_alquiler}>
                    <td style={{fontWeight: 'bold'}}>{a.id_alquiler}</td>
                    <td>{a.clienteNombre}</td>
                    <td>{a.vehiculoNombre}</td>
                    <td>{format(a.fecha_hora_inicio)}</td>
                    <td>{format(a.fecha_hora_fin_prevista)}</td>
                    <td>{format(a.fecha_hora_fin_real)}</td>
                    <td>
                        <span style={{
                            padding: '4px 8px', 
                            borderRadius: '4px', 
                            backgroundColor: a.estado === 'activo' ? '#d1fae5' : a.estado === 'eliminado' ? '#f3f4f6' : '#e0f2fe',
                            color: a.estado === 'activo' ? '#065f46' : '#374151', 
                            fontSize: '0.85em', fontWeight: 'bold',
                            textTransform: 'capitalize'
                        }}>
                            {a.estado}
                        </span>
                    </td>
                    <td>
                    <div style={{display: 'flex', gap: '6px'}}>
                        {/* Botón Devolver */}
                        <button 
                            disabled={a.estado === 'eliminado' || a.estado === 'finalizado'}
                            title="Devolver Vehículo"
                            style={{
                                backgroundColor: a.estado === 'activo' ? '#1D4ED8' : '#ccc',
                                color: 'white',
                                cursor: a.estado === 'activo' ? 'pointer' : 'not-allowed',
                                border: 'none', padding: '6px 10px', borderRadius: '4px',
                                fontWeight: '500'
                            }}
                            onClick={() => {onDevolver(a.id_alquiler)}}
                        >
                        Devolver
                        </button>

                        {/* Botón Eliminar */}
                        <button 
                            disabled={a.estado === 'eliminado' || a.estado === 'finalizado'} 
                            title="Eliminar Registro"
                            style={{
                                backgroundColor: a.estado === 'eliminado' || a.estado === 'finalizado' ? '#ccc' : '#dc3545', 
                                color: 'white',
                                cursor: a.estado === 'eliminado' || a.estado === 'finalizado' ? 'not-allowed' : 'pointer',
                                border: 'none', padding: '6px 10px', borderRadius: '4px',
                                fontWeight: '500'
                            }}
                            onClick={() => {
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
                ))
            ) : (
                <tr>
                    <td colSpan="8" style={{textAlign: 'center', padding: '30px', color: '#666'}}>
                        {searchTerm ? "No se encontraron resultados para tu búsqueda." : "No hay alquileres registrados."}
                    </td>
                </tr>
            )}
            </tbody>
        </table>
      </div>
    </div>
  );
}