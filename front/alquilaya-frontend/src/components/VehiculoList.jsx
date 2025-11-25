import React, { useState, useMemo } from "react";

export default function VehiculoList({ items = [], onDelete, onEdit }) {
  
  // 1. Estados
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  
  // Estado para los 3 toggles de filtro
  const [filters, setFilters] = useState({
    disponibles: true, // Por defecto visible
    alquilados: true,    // Incluye 'alquilado' y 'mantenimiento'
    mantenimiento: false, // 'mantenimiento'
    eliminados: false  // Por defecto oculto
  });

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

  // Helper para cambiar filtros
  const toggleFilter = (key) => {
    setFilters(prev => ({ ...prev, [key]: !prev[key] }));
  };

  // 3. Procesamiento de Datos (Filtrar y Ordenar)
  const processedItems = useMemo(() => {
    let data = [...items];

    // A. FILTRO POR ESTADO (Los 4 Toggles)
    data = data.filter(v => {
      const e = v.estado;
      
      const isDisponible = e === 'disponible';
      const isAlquilado = e === 'alquilado';
      const isMantenimiento = e === 'mantenimiento';
      const isEliminado = e === 'eliminado';

      if (filters.disponibles && isDisponible) return true;
      if (filters.alquilados && isAlquilado) return true;
      if (filters.mantenimiento && isMantenimiento) return true;
      if (filters.eliminados && isEliminado) return true;
      
      return false;
    });

    // B. FILTRO POR BÚSQUEDA
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

    // C. ORDENAR
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
  }, [items, searchTerm, sortConfig, filters]); // Agregamos filters

  return (
    <div className="card">
      {/* Encabezado */}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px', flexWrap: 'wrap', gap: '15px'}}>
        <h3>Vehículos ({processedItems.length})</h3>
        
        {/* BARRA DE FILTROS Y BÚSQUEDA */}
        <div style={{display: 'flex', flexWrap: 'wrap', gap: '10px', alignItems: 'center', flex: 1, justifyContent: 'flex-end'}}>
            
            {/* Toggle: DISPONIBLES (Verde) */}
            <label style={{
                display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer', userSelect: 'none',
                backgroundColor: filters.disponibles ? '#dcfce7' : '#f3f4f6',
                border: filters.disponibles ? '1px solid #86efac' : '1px solid #e5e7eb',
                color: filters.disponibles ? '#166534' : '#6b7280',
                padding: '5px 10px', borderRadius: '20px', fontSize: '0.85rem', fontWeight: '500'
            }}>
                <input type="checkbox" checked={filters.disponibles} onChange={() => toggleFilter('disponibles')} style={{display:'none'}} />
                {filters.disponibles ? '✓' : ''} Disponibles
            </label>

            {/* Toggle: Alquilados (Azul - Alquiladoo) */}
            <label style={{
                display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer', userSelect: 'none',
                backgroundColor: filters.alquilados ? '#dbeafe' : '#f3f4f6',
                border: filters.alquilados ? '1px solid #93c5fd' : '1px solid #e5e7eb',
                color: filters.alquilados ? '#1e40af' : '#6b7280',
                padding: '5px 10px', borderRadius: '20px', fontSize: '0.85rem', fontWeight: '500'
            }}>
                <input type="checkbox" checked={filters.alquilados} onChange={() => toggleFilter('alquilados')} style={{display:'none'}} />
                {filters.alquilados ? '✓' : ''} Alquilados
            </label>

            {/* Toggle: mantenimiento (Gris - Mantenimiento) */}
            <label style={{
                display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer', userSelect: 'none',
                backgroundColor: filters.mantenimiento ? '#e5e7eb' : '#f9fafb',
                border: filters.mantenimiento ? '1px solid #9ca3af' : '1px solid #e5e7eb',
                color: filters.mantenimiento ? '#374151' : '#6b7280',
                padding: '5px 10px', borderRadius: '20px', fontSize: '0.85rem', fontWeight: '500'
            }}>
                <input type="checkbox" checked={filters.mantenimiento} onChange={() => toggleFilter('mantenimiento')} style={{display:'none'}} />
                {filters.mantenimiento ? '✓' : ''} Mantenimiento
            </label>

            {/* Toggle: ELIMINADOS (Rojo) */}
            <label style={{
                display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer', userSelect: 'none',
                backgroundColor: filters.eliminados ? '#fee2e2' : '#f3f4f6',
                border: filters.eliminados ? '1px solid #fca5a5' : '1px solid #e5e7eb',
                color: filters.eliminados ? '#991b1b' : '#6b7280',
                padding: '5px 10px', borderRadius: '20px', fontSize: '0.85rem', fontWeight: '500'
            }}>
                <input type="checkbox" checked={filters.eliminados} onChange={() => toggleFilter('eliminados')} style={{display:'none'}} />
                {filters.eliminados ? '✓' : ''} Eliminados
            </label>

            <div style={{width: '1px', height: '20px', backgroundColor: '#ddd', margin: '0 5px'}}></div>

            {/* INPUT DE BÚSQUEDA */}
            <input 
                type="text" 
                placeholder="🔍 Buscar..." 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{
                    padding: '6px 12px', borderRadius: '6px', border: '1px solid #ccc',
                    minWidth: '200px', fontSize: '0.9rem'
                }}
            />
        </div>
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
                Nombre {getClassNamesFor('nombre') === 'asc' ? '▲' : getClassNamesFor('nombre') === 'desc' ? '▼' : ''}
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
              processedItems.map((v) => {
                const isDeleted = v.estado === 'eliminado';
                const isAlquilado = v.estado === 'alquilado';
                const isInMaintenance = v.estado === 'mantenimiento';
                const isDisabled = isDeleted || isAlquilado;

                return (
                    <tr 
                        key={v.id_vehiculo}
                        style={{
                            backgroundColor: isDeleted ? '#f9fafb' : 'transparent',
                            color: isDeleted ? '#9ca3af' : 'inherit',
                            opacity: isDeleted ? 0.6 : 1
                        }}
                    >
                    <td style={{fontWeight: 'bold', fontFamily: 'monospace'}}>{v.patente}</td>
                    <td>{v.marca}</td>
                    <td>{v.modelo}</td>
                    <td>{v.nombre || '-'}</td>
                    <td>${v.precio_diario}</td>
                    <td>
                        <span style={{
                            padding: '4px 8px', 
                            borderRadius: '4px', 
                            backgroundColor: 
                            v.estado === 'disponible' ? '#d1fae5' : 
                            isDeleted ? '#fee2e2' :
                            isAlquilado ? '#e0f2fe' : 
                            isInMaintenance ? '#E5E7EB' : 'transparent',

                            color: v.estado === 'disponible' ? '#065f46' :
                            isDeleted ? '#991b1b' :
                            isAlquilado ? '#075985' : 
                            isInMaintenance ? '#364151' : 'inherit', 
                            fontSize: '0.85em', fontWeight: 'bold',
                            textTransform: 'capitalize',
                            border: isDeleted ? '1px solid #fecaca' : 'none'
                        }}>
                            {v.estado}
                        </span>
                    </td>
                    <td>
                        <div style={{display:'flex', gap:'6px'}}>
                            {/* BOTÓN EDITAR */}
                            <button 
                                disabled={isDisabled} // Permitimos editar aunque esté alquilado (para cambiar precio, etc), pero no si está borrado
                                onClick={() => onEdit(v)} 
                                title="Editar Vehículo"
                                style={{ 
                                    backgroundColor: isDeleted ? '#e5e7eb' : "#F59E0B", 
                                    color: isDeleted ? '#9ca3af' : 'white', 
                                    border: 'none', padding: '6px 10px', borderRadius: '4px', fontWeight: '500',
                                    cursor: isDeleted ? 'not-allowed' : 'pointer', 
                                }}
                            >
                                Editar
                            </button>

                            {/* BOTÓN ELIMINAR */}
                            <button 
                                disabled={isDisabled} // No eliminar si está en uso o ya eliminado
                                onClick={() => {
                                    if(!isDisabled && window.confirm('¿Estás seguro de eliminar este vehículo?')) {
                                        onDelete(v.id_vehiculo);
                                    }
                                }}
                                title="Eliminar Vehículo"
                                style={{ 
                                    backgroundColor: isDisabled ? '#e5e7eb' : "#EF4444", 
                                    color: isDisabled ? '#9ca3af' : 'white', 
                                    border: 'none', padding: '6px 10px', borderRadius: '4px', fontWeight: '500',
                                    cursor: isDisabled ? 'not-allowed' : 'pointer', 
                                }}
                            >
                                Eliminar
                            </button>
                        </div>
                    </td>
                    </tr>
                );
              })
            ) : (
                <tr>
                    <td colSpan="7" style={{textAlign: 'center', padding: '30px', color: '#666'}}>
                        No se encontraron resultados para los filtros seleccionados.
                    </td>
                </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}