import React, {useEffect, useState, useRef} from "react";
import { getAlquileres, getVehiculos } from "../api/api.js";
import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export default function Dashboard(){
  const [alquileres, setAlquileres] = useState([]);
  const [vehiculos, setVehiculos] = useState([]);
  const canvasRef1 = useRef(null);
  const canvasRef2 = useRef(null);

  async function load(){
    const a = await getAlquileres(); setAlquileres(a.data || []);
    const v = await getVehiculos(); setVehiculos(v.data || []);
  }

  useEffect(()=>{ load(); }, []);

  useEffect(()=>{
    if(!alquileres.length) return;
    // Facturación mensual (simple: agrupa por mes YYYY-MM)
    const months = {};
    alquileres.forEach(x => {
      const d = (x.fecha_hora_fin_real || x.fecha_hora_fin_prevista || x.fecha_hora_inicio).slice(0,7);
      months[d] = (months[d] || 0) + (x.costo_total || 0);
    });
    const labels = Object.keys(months).sort();
    const data = labels.map(k=>months[k]);

    const ctx = canvasRef1.current.getContext("2d");
    new Chart(ctx, { type:"bar", data:{ labels, datasets:[{ label:"Facturación", data }] } });

    // Vehículos más alquilados
    const counts = {};
    alquileres.forEach(x => counts[x.id_vehiculo] = (counts[x.id_vehiculo]||0)+1);
    const vlabels = Object.keys(counts);
    const vdata = vlabels.map(k=>counts[k]);
    const ctx2 = canvasRef2.current.getContext("2d");
    new Chart(ctx2, { type:"pie", data:{ labels:vlabels, datasets:[{ data:vdata }] } });

  }, [alquileres]);

  return (
    <div className="page">
      <h2>Dashboard</h2>
      <div className="grid">
        <div className="card"><h3>Facturación mensual</h3><canvas ref={canvasRef1} /></div>
        <div className="card"><h3>Vehículos más alquilados</h3><canvas ref={canvasRef2} /></div>
      </div>
    </div>
  );
}
