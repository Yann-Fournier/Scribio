import React, { useState, useEffect } from "react";
import axios from "axios";
import './Api.css';

const TestPage = () => {
  const [data, setData] = useState([]);  // Pour stocker les données reçues
  const [loading, setLoading] = useState(true);  // Indicateur de chargement
  const [error, setError] = useState(null);  // Pour afficher les erreurs éventuelles

  useEffect(() => {
    // Fonction pour récupérer les données depuis FastAPI
    axios
      .get("http://localhost:8000/")  // L'URL de votre API FastAPI
      .then((response) => {
        setData(response.data);  // Mettez à jour les données
        setLoading(false);  // Arrêtez le chargement
      })
      .catch((err) => {
        setError(err);  // Si une erreur se produit
        setLoading(false);  // Arrêtez le chargement
      });
  }, []);  // [] indique que l'effet s'exécute uniquement au montage du composant

  if (loading) return <p>Chargement des données...</p>;
  if (error) return <p>Erreur : {error.message}</p>;

  return (
    <div>
      <table border="1">
        <div className="content_api">
            <thead>
            <tr>
                <th>Label</th>
                <th>Repartition</th>
            </tr>
            </thead>
        </div>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item.Label}</td>
              <td>{item.Repartition}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TestPage;
