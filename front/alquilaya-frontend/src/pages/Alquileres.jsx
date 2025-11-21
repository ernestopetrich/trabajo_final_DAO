import React, {useEffect, useState} from "react";
import AlquilerForm from "../components/AlquilerForm";
import AlquilerList from "../components/AlquilerList";
import DevolucionWizard from "../components/DevolucionWizard"; // <--- 1. Importamos el Wizard

// Agregamos getEmpleados a los imports
import { getAlquileres, createAlquiler, deleteAlquiler, getVehiculos, getClientes, getEmpleados, updateAlquiler, devolverAlquiler } from "../api/api";

export default function Alquileres(){
  const [alquileres, setAlquileres] = useState([]);
  const [vehiculos, setVehiculos] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [empleados, setEmpleados] = useState([]); 
  
  const [editingAlquiler, setEditingAlquiler] = useState(null);

  // <--- 2. Estado para controlar el Wizard (si no es null, se muestra)
  const [returningAlquilerId, setReturningAlquilerId] = useState(null);

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

  // <--- 3. Lógica del Wizard ---
  
  // Esta función se activa al tocar "Devolver" en la lista
  function iniciarDevolucion(id){
    setReturningAlquilerId(id); // Abre el wizard guardando el ID
  }

  // Esta función se ejecuta cuando el Wizard termina de guardar daños/multas
  async function finalizarDevolucion(){
    if (returningAlquilerId) {
        // Marcamos como finalizado en el backend
        await devolverAlquiler(returningAlquilerId); 
        setReturningAlquilerId(null); // Cerramos el wizard
        load(); // Recargamos la lista
    }
  }

  return (
    <div className="page">
      <h2>Gestión de Alquileres</h2>
      
      {/* Formulario de Creación */}
      <AlquilerForm 
        onSubmit={handleCreate} 
        clientes={clientes} 
        vehiculos={vehiculos}
        empleados={empleados} 
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
                    empleados={empleados}
                    onSubmit={handleUpdate}
                    onCancel={() => setEditingAlquiler(null)}
                />
            </div>
        </div>
      )}

      {/* <--- 4. Renderizado del Wizard --- */}
      {returningAlquilerId && (
        <DevolucionWizard 
            alquilerId={returningAlquilerId}
            onFinish={finalizarDevolucion}
            onCancel={() => setReturningAlquilerId(null)}
        />
      )}

      {/* Lista */}
      <AlquilerList 
        items={alquileres}
        vehiculos={vehiculos}
        clientes={clientes}
        onStateChange={handleStateChange}
        onDevolver={iniciarDevolucion} // <--- Pasamos iniciarDevolucion en vez de handleDevolver directo
        onDelete={handleDelete}
        onEdit={setEditingAlquiler}
      />
    </div>
  );
}