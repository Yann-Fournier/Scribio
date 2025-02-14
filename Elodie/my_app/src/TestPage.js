import React, { useState } from "react";
import axios from "axios";

const TestPage = () => {
    const [prediction, setPrediction] = useState(null);
    
    const handleSubmit = async () => {
      try {
        const response = await fetch('http://localhost:8000/predict', {  
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        const result = await response.json();
        console.log('Réponse de l\'API:', result);
    
        if (result.Prediction && result.Label) {
          // Mettre à jour l'état avec la prédiction et le label reçus
          setPrediction(`Label: ${result.Label}, Prediction: ${result.Prediction}`);
        } else {
          alert("Erreur dans la prédiction");
        }
    
      } catch (error) {
        console.error('Erreur lors de l\'envoi de la requête:', error);
      }
    };
    
    return (
      <div>
        <button onClick={handleSubmit}>Obtenir une prédiction</button>
        {prediction && (
          <div>
            <h2>{prediction}</h2>
          </div>
        )}
      </div>
    );
    
    
  
    return (
      <div>
        <button onClick={handleSubmit}>Obtenir une prédiction</button>
        
        {prediction && (
          <div>
            <h2>Prédiction : {prediction}</h2>
          </div>
        )}
      </div>
    );
  }
export default TestPage;
