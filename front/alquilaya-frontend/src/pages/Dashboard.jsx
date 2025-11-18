import React, {useEffect, useState, useRef} from "react";
import { getAlquileres, getVehiculos } from "../api/api.js";
import { Chart, registerables } from "chart.js";

// Registramos los componentes de Chart.js
Chart.register(...registerables);

export default function Dashboard() {
  const [alquileres, setAlquileres] = useState([]);
  const [vehiculos, setVehiculos] = useState([]);
  const [loading, setLoading] = useState(true); // Estado para saber si está cargando
  
  // Referencias a los elementos Canvas
  const canvasRef1 = useRef(null);
  const canvasRef2 = useRef(null);
  
  // Referencias para guardar las instancias de los gráficos y poder destruirlos
  const chartInstance1 = useRef(null);
  const chartInstance2 = useRef(null);

  // 1. Carga de datos
  async function load(){
    try {
      console.log("Iniciando carga de datos...");
      const [resAlquileres, resVehiculos] = await Promise.all([
        getAlquileres(),
        getVehiculos()
      ]);
      
      console.log("Datos recibidos:", resAlquileres.data);
      setAlquileres(resAlquileres.data || []);
      setVehiculos(resVehiculos.data || []);
    } catch (error) {
      console.error("Error cargando datos:", error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(()=>{ load(); }, []);

  // 2. Renderizado de Gráficos
  useEffect(() => {
    // Si está cargando o no hay referencias al DOM, no hacemos nada aún
    if (loading || !canvasRef1.current || !canvasRef2.current) return;

    // --- LIMPIEZA PREVIA OBLIGATORIA ---
    // Si ya existen gráficos, los destruimos antes de crear nuevos
    if (chartInstance1.current) {
      chartInstance1.current.destroy();
    }
    if (chartInstance2.current) {
      chartInstance2.current.destroy();
    }

    // --- LÓGICA GRÁFICO 1: Facturación Mensual ---
    const months = {};
    alquileres.forEach(x => {
      // Intentamos obtener la fecha de varias propiedades posibles
      const fechaRaw = x.fecha_hora_fin_real || x.fecha_hora_fin_prevista || x.fecha_hora_inicio;
      if (fechaRaw) {
        const d = fechaRaw.slice(0, 7); // YYYY-MM
        months[d] = (months[d] || 0) + (x.costo_total || 0);
      }
    });
    
    const labels1 = Object.keys(months).sort();
    const data1 = labels1.map(k => months[k]);

    const ctx1 = canvasRef1.current.getContext("2d");
    chartInstance1.current = new Chart(ctx1, {
      type: "bar",
      data: {
        labels: labels1.length ? labels1 : ["Sin datos"], // Fallback si no hay datos
        datasets: [{
          label: "Facturación ($)",
          data: data1.length ? data1 : [0],
          backgroundColor: "rgba(54, 162, 235, 0.6)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false, // Permite que se adapte al contenedor
      }
    });

    // --- LÓGICA GRÁFICO 2: Vehículos más alquilados ---
    const counts = {};
    alquileres.forEach(x => {
      if(x.id_vehiculo) {
        counts[x.id_vehiculo] = (counts[x.id_vehiculo] || 0) + 1;
      }
    });

    // Mapear IDs a Nombres (Patente o Modelo)
    const labels2 = Object.keys(counts).map(id => {
      const v = vehiculos.find(veh => veh.id_vehiculo === parseInt(id));
      return v ? `${v.marca} ${v.modelo} (${v.patente})` : `ID ${id}`;
    });
    const data2 = Object.values(counts);

    const ctx2 = canvasRef2.current.getContext("2d");
    chartInstance2.current = new Chart(ctx2, {
      type: "pie",
      data: {
        labels: labels2.length ? labels2 : ["Sin datos"],
        datasets: [{
          data: data2.length ? data2 : [1], // [1] para que se vea un círculo gris si está vacío
          backgroundColor: [
            "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"
          ]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
      }
    });

    // Función de limpieza al desmontar el componente
    return () => {
      if (chartInstance1.current) chartInstance1.current.destroy();
      if (chartInstance2.current) chartInstance2.current.destroy();
    };

  }, [alquileres, vehiculos, loading]); // Se re-ejecuta si cambian los datos

  return (
    <div className="page" style={{ padding: "20px" }}>
      <h2>Dashboard</h2>
      
      {loading && <p>Cargando estadísticas...</p>}
      
      {!loading && alquileres.length === 0 && (
        <div style={{ padding: "10px", backgroundColor: "#fff3cd", marginBottom: "20px", borderRadius: "5px" }}>
          ⚠️ No hay alquileres registrados. Los gráficos aparecerán vacíos.
        </div>
      )}

      <div className="grid" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "20px" }}>
        
        {/* Tarjeta 1 */}
        <div className="card" style={{ background: "white", padding: "20px", borderRadius: "8px", boxShadow: "0 2px 5px rgba(0,0,0,0.1)", minHeight: "300px" }}>
          <h3>Facturación mensual</h3>
          <div style={{ position: "relative", height: "250px", width: "100%" }}>
            <canvas ref={canvasRef1} />
          </div>
        </div>

        {/* Tarjeta 2 */}
        <div className="card" style={{ background: "white", padding: "20px", borderRadius: "8px", boxShadow: "0 2px 5px rgba(0,0,0,0.1)", minHeight: "300px" }}>
          <h3>Vehículos más alquilados</h3>
          <div style={{ position: "relative", height: "250px", width: "100%" }}>
            <canvas ref={canvasRef2} />
          </div>
        </div>

      </div>
    </div>
  );
}