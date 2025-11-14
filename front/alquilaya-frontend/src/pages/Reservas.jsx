import React, {useEffect, useState} from "react";
import ReservaForm from "../components/ReservaForm";
import ReservaList from "../components/ReservaList";
import { getReservas, createReserva, getVehiculos, getClientes, createAlquilerFromReserva } from "../api/api";

export default function Reservas(){
  const [reservas, setReservas] = useState([]);
  const [vehiculos, setVehiculos] = useState([]);
  const [clientes, setClientes] = useState([]);

  async function loadAll(){
    const r = await getReservas(); setReservas(r.data || []);
    const v = await getVehiculos(); setVehiculos(v.data || []);
    const c = await getClientes(); setClientes(c.data || []);
  }

  useEffect(()=>{ loadAll(); }, []);

  async function handleCreate(payload){ await createReserva(payload); loadAll(); }
  async function handleConvert(id_reserva, id_empleado){
    try{
      await createAlquilerFromReserva({ id_reserva, id_empleado });
      loadAll();
      alert("Reserva convertida a alquiler");
    }catch(e){ alert("Error: " + e?.response?.data?.detail || e.message); }
  }

  return (
    <div className="page">
      <h2>Reservas</h2>
      <ReservaForm onSubmit={handleCreate} clientes={clientes} vehiculos={vehiculos}/>
      <ReservaList items={reservas} onConvert={handleConvert}/>
    </div>
  );
}
