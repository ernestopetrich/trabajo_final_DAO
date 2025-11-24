import React, { useState, useMemo } from "react";

export default function AlquilerList({ items = [], vehiculos = [], clientes = [], onDevolver, onDelete, onEdit, onStateChange, onViewFactura }) {
  
  // 1. Estados
  const [searchTerm, setSearchTerm] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: 'id_alquiler', direction: 'desc' });
  
  // Estado para los 5 filtros
  const [filters, setFilters] = useState({
    pendientes: true,   // Amarillo: Recién creados
    confirmados: true,  // Azul: Pagados, listos para entrega
    activos: true,      // Verde: En curso
    finalizados: false, // Gris: Historial
    eliminados: false   // Rojo: Papelera
  });

  // --- Helpers ---
  const format = (iso) => {
    if (!iso) return "—";
    try { return new Date(iso).toLocaleString(); } catch (e) { return iso; }
  };

  // Calcula días entre dos fechas (mínimo 1 día)
  const calcularDias = (inicioISO, finPrevistaISO) => {
    if (!inicioISO || !finPrevistaISO) return 0;
    const inicio = new Date(inicioISO);
    const fin = new Date(finPrevistaISO);
    const diffMs = fin - inicio;
    const diffHoras = diffMs / (1000 * 60 * 60);
    return Math.max(1, Math.ceil(diffHoras / 24)); // Mínimo 1 día
  };

  const getPrecioVehiculo = (id) => {
    const v = vehiculos.find(x => x.id_vehiculo === id);
    return v ? Number(v.precio_diario || 0) : 0;
  };

  const getClienteNombre = (id) => {
    const c = clientes.find(x => x.id_cliente === id);
    return c ? `${c.nombre} ${c.apellido}` : "Desconocido";
  };

  const getVehiculoNombre = (id) => {
    const v = vehiculos.find(x => x.id_vehiculo === id);
    return v ? `${v.marca} ${v.nombre} ${v.modelo} (${v.patente})` : "Desconocido";
  };

  // --- Ordenamiento ---
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

  // --- Procesamiento de Datos ---
  const processedItems = useMemo(() => {
    // 1. Enriquecer datos (Nombres y Precios)
    let data = items.map(item => {
      const precioDiario = getPrecioVehiculo(item.id_vehiculo);
      const dias = calcularDias(item.fecha_hora_inicio, item.fecha_hora_fin_prevista);
      const precioTotal = precioDiario * dias;

      return {
        ...item,
        clienteNombre: getClienteNombre(item.id_cliente),
        vehiculoNombre: getVehiculoNombre(item.id_vehiculo),
        diasCobrados: dias,
        precioTotal
      };
    });

    // 2. FILTRO POR ESTADO
    data = data.filter(i => {
      const s = i.estado; 
      if (filters.pendientes && s === 'pendiente') return true;
      if (filters.confirmados && (s === 'confirmado' || s === 'confirmada')) return true;
      if (filters.activos && s === 'activo') return true;
      if (filters.finalizados && (s === 'finalizado' || s === 'devuelto')) return true;
      if (filters.eliminados && (s === 'eliminado' || s === 'cancelado')) return true;
      return false;
    });

    // 3. BUSCADOR
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      data = data.filter(i => 
        i.clienteNombre.toLowerCase().includes(term) ||
        i.vehiculoNombre.toLowerCase().includes(term) ||
        String(i.id_alquiler).includes(term)
      );
    }

    // 4. ORDENAR
    if (sortConfig.key) {
      data.sort((a, b) => {
        const vA = a[sortConfig.key]?.toString().toLowerCase() || "";
        const vB = b[sortConfig.key]?.toString().toLowerCase() || "";
        return sortConfig.direction === 'asc' ? (vA < vB ? -1 : 1) : (vA > vB ? -1 : 1);
      });
    }
    return data;
  }, [items, searchTerm, sortConfig, filters, clientes, vehiculos]);

  // --- Botones de Acción (Workflow) ---
  const renderActions = (alquiler) => {
    const s = alquiler.estado;
    const id = alquiler.id_alquiler;
    const btnBase = { border:'none', padding:'5px 10px', borderRadius:'4px', cursor:'pointer', color:'white', fontSize:'0.85rem', fontWeight:'500' };

    return (
      <div style={{display: 'flex', gap: '5px'}}>


        {/* BOTÓN FACTURA (NUEVO) - Visible siempre que no sea borrador/eliminado */}
        {onViewFactura && s === 'finalizado' && (
            <button 
                style={{...btnBase, backgroundColor: '#64748b', display: 'flex', alignItems: 'center', gap: '4px'}} 
                onClick={() => onViewFactura(alquiler)}
                title="Ver Factura"
            >
                📄
            </button>
        )}

        
        {/* Pendiente -> Confirmado */}
        {s === 'pendiente' && onStateChange && (
            <button style={{...btnBase, backgroundColor: '#3B82F6'}} onClick={() => onStateChange(id, 'confirmado')} title="Registrar Pago">
                $ Confirmar
            </button>
        )}

        {/* Confirmado -> Activo */}
        {(s === 'confirmado' || s === 'confirmada') && onStateChange && (
            <button style={{...btnBase, backgroundColor: '#10B981'}} onClick={() => onStateChange(id, 'activo')} title="Entregar Llaves">
                🔑 Entregar
            </button>
        )}

        {/* Activo -> Devolver */}
        {s === 'activo' && onDevolver && (
            <button style={{...btnBase, backgroundColor: '#1D4ED8'}} onClick={() => onDevolver(id)} title="Recibir Vehículo">
                Devolver
            </button>
        )}

        {/* Editar (Solo si no está finalizado/eliminado) */}
        {onEdit && s !== 'finalizado' && s !== 'devuelto' && s !== 'eliminado' && (
            <button style={{...btnBase, backgroundColor: '#F59E0B'}} onClick={() => onEdit(alquiler)}>
                Editar
            </button>
        )}

        {/* Eliminar */}
        {onDelete && s !== 'eliminado' && s !== 'cancelado' && s !== 'finalizado' && (
            <button style={{...btnBase, backgroundColor: '#EF4444'}} onClick={() => { if(window.confirm("¿Eliminar alquiler?")) onDelete(id); }}>
                ✕
            </button>
        )}
      </div>
    );
  };

  return (
    <div className="card">
      <div style={{display: 'flex', flexDirection: 'column', gap: '15px', marginBottom: '15px'}}>
        
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
            <h3>Alquileres ({processedItems.length})</h3>
            
            {/* INPUT DE BÚSQUEDA PEGADO A LOS FILTROS */}
            <div style={{display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap', justifyContent: 'flex-end', flex: 1}}>
                
                {/* BARRA DE FILTROS */}
                <div style={{display: 'flex', gap: '8px', flexWrap: 'wrap'}}>
                    <label style={{
                        padding: '4px 10px', borderRadius: '15px', cursor: 'pointer', fontSize: '0.85rem',
                        backgroundColor: filters.pendientes ? '#fef9c3' : '#f9fafb', border: filters.pendientes ? '1px solid #facc15' : '1px solid #e5e7eb',
                        color: filters.pendientes ? '#854d0e' : '#9ca3af', fontWeight: filters.pendientes ? 'bold' : 'normal'
                    }}>
                        <input type="checkbox" checked={filters.pendientes} onChange={() => toggleFilter('pendientes')} style={{display:'none'}} />
                        Pendientes
                    </label>

                    <label style={{
                        padding: '4px 10px', borderRadius: '15px', cursor: 'pointer', fontSize: '0.85rem',
                        backgroundColor: filters.confirmados ? '#dbeafe' : '#f9fafb', border: filters.confirmados ? '1px solid #60a5fa' : '1px solid #e5e7eb',
                        color: filters.confirmados ? '#1e40af' : '#9ca3af', fontWeight: filters.confirmados ? 'bold' : 'normal'
                    }}>
                        <input type="checkbox" checked={filters.confirmados} onChange={() => toggleFilter('confirmados')} style={{display:'none'}} />
                        Confirmados
                    </label>

                    <label style={{
                        padding: '4px 10px', borderRadius: '15px', cursor: 'pointer', fontSize: '0.85rem',
                        backgroundColor: filters.activos ? '#dcfce7' : '#f9fafb', border: filters.activos ? '1px solid #4ade80' : '1px solid #e5e7eb',
                        color: filters.activos ? '#166534' : '#9ca3af', fontWeight: filters.activos ? 'bold' : 'normal'
                    }}>
                        <input type="checkbox" checked={filters.activos} onChange={() => toggleFilter('activos')} style={{display:'none'}} />
                        Activos
                    </label>

                    <label style={{
                        padding: '4px 10px', borderRadius: '15px', cursor: 'pointer', fontSize: '0.85rem',
                        backgroundColor: filters.finalizados ? '#e5e7eb' : '#f9fafb', border: filters.finalizados ? '1px solid #9ca3af' : '1px solid #e5e7eb',
                        color: filters.finalizados ? '#374151' : '#9ca3af', fontWeight: filters.finalizados ? 'bold' : 'normal'
                    }}>
                        <input type="checkbox" checked={filters.finalizados} onChange={() => toggleFilter('finalizados')} style={{display:'none'}} />
                        Finalizados
                    </label>

                    <label style={{
                        padding: '4px 10px', borderRadius: '15px', cursor: 'pointer', fontSize: '0.85rem',
                        backgroundColor: filters.eliminados ? '#fee2e2' : '#f9fafb', border: filters.eliminados ? '1px solid #f87171' : '1px solid #e5e7eb',
                        color: filters.eliminados ? '#991b1b' : '#9ca3af', fontWeight: filters.eliminados ? 'bold' : 'normal'
                    }}>
                        <input type="checkbox" checked={filters.eliminados} onChange={() => toggleFilter('eliminados')} style={{display:'none'}} />
                        Eliminados
                    </label>
                </div>

                <div style={{width: '1px', height: '20px', backgroundColor: '#ddd'}}></div>

                <input 
                    type="text" 
                    placeholder="🔍 Buscar..." 
                    value={searchTerm} 
                    onChange={e=>setSearchTerm(e.target.value)} 
                    style={{padding:'6px 12px', borderRadius:'6px', border:'1px solid #ccc', minWidth: '150px'}} 
                />
            </div>
        </div>
      </div>

      {/* Tabla */}
      <div style={{overflowX: 'auto'}}>
        <table className="table">
            <thead>
                <tr>
                    <th onClick={()=>requestSort('id_alquiler')} style={{cursor:'pointer'}}>ID {getClassNamesFor('id_alquiler') === 'asc' ? '▲' : '▼'}</th>
                    <th onClick={()=>requestSort('clienteNombre')} style={{cursor:'pointer'}}>Cliente</th>
                    <th onClick={()=>requestSort('vehiculoNombre')} style={{cursor:'pointer'}}>Vehículo</th>
                    <th>Fechas</th>
                    <th>Precio</th>
                    <th onClick={()=>requestSort('estado')} style={{cursor:'pointer'}}>Estado {getClassNamesFor('estado') === 'asc' ? '▲' : '▼'}</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {processedItems.map(a => (
                    <tr key={a.id_alquiler} style={{backgroundColor: (a.estado === 'eliminado' || a.estado === 'cancelado') ? '#f9fafb' : 'white'}}>
                        <td style={{fontWeight:'bold'}}>#{a.id_alquiler}</td>
                        <td>{a.clienteNombre}</td>
                        <td>{a.vehiculoNombre}</td>
                        <td style={{fontSize: '0.85rem', minWidth: '160px'}}>
                            <div><strong>Inicio:</strong> {format(a.fecha_hora_inicio)}</div>
                            <div style={{color: '#666'}}><strong>Fin:</strong> {format(a.fecha_hora_fin_prevista)}</div>
                            {a.fecha_hora_fin_real && <div style={{color: '#166534', marginTop:'2px'}}><strong>Fin Real:</strong> {format(a.fecha_hora_fin_real)}</div>}
                        </td>
                        <td>
                            {a.costo_total ? `$${a.costo_total.toLocaleString("es-AR")}` : `${a.precioTotal.toLocaleString("es-AR")}`}
                            <div style={{fontSize:'0.75rem', color:'#666'}}>({a.diasCobrados} días)</div>
                        </td>
                        <td>
                            <span style={{
                                textTransform: 'uppercase', fontSize: '0.7rem', fontWeight: 'bold', padding: '3px 8px', borderRadius: '4px',
                                backgroundColor: 
                                    a.estado === 'pendiente' ? '#fef9c3' : 
                                    (a.estado === 'confirmado' || a.estado === 'confirmada') ? '#dbeafe' :
                                    a.estado === 'activo' ? '#dcfce7' : 
                                    (a.estado === 'finalizado' || a.estado === 'devuelto') ? '#e5e7eb' : '#fee2e2',
                                color: 
                                    a.estado === 'pendiente' ? '#a16207' : 
                                    (a.estado === 'confirmado' || a.estado === 'confirmada') ? '#1e40af' :
                                    a.estado === 'activo' ? '#15803d' : '#374151'
                            }}>
                                {a.estado}
                            </span>
                        </td>
                        <td>{renderActions(a)}</td>
                    </tr>
                ))}
                {processedItems.length === 0 && <tr><td colSpan="7" style={{textAlign:'center', padding:'20px'}}>No hay datos.</td></tr>}
            </tbody>
        </table>
      </div>
    </div>
  );
}