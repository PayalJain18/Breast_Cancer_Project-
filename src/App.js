import React, { useState } from "react";
import Card from "./components/card";
import Button from "./components/button";
import Input from "./components/input";

const BreastCancerPredictor = () => {
  const [formData, setFormData] = useState({});
  const [result, setResult] = useState(null);

  const featureNames = [
    "mean radius", "mean texture", "mean perimeter", "mean area", "mean smoothness", 
    "mean compactness", "mean concavity", "mean concave points", "mean symmetry", "mean fractal dimension",
    "radius error", "texture error", "perimeter error", "area error", "smoothness error",
    "compactness error", "concavity error", "concave points error", "symmetry error", "fractal dimension error",
    "worst radius", "worst texture", "worst perimeter", "worst area", "worst smoothness",
    "worst compactness", "worst concavity", "worst concave points", "worst symmetry", "worst fractal dimension"
  ];

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch("http://localhost:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input_data: Object.values(formData).map(Number) })
    });
    const data = await response.json();
    setResult(data.prediction);
  };

  return (
    <Card>
      <div className="p-6 max-w-xl mx-auto">
        <h2 className="text-xl font-bold mb-4">Breast Cancer Predictor</h2>
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-2 gap-2">
            {featureNames.map((feature, index) => (
              <Input
                key={index}
                type="number"
                name={index}
                placeholder={feature}
                onChange={handleChange}
                required
              />
            ))}
          </div>
          <Button type="submit">Predict</Button>
        </form>
        {result !== null && (
          <p className="mt-4 text-lg font-semibold">
            Prediction: {result === 0 ? "Malignant" : "Benign"}
          </p>
        )}
      </div>
    </Card>
  );
};

export default BreastCancerPredictor;
