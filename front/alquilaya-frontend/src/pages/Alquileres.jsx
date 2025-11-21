import React, {useEffect, useState} from "react";
import AlquilerForm from "../components/AlquilerForm";
import AlquilerList from "../components/AlquilerList";
// Agregamos getEmpleados a los imports
import { getAlquileres, createAlquiler, deleteAlquiler, getVehiculos, getClientes, getEmpleados, updateAlquiler } from "../api/api";

export default function Alquileres(){
  const [alquileres, setAlquileres] = useState([]);
  const [vehiculos, setVehiculos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [empleados, setEmpleados] = useState([]); // Nuevo estado
  
  const [editingAlquiler, setEditingAlquiler] = useState(null);

  async function load(){
    // Cargamos todo en paralelo, incluyendo empleados
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

  // CREAR
  async function handleCreate(form){
    await createAlquiler({
        ...form,
        estado: 'pendiente' 
    });
    load();
  }

  // CAMBIAR ESTADO
  async function handleStateChange(id, nuevoEstado){
    await updateAlquiler(id, { estado: nuevoEstado });
    load();
  }

  // EDITAR
  async function handleUpdate(formData){
    await updateAlquiler(editingAlquiler.id_alquiler, formData);
    setEditingAlquiler(null);
    load();
  }

  // ELIMINAR
  async function handleDelete(id){
    await deleteAlquiler(id);
    load();
  }

  async function handleDevolver(id){
  // marcar como finalizado
  await updateAlquiler(id, {
    estado: 'finalizado',
    fecha_hora_fin_real: new Date().toISOString()
  });
  load(); // recargar la lista
}


  return (
    <div className="page">
      <h2>Gestión de Alquileres</h2>
      
      {/* Formulario de Creación */}
      <AlquilerForm 
        onSubmit={handleCreate} 
        clientes={clientes} 
        vehiculos={vehiculos}
        empleados={empleados} // Pasamos la lista de empleados
      />
      
      <hr/>

      {/* Modal de Edición */}
      {editingAlquiler && (
        <div className="modal-overlay">
            <div className="modal-content">
                <AlquilerForm 
                    initialData={editingAlquiler}
                    clientes={clientes}
                    vehiculos={vehiculos}
                    empleados={empleados} // Pasamos empleados también al modal
                    onSubmit={handleUpdate}
                    onCancel={() => setEditingAlquiler(null)}
                />
            </div>
            <hr/>
        </div>
      )}


      {/* Lista */}
      <AlquilerList 
        items={alquileres}
        vehiculos={vehiculos}
        clientes={clientes}
        onStateChange={handleStateChange}
        onDevolver={handleDevolver}
        onDelete={handleDelete}
        onEdit={setEditingAlquiler}
      />
    </div>
  );
}
