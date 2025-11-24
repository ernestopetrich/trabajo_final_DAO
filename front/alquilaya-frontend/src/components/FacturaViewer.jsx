import React, { useEffect, useState } from "react";
// CORRECCIÓN: Agregamos .js explícitamente para resolver el error de importación
import { getFacturaByAlquiler } from "../api/api.js"; 

export default function FacturaViewer({ alquiler, onClose }) {
  const [factura, setFactura] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!alquiler) return;

    async function fetchFactura() {
      try {
        setLoading(true);
        // El backend devuelve el JSON con la estructura completa
        const res = await getFacturaByAlquiler(alquiler.id_alquiler);
        setFactura(res.data);
      } catch (err) {
        console.error("Error obteniendo factura:", err);
        setError("No se pudo cargar la factura. Verifique que el alquiler esté finalizado.");
      } finally {
        setLoading(false);
      }
    }

    fetchFactura();
  }, [alquiler]);

  if (!alquiler) return null;

  // --- Estilos Modal Centrado ---
  const overlayStyle = {
    position: 'fixed', top: 0, left: 0, width: '100%', height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.6)', display: 'flex', justifyContent: 'center', alignItems: 'center',
    zIndex: 2000, backdropFilter: 'blur(3px)'
  };

  const modalStyle = {
    backgroundColor: 'white', width: '100%', maxWidth: '800px', maxHeight: '90vh',
    overflowY: 'auto', borderRadius: '8px', boxShadow: '0 20px 50px rgba(0,0,0,0.3)',
    padding: '40px', position: 'relative'
  };

  return (
    <div style={overlayStyle} className="modal-overlay">
      <div style={modalStyle} className="factura-sheet">
        
        <button onClick={onClose} className="no-print" style={{position: 'absolute', top: '15px', right: '15px', background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer', color: '#999'}}>
            &times;
        </button>

        {loading && <div style={{textAlign: 'center', padding: '50px', color: '#666'}}>Cargando factura...</div>}
        
        {error && <div style={{textAlign: 'center', padding: '50px', color: '#ef4444'}}>⚠️ {error}</div>}

        {!loading && !error && factura && (
            <>
                {/* Encabezado */}
                <div style={{borderBottom: '2px solid #333', paddingBottom: '20px', marginBottom: '30px', display: 'flex', justifyContent: 'space-between'}}>
                    <div>
                        <h1 style={{margin: 0, fontSize: '2rem', color: '#333'}}>ALQUILAYA</h1>
                        <p style={{margin: '5px 0 0 0', fontSize: '0.9rem', color: '#666'}}>Servicios de Movilidad S.A.</p>
                        <p style={{margin: 0, fontSize: '0.8rem', color: '#666'}}>Av. Corrientes 1234, CABA</p>
                    </div>
                    <div style={{textAlign: 'right'}}>
                        <h2 style={{margin: 0, color: '#555'}}>FACTURA B</h2>
                        <p style={{margin: '5px 0'}}><strong>N°:</strong> {`${String(factura.id_factura).padStart(4, '0')}-${String(alquiler.id_alquiler).padStart(8, '0')}` || `0001-${String(alquiler.id_alquiler).padStart(8, '0')}`}</p>
                        <p style={{margin: 0}}><strong>Fecha:</strong> {new Date(factura.fecha_hora_emision || Date.now()).toLocaleDateString()}</p>
                    </div>
                </div>

                {/* Datos Cliente */}
                <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '30px', backgroundColor: '#f9f9f9', padding: '15px', borderRadius: '6px'}}>
                    <div style={{width: '100%'}}>
                        <h4 style={{margin: '0 0 10px 0', borderBottom: '1px solid #ddd', paddingBottom: '5px', color: '#555'}}>Cliente</h4>
                        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px'}}>
                            <p style={{margin: 0}}><strong>Nombre:</strong> {factura.cliente?.nombre || alquiler.clienteNombre}</p>
                            <p style={{margin: 0}}><strong>DNI/CUIT:</strong> {factura.cliente?.dni || "-"}</p>
                            <p style={{margin: 0}}><strong>Email:</strong> {factura.cliente?.email || "-"}</p>
                            <p style={{margin: 0}}><strong>Dirección:</strong> {factura.cliente?.direccion || "-"}</p>
                        </div>
                    </div>
                </div>

                {/* Tabla de Detalles (Items) */}
                <table style={{width: '100%', borderCollapse: 'collapse', marginBottom: '30px', fontSize: '0.95rem'}}>
                    <thead>
                        <tr style={{backgroundColor: '#333', color: 'white'}}>
                            <th style={{padding: '12px', textAlign: 'left', borderRadius: '4px 0 0 4px'}}>Concepto</th>
                            <th style={{padding: '12px', textAlign: 'center'}}>Cant.</th>
                            <th style={{padding: '12px', textAlign: 'right'}}>Precio Unit.</th>
                            <th style={{padding: '12px', textAlign: 'right', borderRadius: '0 4px 4px 0'}}>Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        {/* Renderizamos directamente los items que manda el backend */}
                        {factura.items?.map((item, index) => (
                            <tr key={index} style={{borderBottom: '1px solid #eee'}}>
                                <td style={{padding: '12px'}}>
                                    {item.descripcion}
                                </td>
                                <td style={{padding: '12px', textAlign: 'center'}}>
                                    {item.cantidad}
                                </td>
                                <td style={{padding: '12px', textAlign: 'right'}}>
                                    ${Number(item.monto).toLocaleString("es-AR")}
                                </td>
                                <td style={{padding: '12px', textAlign: 'right', fontWeight: 'bold'}}>
                                    ${Number(item.monto*item.cantidad).toLocaleString("es-AR")}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>

                {/* Totales (Calculados por el backend) */}
                <div style={{display: 'flex', justifyContent: 'flex-end'}}>
                    <div style={{width: '300px', padding: '20px', backgroundColor: '#f9f9f9', borderRadius: '8px'}}>
                        <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.9rem'}}>
                            <span>Subtotal:</span>
                            <span>${Number(factura.subtotal).toLocaleString("es-AR")}</span>
                        </div>
                        <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '15px', borderBottom: '1px solid #ddd', paddingBottom: '10px', fontSize: '0.9rem'}}>
                            <span>Impuestos:</span>
                            <span>${Number(factura.impuestos || 0).toLocaleString("es-AR")}</span>
                        </div>
                        <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '1.4rem', fontWeight: 'bold', color: '#333'}}>
                            <span>TOTAL:</span>
                            <span>${Number(factura.total).toLocaleString("es-AR")}</span>
                        </div>
                    </div>
                </div>

                {/* Pie de página */}
                <div style={{marginTop: '40px', textAlign: 'center', color: '#999', fontSize: '0.8rem'}}>
                    <p>Comprobante generado electrónicamente por AlquilaYa.</p>
                </div>

                {/* Botones */}
                <div className="no-print" style={{marginTop: '30px', textAlign: 'center', display: 'flex', gap: '15px', justifyContent: 'center'}}>
                    <button onClick={() => window.print()} style={{backgroundColor: '#1f2937', color: 'white', padding: '12px 25px', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '1rem', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '8px'}}>
                        🖨️ Imprimir
                    </button>
                    <button onClick={onClose} style={{backgroundColor: '#e5e7eb', color: '#374151', padding: '12px 25px', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '1rem', fontWeight: '600'}}>
                        Cerrar
                    </button>
                </div>
            </>
        )}
      </div>
      
      <style>{`
        @media print {
          .no-print, .modal-overlay { background: none; padding: 0; }
          .modal-content { box-shadow: none; padding: 0; margin: 0; width: 100%; max-width: 100%; border: none; }
          body * { visibility: hidden; }
          .factura-sheet, .factura-sheet * { visibility: visible; }
          .factura-sheet { position: absolute; left: 0; top: 0; width: 100%; }
        }
      `}</style>
    </div>
  );
}