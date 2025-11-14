import { useState } from "react";
import Clientes from "./pages/Clientes";
import Vehiculos from "./pages/Vehiculos";
import Alquileres from "./pages/Alquileres";
import Reservas from "./pages/Reservas";
import Dashboard from "./pages/Dashboard";

export default function App(){
  const [view, setView] = useState("dashboard");
  return (
    <div className="app">
      <header className="header">
        <h1>AlquilaYa</h1>
        <nav>
          <button onClick={()=>setView("dashboard")}>Dashboard</button>
          <button onClick={()=>setView("clientes")}>Clientes</button>
          <button onClick={()=>setView("vehiculos")}>Vehículos</button>
          <button onClick={()=>setView("alquileres")}>Alquileres</button>
          <button onClick={()=>setView("reservas")}>Reservas</button>
        </nav>
      </header>
      <main>
        {view === "dashboard" && <Dashboard />}
        {view === "clientes" && <Clientes />}
        {view === "vehiculos" && <Vehiculos />}
        {view === "alquileres" && <Alquileres />}
        {view === "reservas" && <Reservas />}
      </main>
    </div>
  );
}
