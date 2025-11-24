import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: { "Content-Type": "application/json" }
});

// INTERCEPTOR para manejar errores
API.interceptors.response.use(
  response => response, 

  error => {
    // Error del backend con JSON { error: "mensaje" }
    if (error.response && error.response.data) {
      return Promise.resolve({ data: null, error: error.response.data.error });
    }

    // Error inesperado (servidor caído, red, etc.)
    return Promise.resolve({ data: null, error: "Error de red o servidor." });
  }
);

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
export const deleteCliente = (id) => API.put(`/clientes/${id}/delete`);

// Vehículos
export const getVehiculos = () => API.get("/vehiculos/");
export const getVehiculo = (id) => API.get(`/vehiculos/${id}`);
export const createVehiculo = (payload) => API.post("/vehiculos/", payload);
export const updateVehiculo = (id, payload) => API.put(`/vehiculos/${id}`, payload);
export const deleteVehiculo = (id) => API.delete(`/vehiculos/${id}`);

// Alquileres
export const getAlquileres = () => API.get("/alquileres/");
export const createAlquiler = (payload) => API.post("/alquileres/", payload);
export const devolverAlquiler = (id) => API.post(`/alquileres/${id}/devolver`);
export const deleteAlquiler = (id) => API.post(`/alquileres/${id}/delete`);
export const updateAlquiler = (id, payload) => API.put(`/alquileres/${id}`, payload);

// Empleados
export const createEmpleado = (payload) => API.post("/empleados/", payload);
export const updateEmpleado = (id, payload) => API.put(`/empleados/${id}`, payload);
export const deleteEmpleado = (id) => API.put(`/empleados/${id}/delete`);
export const getEmpleados = () => API.get("/empleados/");

// Incidentes
export const createDanio = (payload) => API.post("/danios/", payload);
export const createMulta = (payload) => API.post("/multas/", payload);
export const getDanios = () => API.get("/danios/");
export const getMultas = () => API.get("/multas/");

// Facturas
export const getFacturaByAlquiler = (id_alquiler) => API.get(`/facturas/alquiler/${id_alquiler}`);


