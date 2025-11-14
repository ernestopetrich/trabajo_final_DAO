import React from "react";

export default function ClienteList({items = [], onDelete}){
  return (
    <div className="card">
      <h3>Listado</h3>
      <table className="table">
        <thead><tr><th>ID</th><th>Nombre</th><th>DNI</th><th>Acciones</th></tr></thead>
        <tbody>
          {items.map(c => (
            <tr key={c.id_cliente}>
              <td>{c.id_cliente}</td>
              <td>{c.nombre} {c.apellido}</td>
              <td>{c.dni}</td>
              <td><button onClick={()=>onDelete(c.id_cliente)}>Eliminar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
