import React, { useState, useMemo } from "react";

export default function ClienteList({ items = [], onDelete, onEdit }) {
  
  // 1. Estados
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  
  // Estado para los filtros (Toggles estilo Chips)
  const [filters, setFilters] = useState({
    activos: true,    // Por defecto visible
    eliminados: false // Por defecto oculto
  });

  // 2. Helper de Ordenamiento
  const requestSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  // Helper visual para la flechita de orden
  const getClassNamesFor = (name) => {
    if (!sortConfig.key) return;
    return sortConfig.key === name ? sortConfig.direction : undefined;
  };

  // Helper para cambiar filtros
  const toggleFilter = (key) => {
    setFilters(prev => ({ ...prev, [key]: !prev[key] }));
  };

  // 3. Procesamiento de Datos (Filtrar y Ordenar)
  const filteredItems = useMemo(() => {
    let data = [...items];

    // A. FILTRO POR ESTADO (Chips)
    data = data.filter(c => {
      // Asumimos que si no tiene estado, es activo.
      // Ajusta esto si tu backend usa otros valores (ej: 1 o 0)
      const isDeleted = c.estado === 'eliminado';
      const isActive = !isDeleted; // o c.estado === 'activo'

      if (filters.activos && isActive) return true;
      if (filters.eliminados && isDeleted) return true;
      
      return false;
    });

    // B. FILTRO POR BÚSQUEDA
    if (searchTerm) {
      const lowerTerm = searchTerm.toLowerCase();
      data = data.filter(c => 
        c.nombre.toLowerCase().includes(lowerTerm) ||
        c.apellido.toLowerCase().includes(lowerTerm) ||
        (c.email && c.email.toLowerCase().includes(lowerTerm)) || 
        String(c.dni).includes(lowerTerm)
      );
    }

    // C. ORDENAR
    if (sortConfig.key) {
      data.sort((a, b) => {
        let valA = a[sortConfig.key] ? a[sortConfig.key].toString().toLowerCase() : "";
        let valB = b[sortConfig.key] ? b[sortConfig.key].toString().toLowerCase() : "";

        if (valA < valB) return sortConfig.direction === 'asc' ? -1 : 1;
        if (valA > valB) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return data;
  }, [items, searchTerm, sortConfig, filters]);

  return (
    <div className="card">
      {/* Encabezado */}
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px', flexWrap: 'wrap', gap: '15px'}}>
        <h3>Clientes ({filteredItems.length})</h3>
        
        {/* BARRA DE FILTROS Y BÚSQUEDA */}
        <div style={{display: 'flex', flexWrap: 'wrap', gap: '10px', alignItems: 'center', flex: 1, justifyContent: 'flex-end'}}>
            
            {/* Toggle: ACTIVOS (Verde) */}
            <label style={{
                display: 'flex', alignItems: 'center', gap: '5px', cursor: 'pointer', userSelect: 'none',
                backgroundColor: filters.activos ? '#dcfce7' : '#f3f4f6',
                border: filters.activos ? '1px solid #86efac' : '1px solid #e5e7eb',
                color: filters.activos ? '#166534' : '#6b7280',
                padding: '5px 10px', borderRadius: '20px', fontSize: '0.85rem', fontWeight: '500'
            }}>
                <input type="checkbox" checked={filters.activos} onChange={() => toggleFilter('activos')} style={{display:'none'}} />
                {filters.activos ? '✓' : ''} Activos
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

            {/* INPUT BUSCADOR */}
            <input 
                type="text" 
                placeholder="🔍 Buscar DNI, nombre..." 
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
              {/* Cabeceras Ordenables */}
              <th onClick={() => requestSort('dni')} style={{cursor: 'pointer', userSelect: 'none'}}>
                DNI {getClassNamesFor('dni') === 'asc' ? '▲' : getClassNamesFor('dni') === 'desc' ? '▼' : ''}
              </th>
              
              <th onClick={() => requestSort('nombre')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Nombre {getClassNamesFor('nombre') === 'asc' ? '▲' : getClassNamesFor('nombre') === 'desc' ? '▼' : ''}
              </th>
              
              <th onClick={() => requestSort('apellido')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Apellido {getClassNamesFor('apellido') === 'asc' ? '▲' : getClassNamesFor('apellido') === 'desc' ? '▼' : ''}
              </th>
              
              <th onClick={() => requestSort('email')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Email {getClassNamesFor('email') === 'asc' ? '▲' : getClassNamesFor('email') === 'desc' ? '▼' : ''}
              </th>
              
              <th onClick={() => requestSort('estado')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Estado {getClassNamesFor('estado') === 'asc' ? '▲' : getClassNamesFor('estado') === 'desc' ? '▼' : ''}
              </th>
              
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {filteredItems.length > 0 ? (
              filteredItems.map(c => {
                const isDeleted = c.estado === 'eliminado';
                
                return (
                  <tr 
                    key={c.id_cliente} 
                    style={{
                        backgroundColor: isDeleted ? '#f9fafb' : 'transparent',
                        color: isDeleted ? '#9ca3af' : 'inherit',
                        opacity: isDeleted ? 0.6 : 1
                    }}
                  >
                    <td style={{fontWeight: 'bold', fontFamily: 'monospace'}}>{c.dni}</td>
                    <td>{c.nombre}</td>
                    <td>{c.apellido}</td>
                    <td>{c.email || <span style={{color: isDeleted ? '#ccc' : '#999', fontStyle: 'italic'}}>Sin email</span>}</td>
                    <td>
                        {/* Badge de Estado */}
                        {isDeleted ? (
                            <span style={{backgroundColor: '#fee2e2', color: '#991b1b', padding: '2px 6px', borderRadius: '4px', fontSize: '0.75em', fontWeight: 'bold', border: '1px solid #fecaca'}}>
                                ELIMINADO
                            </span>
                        ) : (
                            <span style={{backgroundColor: '#d1fae5', color: '#065f46', padding: '2px 6px', borderRadius: '4px', fontSize: '0.75em', fontWeight: 'bold', border: '1px solid #a7f3d0'}}>
                                ACTIVO
                            </span>
                        )}
                    </td>
                    <td>
                      <div style={{display: 'flex', gap: '6px'}}>
                          
                          {/* BOTÓN EDITAR */}
                          <button 
                              disabled={isDeleted} 
                              onClick={() => onEdit(c)} 
                              title="Editar Cliente"
                              style={{ 
                                  backgroundColor: isDeleted ? '#e5e7eb' : "#F59E0B", 
                                  color: isDeleted ? '#9ca3af' : 'white', 
                                  border: 'none', 
                                  padding: '6px 10px', 
                                  borderRadius: '4px', 
                                  cursor: isDeleted ? 'not-allowed' : 'pointer', 
                                  fontWeight: '500',
                                  fontSize: '0.9rem'
                              }}
                          >
                              Editar
                          </button>
  
                          {/* BOTÓN ELIMINAR */}
                          <button 
                              disabled={isDeleted} 
                              onClick={() => {
                                  if(window.confirm(`¿Estás seguro de eliminar al cliente ${c.nombre} ${c.apellido}?`)) {
                                      onDelete(c.id_cliente);
                                  }
                              }}
                              title="Eliminar Cliente"
                              style={{ 
                                  backgroundColor: isDeleted ? '#e5e7eb' : "#EF4444", 
                                  color: isDeleted ? '#9ca3af' : 'white', 
                                  border: 'none', 
                                  padding: '6px 10px', 
                                  borderRadius: '4px', 
                                  cursor: isDeleted ? 'not-allowed' : 'pointer', 
                                  fontWeight: '500',
                                  fontSize: '0.9rem'
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
                <td colSpan="6" style={{textAlign: 'center', padding: '30px', color: '#666'}}>
                  {searchTerm 
                    ? "No se encontraron clientes con esa búsqueda." 
                    : "No se encontraron resultados para los filtros seleccionados."}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}