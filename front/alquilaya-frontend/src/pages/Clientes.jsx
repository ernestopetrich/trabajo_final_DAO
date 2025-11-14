import React, {useEffect, useState} from "react";
import ClienteForm from "../components/ClienteForm";
import ClienteList from "../components/ClienteList";
import { getClientes, createCliente, deleteCliente } from "../api/api.js";

export default function Clientes(){
  const [clientes, setClientes] = useState([]);

  async function load(){
    const res = await getClientes();
    setClientes(res.data || []);
  }

  useEffect(()=>{ load(); }, []);

  async function handleCreate(data){
    await createCliente(data);
    load();
  }

  async function handleDelete(id){
    await deleteCliente(id);
    load();
  }

  return (
    <div className="page">
      <h2>Clientes</h2>
      <ClienteForm onSubmit={handleCreate}/>
      <ClienteList items={clientes} onDelete={handleDelete}/>
    </div>
  );
}
