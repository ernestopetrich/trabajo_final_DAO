import React from "react";
import { Link } from "react-router-dom";

export default function Inicio() {
  return (
    <section className="hero">
      <div className="hero-overlay"></div>

      <div className="hero-content">
        <h1>AlquilaYa</h1>
        <p>La forma más rápida y moderna de gestionar tus alquileres.</p>

        <div className="hero-buttons">
          <Link to="/dashboard" className="hero-btn secondary">
            Ir al panel
          </Link>
        </div>
      </div>
    </section>
  );
}
