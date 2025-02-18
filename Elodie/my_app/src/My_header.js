import React from "react";
import "./css/My_header.css";

const My_header = () => {
  return (
    <header className="my-header">
      <div className="header-container">
        <h1 className="header-title">Scribio</h1>
        <nav className="header-nav">
          {/* <a href="/" className="nav-link">Accueil</a>
          <a href="#predictions" className="nav-link">Prédictions</a>
          <a href="#contact" className="nav-link">Contact</a> */}
        </nav>
      </div>
    </header>
  );
};

export default My_header;
