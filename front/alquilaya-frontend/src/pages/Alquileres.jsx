import React, {useEffect, useState} from "react";
import AlquilerForm from "../components/AlquilerForm";
import AlquilerList from "../components/AlquilerList";
import { getAlquileres, createAlquiler, devolverAlquiler, getVehiculos, getClientes } from "../api/api";
import { localToIso } from "../api/api.js";

export default function Alquileres(){
  const [alquileres, setAlquileres] = useState([]);
  const [vehiculos, setVehiculos] = useState([]);
  const [clientes, setClientes] = useState([]);

  async function load(){
    const a = await getAlquileres(); setAlquileres(a.data || []);
    const v = await getVehiculos(); setVehiculos(v.data || []);
    const c = await getClientes(); setClientes(c.data || []);
  }

  useEffect(()=>{ load(); }, []);

  async function handleCreate(form){
    try {
      const res = await createAlquiler({
        id_cliente: Number(form.id_cliente),
        id_vehiculo: Number(form.id_vehiculo),
        id_empleado: Number(form.id_empleado || 1),
        fecha_hora_inicio: localToIso(form.fecha_hora_inicio),
        fecha_hora_fin_prevista: localToIso(form.fecha_hora_fin_prevista)
      });

      if (res.error) {
        alert(res.error);
        return;
      }

      load();

    } catch (err) {
      alert("Error al crear alquiler: " + err.message);
    }
  }


  async function handleDevolver(id){
    await devolverAlquiler(id);
    load();
  }

  return (
    <div className="page">
      <h2>Alquileres</h2>
      <AlquilerForm onSubmit={handleCreate} clientes={clientes} vehiculos={vehiculos}/>
      <AlquilerList items={alquileres} vehiculos={vehiculos} clientes ={clientes} onDevolver={handleDevolver}/>
    </div>
  );
}
