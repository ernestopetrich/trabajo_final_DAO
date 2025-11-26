import React, {useEffect, useState} from "react";
import AlquilerForm from "../components/AlquilerForm";
import AlquilerList from "../components/AlquilerList";
import DevolucionWizard from "../components/DevolucionWizard"; // Para devolver
import FacturaViewer from "../components/FacturaViewer";       // Para ver factura

import { getAlquileres, createAlquiler, deleteAlquiler, getVehiculos, getClientes, getEmpleados, updateAlquiler, devolverAlquiler, confirmarAlquiler, iniciarAlquiler } from "../api/api";

export default function Alquileres(){
  const [alquileres, setAlquileres] = useState([]);
  const [vehiculos, setVehiculos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [empleados, setEmpleados] = useState([]);
  
  const [editingAlquiler, setEditingAlquiler] = useState(null);
  
  // ESTADO 1: Control del Wizard de Devolución
  const [returningAlquilerId, setReturningAlquilerId] = useState(null);

  // ESTADO 2: Control del Visor de Factura (¡Esto faltaba!)
  const [facturaAlquiler, setFacturaAlquiler] = useState(null);

  async function load(){
    const [a, v, c, e] = await Promise.all([
        getAlquileres(), 
        getVehiculos(), 
        getClientes(),
        getEmpleados()
    ]);
    setAlquileres(a.data || []);
    setVehiculos(v.data || []);
    setClientes(c.data || []);
    setEmpleados(e.data || []);
  }

  useEffect(()=>{ load(); }, []);

  // --- ACCIONES ---
  async function handleCreate(form){
    await createAlquiler({ ...form, estado: 'pendiente' });
    load();
  }

  async function handleStateChange(id, nuevoEstado){

    if (nuevoEstado === 'confirmado') {
      await confirmarAlquiler(id);
    }
    else if (nuevoEstado === 'activo') {
      await iniciarAlquiler(id);
    }
    load();
  }

  async function handleUpdate(formData){
    delete formData.id_alquiler; // Evitar modificar el ID
    delete formData.estado; // Evitar modificar estado aquí
    delete formData.clienteNombre;
    delete formData.vehiculoNombre;
    delete formData.diasCobrados;
    delete formData.precioTotal;
    await updateAlquiler(editingAlquiler.id_alquiler, formData);
    setEditingAlquiler(null);
    load();
  }

  async function handleDelete(id){
    await deleteAlquiler(id);
    load();
  }

  // --- LÓGICA WIZARD (Devolución) ---
  function iniciarDevolucion(id){
    setReturningAlquilerId(id);
  }

  async function finalizarDevolucion(){
    if (returningAlquilerId) {
        await devolverAlquiler(returningAlquilerId);
        setReturningAlquilerId(null);
        load();
    }
  }

  return (
    <div className="page">
      <h2>Gestión de Alquileres</h2>
      
      <AlquilerForm 
        onSubmit={handleCreate} 
        clientes={clientes} 
        vehiculos={vehiculos} 
        empleados={empleados} 
      />
      <hr/>

      {/* 1. Modal Edición */}
      {editingAlquiler && (
        <div className="modal-overlay">
            <div className="modal-content">
                <AlquilerForm 
                    initialData={editingAlquiler}
                    clientes={clientes}
                    vehiculos={vehiculos}
                    empleados={empleados}
                    onSubmit={handleUpdate}
                    onCancel={() => setEditingAlquiler(null)}
                />
            </div>
        </div>
      )}

      {/* 2. Modal Wizard Devolución */}
      {returningAlquilerId && (
        <DevolucionWizard 
            alquilerId={returningAlquilerId}
            onFinish={finalizarDevolucion}
            onCancel={() => setReturningAlquilerId(null)}
        />
      )}

      {/* 3. Modal Factura (¡Esto faltaba integrar!) */}
      {facturaAlquiler && (
        <FacturaViewer 
            alquiler={facturaAlquiler} 
            onClose={() => setFacturaAlquiler(null)} 
        />
      )}

      {/* Lista */}
      <AlquilerList 
        items={alquileres}
        vehiculos={vehiculos}
        clientes={clientes}
        onStateChange={handleStateChange}
        onDevolver={iniciarDevolucion}
        onDelete={handleDelete}
        onEdit={setEditingAlquiler}
        onViewFactura={setFacturaAlquiler} // <--- ¡CRUCIAL! Pasar la función aquí
      />
    </div>
  );
}