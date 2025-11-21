import React, {useEffect, useState} from "react";
import ClienteForm from "../components/ClienteForm";
import ClienteList from "../components/ClienteList";
// Asegúrate de importar updateCliente (debes crearla en api.js: axios.patch/put)
import { getClientes, createCliente, deleteCliente, updateCliente } from "../api/api.js";

export default function Clientes(){
  const [clientes, setClientes] = useState([]);
  const [editingCliente, setEditingCliente] = useState(null); // Estado para el modal

  async function load(){
    const res = await getClientes();
    setClientes(res.data || []);
  }

  useEffect(()=>{ load(); }, []);

  // Crear
  async function handleCreate(data){
    await createCliente(data);
    load();
  }

  // Eliminar (Con manejo de errores básico)
  async function handleDelete(id){
    try {
        await deleteCliente(id);
        load();
    } catch (error) {
        alert("No se puede eliminar el cliente. Probablemente tenga alquileres o reservas asociados.");
    }
  }

  // Editar
  async function handleUpdate(data) {
    await updateCliente(editingCliente.id_cliente, data);
    setEditingCliente(null);
    load();
  }

  return (
    <div className="page">
      <h2>Clientes</h2>
      
      {/* Formulario de Creación */}
      <ClienteForm onSubmit={handleCreate}/>

      <hr />

      {/* Modal de Edición */}
      {editingCliente && (
        <div className="modal-overlay">
          <div className="modal-content">
            <ClienteForm 
                initialData={editingCliente} 
                onSubmit={handleUpdate} 
                onCancel={() => setEditingCliente(null)}
            />
          </div>
        </div>
      )}

      {/* Lista */}
      <ClienteList 
        items={clientes} 
        onDelete={handleDelete} 
        onEdit={setEditingCliente} // Al hacer click, guardamos el cliente en el estado
      />

      
    </div>
  );
}