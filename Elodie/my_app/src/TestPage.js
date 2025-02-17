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
          "Content-Type": "application/json"
        }
      });

      const result = await response.json();
      console.log("Réponse de l'API:", result);

      // Ajout des données récupérées dans l'état
      if (result) {
        setPredictions((prev) => [
          { ...result }, // Ajoute les nouvelles données en haut du tableau
          ...prev, // Ajoute l'état précédent en dessous
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
        onMouseOver={(e) => (e.target.style.backgroundColor = "rgb(72, 72, 145)")}
        onMouseOut={(e) => (e.target.style.backgroundColor = "rgb(42, 42, 78)")}
      >
        {loading ? "Chargement..." : "Obtenir une prédiction"}
      </button>

      {predictions.length > 0 && (
        <table
          style={{
            marginTop: "45px",
            width: "100%",
            borderCollapse: "collapse",
            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
          }}
        >
          <thead>
            <tr style={{ backgroundColor: "rgb(42, 42, 78)", color: "white" }}>
              <th style={tableHeaderStyle}>Label</th>
              <th style={tableHeaderStyle}>Prédiction</th>
              <th style={tableHeaderStyle}>Image</th>
              <th style={tableHeaderStyle}>Maj</th>
              <th style={tableHeaderStyle}>Min</th>
              <th style={tableHeaderStyle}>Nbr</th>
              <th style={tableHeaderStyle}>A</th>
              <th style={tableHeaderStyle}>B</th>
              <th style={tableHeaderStyle}>C</th>
              <th style={tableHeaderStyle}>D</th>
              <th style={tableHeaderStyle}>E</th>
              <th style={tableHeaderStyle}>F</th>
              <th style={tableHeaderStyle}>G</th>
              <th style={tableHeaderStyle}>H</th>
              <th style={tableHeaderStyle}>I</th>
              <th style={tableHeaderStyle}>J</th>
              <th style={tableHeaderStyle}>K</th>
              <th style={tableHeaderStyle}>L</th>
              <th style={tableHeaderStyle}>M</th>
              <th style={tableHeaderStyle}>N</th>
              <th style={tableHeaderStyle}>O</th>
              <th style={tableHeaderStyle}>P</th>
              <th style={tableHeaderStyle}>Q</th>
              <th style={tableHeaderStyle}>R</th>
              <th style={tableHeaderStyle}>S</th>
              <th style={tableHeaderStyle}>T</th>
              <th style={tableHeaderStyle}>U</th>
              <th style={tableHeaderStyle}>V</th>
              <th style={tableHeaderStyle}>W</th>
              <th style={tableHeaderStyle}>X</th>
              <th style={tableHeaderStyle}>Y</th>
              <th style={tableHeaderStyle}>Z</th>
              <th style={tableHeaderStyle}>a</th>
              <th style={tableHeaderStyle}>b</th>
              <th style={tableHeaderStyle}>c</th>
              <th style={tableHeaderStyle}>d</th>
              <th style={tableHeaderStyle}>e</th>
              <th style={tableHeaderStyle}>f</th>
              <th style={tableHeaderStyle}>g</th>
              <th style={tableHeaderStyle}>h</th>
              <th style={tableHeaderStyle}>i</th>
              <th style={tableHeaderStyle}>j</th>
              <th style={tableHeaderStyle}>k</th>
              <th style={tableHeaderStyle}>l</th>
              <th style={tableHeaderStyle}>m</th>
              <th style={tableHeaderStyle}>n</th>
              <th style={tableHeaderStyle}>o</th>
              <th style={tableHeaderStyle}>p</th>
              <th style={tableHeaderStyle}>q</th>
              <th style={tableHeaderStyle}>r</th>
              <th style={tableHeaderStyle}>s</th>
              <th style={tableHeaderStyle}>t</th>
              <th style={tableHeaderStyle}>u</th>
              <th style={tableHeaderStyle}>v</th>
              <th style={tableHeaderStyle}>w</th>
              <th style={tableHeaderStyle}>x</th>
              <th style={tableHeaderStyle}>y</th>
              <th style={tableHeaderStyle}>z</th>
              <th style={tableHeaderStyle}>0</th>
              <th style={tableHeaderStyle}>1</th>
              <th style={tableHeaderStyle}>2</th>
              <th style={tableHeaderStyle}>3</th>
              <th style={tableHeaderStyle}>4</th>
              <th style={tableHeaderStyle}>5</th>
              <th style={tableHeaderStyle}>6</th>
              <th style={tableHeaderStyle}>7</th>
              <th style={tableHeaderStyle}>8</th>
              <th style={tableHeaderStyle}>9</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map((item, index) => (
              <tr key={index} style={index % 2 === 0 ? rowStyleEven : rowStyleOdd}>
                <td style={cellStyle}>{item.Label}</td>
                <td style={cellStyle}>{item.Prediction}</td>
                <td style={cellStyle}>
                  <img
                    src={item.Image}
                    alt={`Image de prédiction ${item.Label}`}
                    style={{ width: "100px", height: "100px", objectFit: "cover" }}
                  />
                </td>
                <td style={cellStyle}>{item.Maj}</td>
                <td style={cellStyle}>{item.Min}</td>
                <td style={cellStyle}>{item.Nbr}</td>
                <td style={cellStyle}>{item.A}</td>
                <td style={cellStyle}>{item.B}</td>
                <td style={cellStyle}>{item.C}</td>
                <td style={cellStyle}>{item.D}</td>
                <td style={cellStyle}>{item.E}</td>
                <td style={cellStyle}>{item.F}</td>
                <td style={cellStyle}>{item.G}</td>
                <td style={cellStyle}>{item.H}</td>
                <td style={cellStyle}>{item.I}</td>
                <td style={cellStyle}>{item.J}</td>
                <td style={cellStyle}>{item.K}</td>
                <td style={cellStyle}>{item.L}</td>
                <td style={cellStyle}>{item.M}</td>
                <td style={cellStyle}>{item.N}</td>
                <td style={cellStyle}>{item.O}</td>
                <td style={cellStyle}>{item.P}</td>
                <td style={cellStyle}>{item.Q}</td>
                <td style={cellStyle}>{item.R}</td>
                <td style={cellStyle}>{item.S}</td>
                <td style={cellStyle}>{item.T}</td>
                <td style={cellStyle}>{item.U}</td>
                <td style={cellStyle}>{item.V}</td>
                <td style={cellStyle}>{item.W}</td>
                <td style={cellStyle}>{item.X}</td>
                <td style={cellStyle}>{item.Y}</td>
                <td style={cellStyle}>{item.Z}</td>
                <td style={cellStyle}>{item["a"]}</td>
                <td style={cellStyle}>{item["b"]}</td>
                <td style={cellStyle}>{item["c"]}</td>
                <td style={cellStyle}>{item["d"]}</td>
                <td style={cellStyle}>{item["e"]}</td>
                <td style={cellStyle}>{item["f"]}</td>
                <td style={cellStyle}>{item["g"]}</td>
                <td style={cellStyle}>{item["h"]}</td>
                <td style={cellStyle}>{item["i"]}</td>
                <td style={cellStyle}>{item["j"]}</td>
                <td style={cellStyle}>{item["k"]}</td>
                <td style={cellStyle}>{item["l"]}</td>
                <td style={cellStyle}>{item["m"]}</td>
                <td style={cellStyle}>{item["n"]}</td>
                <td style={cellStyle}>{item["o"]}</td>
                <td style={cellStyle}>{item["p"]}</td>
                <td style={cellStyle}>{item["q"]}</td>
                <td style={cellStyle}>{item["r"]}</td>
                <td style={cellStyle}>{item["s"]}</td>
                <td style={cellStyle}>{item["t"]}</td>
                <td style={cellStyle}>{item["u"]}</td>
                <td style={cellStyle}>{item["v"]}</td>
                <td style={cellStyle}>{item["w"]}</td>
                <td style={cellStyle}>{item["x"]}</td>
                <td style={cellStyle}>{item["y"]}</td>
                <td style={cellStyle}>{item["z"]}</td>
                <td style={cellStyle}>{item["0"]}</td>
                <td style={cellStyle}>{item["1"]}</td>
                <td style={cellStyle}>{item["2"]}</td>
                <td style={cellStyle}>{item["3"]}</td>
                <td style={cellStyle}>{item["4"]}</td>
                <td style={cellStyle}>{item["5"]}</td>
                <td style={cellStyle}>{item["6"]}</td>
                <td style={cellStyle}>{item["7"]}</td>
                <td style={cellStyle}>{item["8"]}</td>
                <td style={cellStyle}>{item["9"]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

const tableHeaderStyle = {
  padding: "10px",
  backgroundColor: "#2A2A4E",
  color: "white",
  fontWeight: "bold",
  textAlign: "center",
};

const rowStyleEven = {
  backgroundColor: "#f2f2f2",
};

const rowStyleOdd = {
  backgroundColor: "#ffffff",
};

const cellStyle = {
  padding: "10px",
  border: "1px solid #ddd",
  textAlign: "center",
};

export default TestPage;
