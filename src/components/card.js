import React from "react";

const Card = ({ children }) => (
  <div className="p-6 max-w-xl mx-auto mt-10 bg-white shadow-md rounded-lg">
    {children}
  </div>
);

export default Card;
