import React from "react";

export default function ClienteList({items = [], onDelete}){
  return (
    <div className="card">
      <h3>Listado</h3>
      <table className="table">
        <thead><tr><th>DNI</th><th>Nombre</th><th>Apellido</th><th>Email</th><th>Acciones</th><th>SAAAAS</th></tr></thead>
        <tbody>
          {items.map(c => (
            <tr key={c.id_cliente}>
              <td style={{fontWeight: 'bold', fontFamily: 'monospace'}}>{c.dni}</td>
              <td>{c.nombre}</td>
              <td>{c.apellido}</td>
              <td>{c.email}</td>
              <td><button onClick={()=>onDelete(c.id_cliente)}>Eliminar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
