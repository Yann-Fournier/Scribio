
import './App.css';
import React from "react";
import Webcam from "react-webcam";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import TestPage from "./TestPage";
import My_header from "./My_header";
import My_footer from "./My_footer";

// const videoConstraints = {
//   width: 1280,
//   height: 720,
//   facingMode: "user"
// };

// const WebcamCapture = () => (
//   <Webcam
//     audio={false}
//     height={720}
//     screenshotFormat="image/jpeg"
//     width={1280}
//     videoConstraints={videoConstraints}
//   >
//     {({ getScreenshot }) => (
//       <button
//         onClick={() => {
//           const imageSrc = getScreenshot()
//         }}
//       >
//         Capture photo
//       </button>
//     )}
//   </Webcam>
// );

const App = () => {
  return (
    <Router>
        <Routes>
          <Route path="/" element={<My_header />} />
        </Routes>
        <Routes>
          <Route path="/" element={<TestPage />} />
        </Routes>
      {/* <p className='camera'>
        <WebcamCapture />
      </p> */}
      <p>
        <MyButton />
      </p>
      <Routes>
          <Route path="/" element={<My_footer />} />
        </Routes>
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