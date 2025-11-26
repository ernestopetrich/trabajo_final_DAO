import React, {useEffect, useState} from "react";
import VehiculoForm from "../components/VehiculoForm";
import VehiculoList from "../components/VehiculoList";
import { getVehiculos, createVehiculo, deleteVehiculo, updateVehiculo } from "../api/api";

export default function Vehiculos(){
  const [vehiculos, setVehiculos] = useState([]);

  // Estado para saber si estamos editando (si es null, no editamos)
  const [editingVehiculo, setEditingVehiculo] = useState(null);

  async function load(){ const res = await getVehiculos(); setVehiculos(res.data || []); }
  useEffect(()=>{ load(); }, []);

  async function handleCreate(data){ await createVehiculo(data); load(); }
  async function handleDelete(id){ await deleteVehiculo(id); load(); }

  async function startEdit(vehiculo){
    setEditingVehiculo(vehiculo);
  }

  async function handleUpdate(data){
    // data trae los datos del formulario, editingVehiculo tiene el ID original
    await updateVehiculo(editingVehiculo.id_vehiculo, data);
    setEditingVehiculo(null); // Cerramos el modal
    load(); // Recargamos la lista
  }

  // --- LÓGICA DE MANTENIMIENTO (NUEVO) ---
  async function handleMantenimiento(vehiculo) {
    // Si está disponible, lo mandamos a mantenimiento.
    // Si está en mantenimiento, lo devolvemos a disponible.
    const nuevoEstado = vehiculo.estado === 'mantenimiento' ? 'disponible' : 'mantenimiento';
    
    const mensaje = nuevoEstado === 'mantenimiento' 
        ? `¿Enviar el vehículo ${vehiculo.patente} a mantenimiento?`
        : `¿Habilitar el vehículo ${vehiculo.patente} nuevamente?`;

    if(window.confirm(mensaje)) {
        try {
            await updateVehiculo(vehiculo.id_vehiculo, { estado: nuevoEstado });
            load();
        } catch (error) {
            alert("Error al cambiar estado: " + error.message);
        }
    }
  }



  return (
    <div className="page">
      <h2>Vehículos</h2>
      
      {/* Formulario de Creación (Siempre visible arriba) */}
      <VehiculoForm onSubmit={handleCreate}/>

      <hr />

      {/* --- MODAL DE EDICIÓN --- */}
      {/* Solo se muestra si editingVehiculo TIENE datos */}
      {editingVehiculo && (
        <div className="modal-overlay">
          <div className="modal-content">
            {/* Reutilizamos el mismo formulario, pero le pasamos initialData */}
            <VehiculoForm 
                initialData={editingVehiculo} 
                onSubmit={handleUpdate} 
                onCancel={() => setEditingVehiculo(null)} // Botón cancelar cierra el modal
            />
          </div>
          <hr/>
        </div>
      )}

      {/* Lista */}
      <VehiculoList 
        items={vehiculos} 
        onDelete={handleDelete} 
        onEdit={startEdit} // Pasamos la función de editar
        onMantenimiento={handleMantenimiento}
      />
    </div>
  );
}
