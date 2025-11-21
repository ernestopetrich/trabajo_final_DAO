import React, { useState } from "react";
import { createDanio, createMulta } from "../api/api.js"; // <--- Importamos createDanio

export default function DevolucionWizard({ alquilerId, onFinish, onCancel }) {
  // step 1: Daños, step 2: Multas
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);

  // --- ESTADOS DEL FORMULARIO ---
  // Cambio de 'dano' a 'danio'
  const [danio, setDanio] = useState({
    descripcion: "",
    costo_reparacion: "",
    estado: "pendiente" 
  });

  const [multa, setMulta] = useState({
    descripcion: "",
    monto: "",
    estado: "pendiente" 
  });

  // --- MANEJADORES ---
  
  // Cambio de 'handleSaveDano' a 'handleSaveDanio'
  const handleSaveDanio = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (danio.descripcion) {
        await createDanio({ // <--- Usamos createDanio
          id_alquiler: alquilerId,
          descripcion: danio.descripcion,
          costo_reparacion: Number(danio.costo_reparacion) || 0,
          fecha_hora_reporte: new Date().toISOString(),
          estado: danio.estado
        });
      }
      setStep(2); 
    } catch (error) {
      alert("Error al guardar daño: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveMulta = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (multa.descripcion) {
        await createMulta({
          id_alquiler: alquilerId,
          descripcion: multa.descripcion,
          monto: Number(multa.monto) || 0,
          fecha_hora_multa: new Date().toISOString(),
          estado: multa.estado
        });
      }
      await onFinish(); 
    } catch (error) {
      alert("Error al guardar multa: " + error.message);
      setLoading(false); 
    }
  };

  const handleSkip = async () => {
    if (step === 1) {
      setStep(2);
    } else {
      setLoading(true);
      await onFinish(); 
    }
  };

  // --- ESTILOS INLINE ---
  const overlayStyle = {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.5)', 
    display: 'flex',
    justifyContent: 'center', 
    alignItems: 'center',     
    zIndex: 1000,
    backdropFilter: 'blur(2px)' 
  };

  const modalStyle = {
    backgroundColor: 'white',
    padding: '25px',
    borderRadius: '12px', 
    boxShadow: '0 10px 25px rgba(0,0,0,0.2)', 
    width: '100%',
    maxWidth: '500px',
    border: '1px solid #e5e7eb' 
  };

  return (
    <div style={overlayStyle}>
      <div style={modalStyle} className="card">
        
        {/* PASO 1: REPORTE DE DAÑOS */}
        {step === 1 && (
          <form onSubmit={handleSaveDanio}> {/* <--- Cambio aquí */}
            <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: '15px', borderBottom: '1px solid #eee', paddingBottom: '10px'}}>
                <h3 style={{margin: 0, color: '#1f2937'}}>⚠️ Reporte de Daños</h3>
                <span style={{fontSize:'0.8rem', color:'#666', backgroundColor: '#f3f4f6', padding: '2px 8px', borderRadius: '10px'}}>Paso 1/2</span>
            </div>
            
            <p style={{fontSize:'0.9rem', color:'#4b5563', marginBottom:'20px', lineHeight: '1.4'}}>
                Revisa el vehículo. Si encuentras nuevos daños, descríbelos abajo. Si está impecable, pulsa "Sin Daños".
            </p>

            <div style={{marginBottom: '15px'}}>
              <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', fontSize: '0.9rem'}}>Descripción del daño:</label>
              <textarea 
                value={danio.descripcion}
                onChange={(e) => setDanio({...danio, descripcion: e.target.value})} // <--- Cambio aquí
                placeholder="Ej: Rayadura profunda en guardabarros izquierdo..."
                rows="3"
                style={{width: '100%', padding: '10px', borderRadius:'6px', border:'1px solid #d1d5db', fontFamily: 'inherit'}}
              />
            </div>

            <div style={{marginBottom: '20px'}}>
              <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', fontSize: '0.9rem'}}>Costo estimado de reparación ($):</label>
              <input 
                type="number"
                value={danio.costo_reparacion}
                onChange={(e) => setDanio({...danio, costo_reparacion: e.target.value})} // <--- Cambio aquí
                placeholder="0.00"
                style={{width: '100%', padding: '10px', borderRadius:'6px', border:'1px solid #d1d5db'}}
              />
            </div>

            <div style={{display: 'flex', gap: '10px'}}>
              <button 
                type="button" 
                onClick={handleSkip}
                style={{flex: 1, backgroundColor: '#10B981', color: 'white', padding: '12px', border:'none', borderRadius:'6px', cursor:'pointer', fontWeight: '600'}}
              >
                ✅ Sin Daños
              </button>
              
              <button 
                type="submit" 
                disabled={!danio.descripcion || loading}
                style={{
                    flex: 1, 
                    backgroundColor: (!danio.descripcion || loading) ? '#fca5a5' : '#EF4444', 
                    color: 'white', padding: '12px', border:'none', borderRadius:'6px', 
                    cursor: (!danio.descripcion || loading) ? 'not-allowed' : 'pointer', 
                    fontWeight: '600'
                }}
              >
                {loading ? "Guardando..." : "⚠️ Registrar Daño"}
              </button>
            </div>
            
            <button type="button" onClick={onCancel} style={{marginTop: '15px', background:'none', border:'none', color:'#6b7280', cursor:'pointer', width:'100%', fontSize: '0.85rem'}}>
                Cancelar operación
            </button>
          </form>
        )}

        {/* PASO 2: REPORTE DE MULTAS (Sin cambios en variables, solo renderizado igual) */}
        {step === 2 && (
          <form onSubmit={handleSaveMulta}>
            <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: '15px', borderBottom: '1px solid #eee', paddingBottom: '10px'}}>
                <h3 style={{margin: 0, color: '#1f2937'}}>👮 Reporte de Multas</h3>
                <span style={{fontSize:'0.8rem', color:'#666', backgroundColor: '#f3f4f6', padding: '2px 8px', borderRadius: '10px'}}>Paso 2/2</span>
            </div>

            <p style={{fontSize:'0.9rem', color:'#4b5563', marginBottom:'20px', lineHeight: '1.4'}}>
                ¿El cliente cometió alguna infracción de tránsito durante el alquiler?
            </p>

            <div style={{marginBottom: '15px'}}>
              <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', fontSize: '0.9rem'}}>Descripción de la infracción:</label>
              <textarea 
                value={multa.descripcion}
                onChange={(e) => setMulta({...multa, descripcion: e.target.value})}
                placeholder="Ej: Exceso de velocidad en zona escolar..."
                rows="3"
                style={{width: '100%', padding: '10px', borderRadius:'6px', border:'1px solid #d1d5db', fontFamily: 'inherit'}}
              />
            </div>

            <div style={{marginBottom: '20px'}}>
              <label style={{display: 'block', marginBottom: '5px', fontWeight: '500', fontSize: '0.9rem'}}>Monto de la multa ($):</label>
              <input 
                type="number"
                value={multa.monto}
                onChange={(e) => setMulta({...multa, monto: e.target.value})}
                placeholder="0.00"
                style={{width: '100%', padding: '10px', borderRadius:'6px', border:'1px solid #d1d5db'}}
              />
            </div>

            <div style={{display: 'flex', gap: '10px'}}>
              <button 
                type="button" 
                onClick={handleSkip}
                disabled={loading}
                style={{flex: 1, backgroundColor: '#10B981', color: 'white', padding: '12px', border:'none', borderRadius:'6px', cursor:'pointer', fontWeight: '600'}}
              >
                {loading ? "Finalizando..." : "✅ Sin Multas (Fin)"}
              </button>
              
              <button 
                type="submit" 
                disabled={!multa.descripcion || loading}
                style={{
                    flex: 1, 
                    backgroundColor: (!multa.descripcion || loading) ? '#fbbf24' : '#F59E0B', 
                    color: 'white', padding: '12px', border:'none', borderRadius:'6px', 
                    cursor: (!multa.descripcion || loading) ? 'not-allowed' : 'pointer', 
                    fontWeight: '600'
                }}
              >
                {loading ? "Procesando..." : "👮 Registrar y Fin"}
              </button>
            </div>
          </form>
        )}

      </div>
    </div>
  );
}