// import React, { useState } from "react";
// import axios from "axios";

// const Prediction = () => {
//   const [imagePath, setImagePath] = useState("");
//   const [prediction, setPrediction] = useState("");

//   const handlePredict = async () => {
//     try {
//       const response = await axios.post("http://127.0.0.1:8000/predict", {
//         image_path: imagePath,  // On envoie le chemin de l'image
//       });

//       setPrediction(response.data.prediction);  // Récupérer la réponse de l'API
//     } catch (error) {
//       console.error("Erreur lors de la prédiction:", error);
//     }
//   };

//   return (
//     <div>
//       <h2>Prédiction d'image</h2>
//       <input
//         type="text"
//         placeholder="Entrez le chemin de l'image"
//         value={imagePath}
//         onChange={(e) => setImagePath(e.target.value)}
//       />
//       <button onClick={handlePredict}>Prédire</button>
//       {prediction && <h3>Résultat: {prediction}</h3>}
//     </div>
//   );
// };

// export default Prediction;
