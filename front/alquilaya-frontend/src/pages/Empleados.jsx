import React, {useEffect, useState} from "react";
import EmpleadoForm from "../components/EmpleadoForm";
import EmpleadoList from "../components/EmpleadoList";
import { getEmpleados, createEmpleado, updateEmpleado, deleteEmpleado } from "../api/api";

export default function Empleados(){
  const [empleados, setEmpleados] = useState([]);
  const [editingEmpleado, setEditingEmpleado] = useState(null);

  async function load(){
    try {
        const res = await getEmpleados();
        setEmpleados(res.data || []);
    } catch (error) {
        console.error("Error cargando empleados:", error);
    }
  }

  useEffect(()=>{ load(); }, []);

  // CREAR
  async function handleCreate(data){
    try {
        await createEmpleado(data);
        load();
    } catch (error) {
        alert("Error al crear empleado: " + error.message);
    }
  }

  // ELIMINAR
  async function handleDelete(id){
    try {
        await deleteEmpleado(id);
        load();
    } catch (error) {
        alert("No se puede eliminar el empleado. Posiblemente tenga alquileres asociados.");
    }
  }

  // EDITAR
  async function handleUpdate(data) {
    try {
        await updateEmpleado(editingEmpleado.id_empleado, data);
        setEditingEmpleado(null);
        load();
    } catch (error) {
        alert("Error al actualizar empleado: " + error.message);
    }
  }

  return (
    <div className="page">
      <h2>Gestión de Empleados</h2>
      
      {/* Formulario de Creación */}
      <EmpleadoForm onSubmit={handleCreate}/>


    
      <hr />

        {/* Modal de Edición */}
      {editingEmpleado && (
        <div className="modal-overlay">
          <div className="modal-content">
            <EmpleadoForm 
                initialData={editingEmpleado} 
                onSubmit={handleUpdate} 
                onCancel={() => setEditingEmpleado(null)}
            />
          </div>
          <hr/>
        </div>
      )}

      {/* Lista */}
      <EmpleadoList 
        items={empleados} 
        onDelete={handleDelete} 
        onEdit={setEditingEmpleado}
      />
    </div>
  );
}