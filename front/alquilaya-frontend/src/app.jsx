// src/app.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";

import Dashboard from "./pages/Dashboard.jsx";
import Clientes from "./pages/Clientes.jsx";
import Vehiculos from "./pages/Vehiculos.jsx";
import Alquileres from "./pages/Alquileres.jsx";
import Inicio from "./pages/Inicio.jsx";


export default function App() {
  return (
    <Router>
      <header className="topnav">
        <div className="nav-left">
          <span className="logo">🚗 AlquilaYa</span>
        </div>

        <nav className="nav-links">
          <NavLink to="/" end className="nav-item">Inicio</NavLink>

          <NavLink to="/dashboard" end className="nav-item">
            Dashboard
          </NavLink>
          <NavLink to="/alquileres" className="nav-item">
            Alquileres
          </NavLink>
          <NavLink to="/vehiculos" className="nav-item">
            Vehículos
          </NavLink>
          <NavLink to="/clientes" className="nav-item">
            Clientes
          </NavLink>
        </nav>
      </header>

      <main className="main-content">

        <Routes>
          <Route path="/" element={<Inicio />} />

          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/alquileres" element={<Alquileres />} />
          <Route path="/vehiculos" element={<Vehiculos />} />
          <Route path="/clientes" element={<Clientes />} />
        </Routes>

      </main>
    </Router>
  );
}
