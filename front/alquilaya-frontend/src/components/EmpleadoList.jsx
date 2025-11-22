import React, { useState, useMemo } from "react";

export default function EmpleadoList({ items = [], onDelete, onEdit }) {
  
  // 1. Estados
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  
  // Filtros (Chips)
  const [filters, setFilters] = useState({
    activos: true,
    eliminados: false
  });

  // 2. Helper de Ordenamiento
  const requestSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getClassNamesFor = (name) => {
    if (!sortConfig.key) return;
    return sortConfig.key === name ? sortConfig.direction : undefined;
  };

  const toggleFilter = (key) => {
    setFilters(prev => ({ ...prev, [key]: !prev[key] }));
  };

  // 3. Procesamiento de Datos
  const filteredItems = useMemo(() => {
    let data = [...items];

    // A. FILTRO POR ESTADO
    data = data.filter(e => {
      // Asumimos que si no tiene estado explícito, es activo
      const isDeleted = e.activo === false;
      const isActive = !isDeleted;

      if (filters.activos && isActive) return true;
      if (filters.eliminados && isDeleted) return true;
      
      return false;
    });

    // B. FILTRO POR BÚSQUEDA
    if (searchTerm) {
      const lowerTerm = searchTerm.toLowerCase();
      data = data.filter(e => 
        e.nombre.toLowerCase().includes(lowerTerm) ||
        e.apellido.toLowerCase().includes(lowerTerm) ||
        String(e.dni).includes(lowerTerm)
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
        <h3>Empleados ({filteredItems.length})</h3>
        
        <div style={{display: 'flex', flexWrap: 'wrap', gap: '10px', alignItems: 'center', flex: 1, justifyContent: 'flex-end'}}>
            
            {/* Toggle: ACTIVOS */}
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

            {/* Toggle: ELIMINADOS */}
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
                placeholder="🔍 Buscar empleado..." 
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
              <th onClick={() => requestSort('dni')} style={{cursor: 'pointer', userSelect: 'none'}}>
                DNI {getClassNamesFor('dni') === 'asc' ? '▲' : getClassNamesFor('dni') === 'desc' ? '▼' : ''}
              </th>
              <th onClick={() => requestSort('nombre')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Nombre {getClassNamesFor('nombre') === 'asc' ? '▲' : getClassNamesFor('nombre') === 'desc' ? '▼' : ''}
              </th>
              <th onClick={() => requestSort('apellido')} style={{cursor: 'pointer', userSelect: 'none'}}>
                Apellido {getClassNamesFor('apellido') === 'asc' ? '▲' : getClassNamesFor('apellido') === 'desc' ? '▼' : ''}
              </th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {filteredItems.length > 0 ? (
              filteredItems.map(e => {
                const isDeleted = e.activo === false;
                
                return (
                  <tr 
                    key={e.id_empleado} 
                    style={{
                        backgroundColor: isDeleted ? '#f9fafb' : 'transparent',
                        color: isDeleted ? '#9ca3af' : 'inherit',
                        opacity: isDeleted ? 0.6 : 1
                    }}
                  >
                    <td style={{fontWeight: 'bold', fontFamily: 'monospace'}}>{e.dni}</td>
                    <td>{e.nombre}</td>
                    <td>{e.apellido}</td>
                    <td>
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
                          <button 
                              disabled={isDeleted} 
                              onClick={() => onEdit(e)} 
                              title="Editar Empleado"
                              style={{ 
                                  backgroundColor: isDeleted ? '#e5e7eb' : "#F59E0B", 
                                  color: isDeleted ? '#9ca3af' : 'white', 
                                  border: 'none', padding: '6px 10px', borderRadius: '4px', fontWeight: '500', cursor: isDeleted ? 'not-allowed' : 'pointer'
                              }}
                          >
                              Editar
                          </button>
                          <button 
                              disabled={isDeleted} 
                              onClick={() => {
                                  if(window.confirm(`¿Estás seguro de eliminar a ${e.nombre} ${e.apellido}?`)) {
                                      onDelete(e.id_empleado);
                                  }
                              }}
                              title="Eliminar Empleado"
                              style={{ 
                                  backgroundColor: isDeleted ? '#e5e7eb' : "#EF4444", 
                                  color: isDeleted ? '#9ca3af' : 'white', 
                                  border: 'none', padding: '6px 10px', borderRadius: '4px', fontWeight: '500', cursor: isDeleted ? 'not-allowed' : 'pointer'
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
                <td colSpan="5" style={{textAlign: 'center', padding: '30px', color: '#666'}}>
                  {searchTerm ? "No se encontraron resultados." : "No hay empleados registrados."}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}