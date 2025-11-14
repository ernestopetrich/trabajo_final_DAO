import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: { "Content-Type": "application/json" }
});

export function localToIso(datetimeLocalStr){
  if(!datetimeLocalStr) return null;
  const s = datetimeLocalStr.replace("T"," ");
  // si no tiene segundos, agregar :00
  return s.length === 16 ? s + ":00" : s;
}

// Clientes
export const getClientes = () => API.get("/clientes/");
export const getCliente = (id) => API.get(`/clientes/${id}`);
export const createCliente = (payload) => API.post("/clientes/", payload);
export const updateCliente = (id, payload) => API.put(`/clientes/${id}`, payload);
export const deleteCliente = (id) => API.delete(`/clientes/${id}`);

// Vehículos
export const getVehiculos = () => API.get("/vehiculos/");
export const getVehiculo = (id) => API.get(`/vehiculos/${id}`);
export const createVehiculo = (payload) => API.post("/vehiculos/", payload);
export const updateVehiculo = (id, payload) => API.put(`/vehiculos/${id}`, payload);
export const deleteVehiculo = (id) => API.delete(`/vehiculos/${id}`);

// Reservas
export const getReservas = () => API.get("/reservas/");
export const createReserva = (payload) => API.post("/reservas/", payload);

// Alquileres
export const getAlquileres = () => API.get("/alquileres/");
export const createAlquiler = (payload) => API.post("/alquileres/", payload);
export const createAlquilerFromReserva = (payload) => API.post("/alquileres/reserva", payload);
export const devolverAlquiler = (id) => API.post(`/alquileres/${id}/devolver`);
