import React from "react";

export default function FacturaViewer({ alquiler, onClose }) {
  if (!alquiler) return null;

  // Cálculos auxiliares
  const dias = alquiler.diasCobrados || 0;
  const precioUnitario = alquiler.precioTotal / (dias || 1);
  const subtotal = alquiler.precioTotal;
  const impuestos = subtotal * 0.21; // Ejemplo IVA 21%
  const total = subtotal + impuestos;

  // Función para imprimir
  const handlePrint = () => {
    window.print();
  };

  // Estilos Inline para la "Hoja" de factura
  const sheetStyle = {
    backgroundColor: 'white',
    padding: '40px',
    borderRadius: '4px',
    boxShadow: '0 0 15px rgba(0,0,0,0.15)',
    maxWidth: '800px',
    width: '100%',
    margin: '0 auto',
    color: '#333',
    fontFamily: 'Helvetica, Arial, sans-serif'
  };

  return (
    <div className="modal-overlay" style={{zIndex: 2000}}>
      <div style={{width: '100%', maxHeight: '90vh', overflowY: 'auto', padding: '20px'}}>
        
        <div style={sheetStyle} className="factura-sheet">
          
          {/* Encabezado */}
          <div style={{borderBottom: '2px solid #333', paddingBottom: '20px', marginBottom: '30px', display: 'flex', justifyContent: 'space-between'}}>
            <div>
                <h1 style={{margin: 0, fontSize: '2rem'}}>ALQUILAYA</h1>
                <p style={{margin: '5px 0 0 0', fontSize: '0.9rem', color: '#666'}}>Servicios de Movilidad S.A.</p>
            </div>
            <div style={{textAlign: 'right'}}>
                <h2 style={{margin: 0, color: '#555'}}>FACTURA</h2>
                <p style={{margin: '5px 0'}}><strong>N°:</strong> 0001-{String(alquiler.id_alquiler).padStart(8, '0')}</p>
                <p style={{margin: 0}}><strong>Fecha:</strong> {new Date().toLocaleDateString()}</p>
            </div>
          </div>

          {/* Datos Cliente y Emisor */}
          <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '30px'}}>
            <div style={{width: '45%'}}>
                <h4 style={{borderBottom: '1px solid #ccc', paddingBottom: '5px'}}>Facturar a:</h4>
                <p style={{margin: '5px 0'}}><strong>Cliente:</strong> {alquiler.clienteNombre}</p>
                {/* Aquí podrías agregar DNI/Dirección si vinieran en el objeto alquiler completo */}
            </div>
            <div style={{width: '45%'}}>
                <h4 style={{borderBottom: '1px solid #ccc', paddingBottom: '5px'}}>Detalles del Servicio:</h4>
                <p style={{margin: '5px 0'}}><strong>Vehículo:</strong> {alquiler.vehiculoNombre}</p>
                <p style={{margin: '5px 0'}}><strong>Retiro:</strong> {new Date(alquiler.fecha_hora_inicio).toLocaleString()}</p>
                <p style={{margin: '5px 0'}}><strong>Devolución:</strong> {new Date(alquiler.fecha_hora_fin_prevista).toLocaleString()}</p>
            </div>
          </div>

          {/* Tabla de Conceptos */}
          <table style={{width: '100%', borderCollapse: 'collapse', marginBottom: '30px'}}>
            <thead>
                <tr style={{backgroundColor: '#f5f5f5', borderBottom: '1px solid #000'}}>
                    <th style={{padding: '10px', textAlign: 'left'}}>Descripción</th>
                    <th style={{padding: '10px', textAlign: 'center'}}>Cant. (Días)</th>
                    <th style={{padding: '10px', textAlign: 'right'}}>Precio Unit.</th>
                    <th style={{padding: '10px', textAlign: 'right'}}>Total</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style={{padding: '10px', borderBottom: '1px solid #eee'}}>Alquiler de Vehículo</td>
                    <td style={{padding: '10px', borderBottom: '1px solid #eee', textAlign: 'center'}}>{dias}</td>
                    <td style={{padding: '10px', borderBottom: '1px solid #eee', textAlign: 'right'}}>${precioUnitario.toLocaleString("es-AR")}</td>
                    <td style={{padding: '10px', borderBottom: '1px solid #eee', textAlign: 'right'}}>${subtotal.toLocaleString("es-AR")}</td>
                </tr>
                {/* Aquí podrías agregar filas extras para Multas o Daños si existieran */}
            </tbody>
          </table>

          {/* Totales */}
          <div style={{display: 'flex', justifyContent: 'flex-end'}}>
            <div style={{width: '250px'}}>
                <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '5px'}}>
                    <span>Subtotal:</span>
                    <span>${subtotal.toLocaleString("es-AR")}</span>
                </div>
                <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '10px', borderBottom: '1px solid #ccc', paddingBottom: '10px'}}>
                    <span>IVA (21%):</span>
                    <span>${impuestos.toLocaleString("es-AR")}</span>
                </div>
                <div style={{display: 'flex', justifyContent: 'space-between', fontSize: '1.2rem', fontWeight: 'bold'}}>
                    <span>TOTAL:</span>
                    <span>${total.toLocaleString("es-AR")}</span>
                </div>
            </div>
          </div>

          {/* Botones de Acción (No se imprimen gracias a @media print) */}
          <div className="no-print" style={{marginTop: '40px', textAlign: 'center', display: 'flex', gap: '10px', justifyContent: 'center'}}>
            <button onClick={handlePrint} style={{backgroundColor: '#333', color: 'white', padding: '10px 20px', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '1rem'}}>
                🖨️ Imprimir
            </button>
            <button onClick={onClose} style={{backgroundColor: '#ddd', color: '#333', padding: '10px 20px', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '1rem'}}>
                Cerrar
            </button>
          </div>

        </div>
      </div>
      
      {/* Estilos de Impresión */}
      <style>{`
        @media print {
          .no-print, .modal-overlay { background: none; }
          .modal-content { box-shadow: none; padding: 0; margin: 0; width: 100%; max-width: 100%; }
          .factura-sheet { box-shadow: none; margin: 0; padding: 0; width: 100%; }
          body * { visibility: hidden; }
          .factura-sheet, .factura-sheet * { visibility: visible; }
          .factura-sheet { position: absolute; left: 0; top: 0; }
        }
      `}</style>
    </div>
  );
}