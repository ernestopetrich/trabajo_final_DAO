// front/src/pages/Dashboard.jsx
import React, {useEffect, useState, useRef} from "react";
import { 
  getAlquileres, 
  getVehiculos, 
  getClientes, 
  descargarPDF 
} from "../api/api.js";

import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default function Dashboard() {
  const [alquileres, setAlquileres] = useState([]);
  const [vehiculos, setVehiculos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);

  // Refs para gráficos
  const refFacturacion = useRef(null);
  const refVehiculos = useRef(null);
  const refAlqMes = useRef(null);

  const chartFact = useRef(null);
  const chartVeh = useRef(null);
  const chartAlqMes = useRef(null);

  // ===========================
  // 🔹 1) Carga de datos
  // ===========================
  async function load() {
    try {
      setLoading(true);
      const [rA, rV, rC] = await Promise.all([
        getAlquileres(),
        getVehiculos(),
        getClientes()
      ]);

      setAlquileres(rA.data || []);
      setVehiculos(rV.data || []);
      setClientes(rC.data || []);
    } catch (err) {
      console.error("Error cargando datos:", err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  // Mapa rápido ID → cliente
  const clienteMap = {};
  clientes.forEach(c => {
    clienteMap[c.id_cliente] = `${c.nombre} ${c.apellido}`;
  });

  // ===========================
  // 🔹 2) Renderizado de gráficos
  // ===========================
  useEffect(() => {
    if (loading) return;

    // Destruir previos
    if (chartFact.current) chartFact.current.destroy();
    if (chartVeh.current) chartVeh.current.destroy();
    if (chartAlqMes.current) chartAlqMes.current.destroy();

    // ----------------------------
    // 📌 GRAFICO FACTURACIÓN
    // ----------------------------
    const monthlyMoney = {};
    alquileres.forEach(a => {
      const fecha = a.fecha_hora_fin_real || a.fecha_hora_fin_prevista || a.fecha_hora_inicio;
      if (!fecha) return;
      const key = fecha.slice(0,7);
      monthlyMoney[key] = (monthlyMoney[key] || 0) + (a.costo_total || 0);
    });

    const labelsFact = Object.keys(monthlyMoney).sort();
    const dataFact = labelsFact.map(k => monthlyMoney[k]);

    if (refFacturacion.current) {
      chartFact.current = new Chart(refFacturacion.current.getContext("2d"), {
        type: "bar",
        data: {
          labels: labelsFact.length ? labelsFact : ["Sin datos"],
          datasets: [{
            label: "Facturación ($)",
            data: dataFact.length ? dataFact : [0],
            backgroundColor: "rgba(54,162,235,0.6)",
            borderColor: "rgba(54,162,235,1)",
            borderWidth: 1
          }]
        },
        options: { responsive: true, maintainAspectRatio: false }
      });
    }

    // ----------------------------
    // 📌 GRAFICO VEHÍCULOS MÁS ALQUILADOS
    // ----------------------------
    const countVeh = {};
    alquileres.forEach(a => {
      if (["eliminado", "cancelado", "pendiente"].includes(a.estado)) return;
      countVeh[a.id_vehiculo] = (countVeh[a.id_vehiculo] || 0) + 1;
    });

    const vehIds = Object.keys(countVeh);
    const labelsVeh = vehIds.map(id => {
      const v = vehiculos.find(x => x.id_vehiculo === Number(id));
      return v ? `${v.marca} ${v.modelo} (${v.patente})` : `Vehículo ${id}`;
    });
    const dataVeh = vehIds.map(id => countVeh[id]);

    if (refVehiculos.current) {
      chartVeh.current = new Chart(refVehiculos.current.getContext("2d"), {
        type: "pie",
        data: {
          labels: labelsVeh.length ? labelsVeh : ["Sin datos"],
          datasets: [{
            data: dataVeh.length ? dataVeh : [1],
            backgroundColor: [
              "#FF6384", "#36A2EB", "#FFCE56",
              "#4BC0C0", "#9966FF", "#FF9F40"
            ]
          }]
        },
        options: { responsive: true, maintainAspectRatio: false }
      });
    }

    // ----------------------------
    // 📌 GRAFICO ALQUILERES POR MES
    // ----------------------------
    const monthlyCount = {};
    alquileres.forEach(a => {
      const fecha = a.fecha_hora_inicio || a.fecha_hora_fin_real || a.fecha_hora_fin_prevista;
      if (["eliminado", "pendiente"].includes(a.estado)) return;
      if (!fecha) return;
      const key = fecha.slice(0,7);
      monthlyCount[key] = (monthlyCount[key] || 0) + 1;
    });

    const labelsMes = Object.keys(monthlyCount).sort();
    const dataMes = labelsMes.map(k => monthlyCount[k]);

    if (refAlqMes.current) {
      chartAlqMes.current = new Chart(refAlqMes.current.getContext("2d"), {
        type: "bar",
        data: {
          labels: labelsMes.length ? labelsMes : ["Sin datos"],
          datasets: [{
            label: "Alquileres",
            data: dataMes.length ? dataMes : [0],
            backgroundColor: "rgba(255,99,132,0.6)",
            borderColor: "rgba(255,99,132,1)",
            borderWidth: 1
          }]
        },
        options: { responsive: true, maintainAspectRatio: false }
      });
    }

    // cleanup
    return () => {
      if (chartFact.current) chartFact.current.destroy();
      if (chartVeh.current) chartVeh.current.destroy();
      if (chartAlqMes.current) chartAlqMes.current.destroy();
    };

  }, [alquileres, vehiculos, clientes, loading]);


  // ===========================
  // 🔹 Render
  // ===========================
  const cardStyle = {
    background: "white",
    padding: "20px",
    borderRadius: "8px",
    boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
    minHeight: "300px",
    display: "flex",
    flexDirection: "column"
  };

  const buttonStyle = {
    marginTop: "10px",
    padding: "8px 12px",
    background: "#0d6efd",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    width: "fit-content"
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Dashboard</h2>

      <div 
        style={{
          display: "grid",
          gap: "20px",
          gridTemplateColumns: "repeat(auto-fit, minmax(350px, 1fr))"
        }}
      >

        {/* 1️⃣ Alquileres por cliente */}
        <div style={cardStyle}>
          <h3>Alquileres por cliente</h3>

          <ul style={{listStyle: "none", padding: 0, maxHeight: 170, overflow: "auto"}}>
            {Object.entries(
              alquileres.reduce((acc, alq) => {
                if (!["eliminado", "cancelado"].includes(alq.estado)) {
                  acc[alq.id_cliente] = (acc[alq.id_cliente] || 0) + 1;
                }
                return acc;
              }, {})
            ).map(([id, cant]) => (
              <li key={id} style={{padding: "6px 0", borderBottom: "1px solid #f2f2f2"}}>
                {clienteMap[id] || `Cliente ${id}`} — {cant} alquiler(es)
              </li>
            ))}
          </ul>

          <button style={buttonStyle} onClick={() => descargarPDF("/reportes/pdf/alquileres-por-cliente")}>
            Descargar PDF
          </button>
        </div>

        {/* 2️⃣ Vehículos más alquilados */}
        <div style={cardStyle}>
          <h3>Vehículos más alquilados</h3>
          <div style={{ position: "relative", height: "230px" }}>
            <canvas ref={refVehiculos}></canvas>
          </div>
          <button style={buttonStyle} onClick={() => descargarPDF("/reportes/pdf/vehiculos-mas-alquilados")}>
            Descargar PDF
          </button>
        </div>

        {/* 3️⃣ Alquileres por mes — gráfico */}
        <div style={cardStyle}>
          <h3>Alquileres por mes</h3>
          <div style={{ position: "relative", height: "230px" }}>
            <canvas ref={refAlqMes}></canvas>
          </div>
          <button style={buttonStyle} onClick={() => descargarPDF("/reportes/pdf/alquileres-por-mes")}>
            Descargar PDF
          </button>
        </div>

        {/* 4️⃣ Facturación mensual */}
        <div style={cardStyle}>
          <h3>Facturación mensual</h3>
          <div style={{ position: "relative", height: "230px" }}>
            <canvas ref={refFacturacion}></canvas>
          </div>
          <button style={buttonStyle} onClick={() => descargarPDF("/reportes/pdf/facturacion-mensual")}>
            Descargar PDF
          </button>
        </div>

      </div>
    </div>
  );
}
