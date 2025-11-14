import React, {useEffect, useState} from "react";
import VehiculoForm from "../components/VehiculoForm";
import VehiculoList from "../components/VehiculoList";
import { getVehiculos, createVehiculo, deleteVehiculo } from "../api/api";

export default function Vehiculos(){
  const [vehiculos, setVehiculos] = useState([]);

  async function load(){ const res = await getVehiculos(); setVehiculos(res.data || []); }
  useEffect(()=>{ load(); }, []);

  async function handleCreate(data){ await createVehiculo(data); load(); }
  async function handleDelete(id){ await deleteVehiculo(id); load(); }

  return (
    <div className="page">
      <h2>Vehículos</h2>
      <VehiculoForm onSubmit={handleCreate}/>
      <VehiculoList items={vehiculos} onDelete={handleDelete}/>
    </div>
  );
}
