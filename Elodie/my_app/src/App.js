import "./App.css";
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import TestPage from "./TestPage";
import My_header from "./My_header";
import My_footer from "./My_footer";

const App = () => {
  return (
    <Router>
      {/* Header toujours affiché */}
      <My_header />

      {/* Définition des routes */}
      <Routes>
        <Route path="/" element={<TestPage />} />
      </Routes>

      {/* Footer toujours affiché */}
      <My_footer />
    </Router>
  );
};


function MyButton() {
  return (
    <button>
      I'm a button
    </button>
  );
}

export default App;