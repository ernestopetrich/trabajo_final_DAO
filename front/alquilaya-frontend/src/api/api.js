import axios from "axios";

// 1. Verificación de seguridad para la URL
const apiUrl = import.meta.env.VITE_API_URL;
console.log("Conectando a API en:", apiUrl); // <--- Mira esto en la consola del navegador (F12)

if (!apiUrl) {
    console.error("¡ERROR CRÍTICO! VITE_API_URL no está definida. Revisa tu archivo .env");
}

const API = axios.create({
  baseURL: apiUrl,
  headers: { "Content-Type": "application/json" }
});

// 2. INTERCEPTOR CORREGIDO
API.interceptors.response.use(
  (response) => {
    // ÉXITO: Devolvemos la respuesta tal cual
    return response;
  },
  (error) => {
    console.error("Error en la API:", error);

    // ERROR: Rechazamos la promesa para que el componente sepa que falló.
    // Esto permite que el try/catch o el .catch() del componente capturen el error.
    if (error.response && error.response.data) {
        return Promise.reject(error.response.data); // Devuelve el error del backend
    }
    return Promise.reject({ error: "Error de red o servidor no disponible." });
  }
);

// --- Funciones Auxiliares ---

export function localToIso(datetimeLocalStr){
  if(!datetimeLocalStr) return null;
  const s = datetimeLocalStr.replace("T"," ");
  return s.length === 16 ? s + ":00" : s;
}

export function descargarPDF(url) {
    // Aseguramos que la URL no tenga doble slash //
    const cleanBase = apiUrl.endsWith('/') ? apiUrl.slice(0, -1) : apiUrl;
    const cleanPath = url.startsWith('/') ? url : `/${url}`;
    window.open(`${cleanBase}${cleanPath}`, "_blank");
}

// --- Endpoints (Sin cambios, están bien) ---

// Clientes
export const getClientes = () => API.get("/clientes/"); // Ojo con la barra final si tu backend no la espera
export const getCliente = (id) => API.get(`/clientes/${id}`);
export const createCliente = (payload) => API.post("/clientes/", payload);
export const updateCliente = (id, payload) => API.put(`/clientes/${id}`, payload);
export const deleteCliente = (id) => API.put(`/clientes/${id}/delete`);

// Vehículos
export const getVehiculos = () => API.get("/vehiculos/");
export const getVehiculo = (id) => API.get(`/vehiculos/${id}`);
export const createVehiculo = (payload) => API.post("/vehiculos/", payload);
export const updateVehiculo = (id, payload) => API.put(`/vehiculos/${id}`, payload);
export const deleteVehiculo = (id) => API.put(`/vehiculos/${id}/delete`);

// Alquileres
export const getAlquileres = () => API.get("/alquileres/");
export const createAlquiler = (payload) => API.post("/alquileres/", payload);
// ESTADOS
export const confirmarAlquiler = (id) => API.post(`/alquileres/${id}/confirmar`);
export const iniciarAlquiler = (id) => API.post(`/alquileres/${id}/iniciar`);
export const devolverAlquiler = (id) => API.post(`/alquileres/${id}/devolver`);
export const deleteAlquiler = (id) => API.post(`/alquileres/${id}/delete`); // Nota: aquí usas POST, asegúrate que el backend lo espera así
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