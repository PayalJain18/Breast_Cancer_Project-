import React from "react";

const Button = ({ children, ...props }) => (
  <button className="mt-4 w-full bg-blue-500 text-white py-2 px-4 rounded" {...props}>
    {children}
  </button>
);

export default Button;
