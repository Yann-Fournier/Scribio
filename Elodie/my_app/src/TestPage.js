import React, { useState } from "react";

const TestPage = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const result = await response.json();
      console.log("Réponse de l'API:", result);

      if (result.Prediction && result.Label) {
        // Ajoute la nouvelle prédiction à la liste existante
        setPredictions((prev) => [
          ...prev,
          { label: result.Label, prediction: result.Prediction },
        ]);
      } else {
        alert("Erreur dans la prédiction");
      }
    } catch (error) {
      console.error("Erreur lors de l'envoi de la requête:", error);
    } finally {
      setLoading(false);
    }
  };

  // Fonction de réinitialisation du tableau
  const handleReset = () => {
    setPredictions([]); // Réinitialise les prédictions
  };

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <button
        onClick={handleSubmit}
        style={{
          padding: "15px 30px",
          marginTop: "55px",
          fontSize: "18px",
          backgroundColor: "rgb(42, 42, 78)",
          color: "white",
          border: "none",
          borderRadius: "15px",
          cursor: "pointer",
          boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
          transition: "background-color 0.3s",
        }}
        onMouseOver={(e) =>
          (e.target.style.backgroundColor = "rgb(72, 72, 145)")
        }
        onMouseOut={(e) =>
          (e.target.style.backgroundColor = "rgb(42, 42, 78)")
        }
      >
        {loading ? "Chargement..." : "Obtenir une prédiction"}
      </button>

      {predictions.length > 0 && (
        <>
          <table
            style={{
              marginTop: "45px",
              width: "100%",
              borderCollapse: "collapse",
              boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
            }}
          >
            <thead>
              <tr
                style={{
                  backgroundColor: "rgb(42, 42, 78)",
                  color: "white",
                }}
              >
                <th style={tableHeaderStyle}>Label</th>
                <th style={tableHeaderStyle}>Prédiction</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map((item, index) => (
                <tr
                  key={index}
                  style={index % 2 === 0 ? rowStyleEven : rowStyleOdd}
                >
                  <td style={cellStyle}>{item.label}</td>
                  <td style={cellStyle}>{item.prediction}</td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Bouton Reset */}
          <button
            onClick={handleReset}
            style={{
              padding: "10px 20px",
              marginTop: "20px",
              fontSize: "16px",
              backgroundColor: "#d9534f",
              color: "white",
              border: "none",
              borderRadius: "10px",
              cursor: "pointer",
              boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
              transition: "background-color 0.3s",
            }}
            onMouseOver={(e) =>
              (e.target.style.backgroundColor = "#c9302c")
            }
            onMouseOut={(e) => (e.target.style.backgroundColor = "#d9534f")}
          >
            Réinitialiser le tableau
          </button>
        </>
      )}
    </div>
  );
};

const tableHeaderStyle = {
  padding: "15px",
  fontSize: "18px",
  fontWeight: "bold",
  textAlign: "center",
};

const cellStyle = {
  padding: "15px",
  border: "1px solid #ddd",
  textAlign: "center",
  fontSize: "18px",
};

const rowStyleEven = {
  backgroundColor: "#f9f9f9",
};

const rowStyleOdd = {
  backgroundColor: "#ffffff",
};

export default TestPage;
