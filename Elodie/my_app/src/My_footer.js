import React from "react";
import "./css/My_footer.css";

const My_footer = () => {
  return (
    <footer className="my-footer">
      <p>&copy; {new Date().getFullYear()} Scribio. Tous droits réservés.</p>
    </footer>
  );
};

export default My_footer;
