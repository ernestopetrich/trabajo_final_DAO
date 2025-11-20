import React, { useState, useMemo } from "react";

export default function VehiculoList({ items = [], onDelete, onEdit }) {
  
  // 1. Estados para Búsqueda y Ordenamiento
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  // 2. Helper de Ordenamiento
  const requestSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  // Helper visual (flechita)
  const getClassNamesFor = (name) => {
    if (!sortConfig.key) return;
    return sortConfig.key === name ? sortConfig.direction : undefined;
  };

  // 3. Procesamiento de Datos (Filtrar y Ordenar)
  const processedItems = useMemo(() => {
    let data = [...items];

    // A. Filtrar (Buscador)
    if (searchTerm) {
      const lowerTerm = searchTerm.toLowerCase();
      data = data.filter(v => 
        v.patente.toLowerCase().includes(lowerTerm) ||
        v.marca.toLowerCase().includes(lowerTerm) ||
        v.modelo.toLowerCase().includes(lowerTerm) ||
        (v.nombre && v.nombre.toLowerCase().includes(lowerTerm)) ||
        v.estado.toLowerCase().includes(lowerTerm)
      );
    }

    // B. Ordenar
    if (sortConfig.key) {
      data.sort((a, b) => {
        let valA = a[sortConfig.key];
        let valB = b[sortConfig.key];

        if (typeof valA === 'string') valA = valA.toLowerCase();
        if (typeof valB === 'string') valB = valB.toLowerCase();

        if (valA < valB) return sortConfig.direction === 'asc' ? -1 : 1;
        if (valA > valB) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return data;
  }, [items, searchTerm, sortConfig]);

  return (
    <div className="card">
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px', flexWrap: 'wrap', gap: '10px'}}>
        <h3>Listado de Vehículos ({processedItems.length})</h3>
        
        {/* INPUT DE BÚSQUEDA */}
        <input 
          type="text" 
          placeholder="🔍 Buscar patente, marca, modelo..." 
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
              {/* Cabeceras Interactivas */}
              <th onClick={() => requestSort('patente')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Patente {getClassNamesFor('patente') === 'asc' ? '▲' : getClassNamesFor('patente') === 'desc' ? '▼' : ''}
              </th>
              
              <th onClick={() => requestSort('marca')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Marca {getClassNamesFor('marca') === 'asc' ? '▲' : getClassNamesFor('marca') === 'desc' ? '▼' : ''}
              </th>

              <th onClick={() => requestSort('modelo')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Modelo {getClassNamesFor('modelo') === 'asc' ? '▲' : getClassNamesFor('modelo') === 'desc' ? '▼' : ''}
              </th>

              <th onClick={() => requestSort('nombre')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Categoría {getClassNamesFor('nombre') === 'asc' ? '▲' : getClassNamesFor('nombre') === 'desc' ? '▼' : ''}
              </th>
              
              <th onClick={() => requestSort('precio_diario')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Precio {getClassNamesFor('precio_diario') === 'asc' ? '▲' : getClassNamesFor('precio_diario') === 'desc' ? '▼' : ''}
              </th>
              
              <th onClick={() => requestSort('estado')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Estado {getClassNamesFor('estado') === 'asc' ? '▲' : getClassNamesFor('estado') === 'desc' ? '▼' : ''}
              </th>
              
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {processedItems.length > 0 ? (
              processedItems.map((v) => (
                <tr key={v.id_vehiculo}>
                  <td style={{fontWeight: 'bold', fontFamily: 'monospace'}}>{v.patente}</td>
                  <td>{v.marca}</td>
                  <td>{v.modelo}</td>
                  <td>{v.nombre || '-'}</td>
                  <td>${v.precio_diario}</td>
                  <td>
                    <span style={{
                        padding: '4px 8px', 
                        borderRadius: '4px', 
                        backgroundColor: v.estado === 'disponible' ? '#d1fae5' : v.estado === 'eliminado' ? '#f3f4f6' : '#fee2e2',
                        color: v.estado === 'disponible' ? '#065f46' : v.estado === 'eliminado' ? '#374151' : '#991b1b', 
                        fontSize: '0.85em', fontWeight: 'bold',
                        textTransform: 'capitalize'
                    }}>
                        {v.estado}
                    </span>
                  </td>
                  <td>
                    <div style={{display:'flex', gap:'6px'}}>
                        {/* BOTÓN EDITAR */}
                        <button 
                            disabled={v.estado === 'eliminado' || v.estado === 'alquilado'}
                            onClick={() => onEdit(v)} 
                            title="Editar Vehículo"
                            style={{ 
                                backgroundColor: v.estado === 'eliminado' || v.estado === 'alquilado' ? '#ccc' : "#F59E0B", 
                                color: 'white', 
                                border: 'none', 
                                padding: '6px 10px', 
                                borderRadius: '4px', 
                                cursor: v.estado === 'eliminado' || v.estado === 'alquilado' ? 'not-allowed' : 'pointer', 
                                fontWeight: '500' 
                            }}
                        >
                            Editar
                        </button>

                        {/* BOTÓN ELIMINAR */}
                        <button 
                            disabled={v.estado === 'eliminado' || v.estado === 'alquilado'}
                            onClick={() => {
                                if(v.estado !== 'eliminado' && window.confirm('¿Estás seguro de eliminar este vehículo?')) {
                                    onDelete(v.id_vehiculo);
                                }
                            }}
                            title="Eliminar Vehículo"
                            style={{ 
                                backgroundColor: v.estado === 'eliminado' || v.estado === 'alquilado' ? '#ccc' : "#EF4444", 
                                color: 'white', 
                                border: 'none', 
                                padding: '6px 10px', 
                                borderRadius: '4px', 
                                cursor: v.estado === 'eliminado' || v.estado === 'alquilado' ? 'not-allowed' : 'pointer', 
                                fontWeight: '500' 
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
                    <td colSpan="7" style={{textAlign: 'center', padding: '30px', color: '#666'}}>
                        {searchTerm ? "No se encontraron vehículos con esa búsqueda." : "No hay vehículos registrados."}
                    </td>
                </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}