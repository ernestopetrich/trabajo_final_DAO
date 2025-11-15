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
          <button style={{ color: 'black' }} onClick={() => setView("dashboard")}>
            Dashboard
          </button>
          <button style={{ color: 'black' }} onClick={() => setView("clientes")}>
            Clientes
          </button>
          <button style={{ color: 'black' }} onClick={() => setView("vehiculos")}>
            Vehículos
          </button>
          <button style={{ color: 'black' }} onClick={() => setView("alquileres")}>
            Alquileres
          </button>
          <button style={{ color: 'black' }} onClick={() => setView("reservas")}>
            Reservas
          </button>
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
