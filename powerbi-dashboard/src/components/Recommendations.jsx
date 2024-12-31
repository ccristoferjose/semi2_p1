import React from "react";

const Recommendations = () => {
  const recommendations = [
    "Enfocar recursos en departamentos con mayor impacto, como Guatemala y Quetzaltenango.",
    "Monitorear la variación diaria de muertes y mejorar la calidad del reporte de datos.",
    "Ampliar la cobertura de salud en departamentos con menos casos, como Huehuetenango y Petén.",
    "Fortalecer las medidas sanitarias en periodos críticos identificados en el análisis, como mayo 2020.",
    "Realizar análisis más profundos a nivel municipal para identificar focos específicos de vulnerabilidad.",
    "Añadir segmentadores interactivos en el dashboard para analizar tasas de mortalidad por población y densidad.",
    "Comparar tasas de mortalidad departamentales con la nacional y global para identificar prioridades.",
    "Fortalecer campañas de prevención en áreas con menor acceso a servicios de salud."
  ];

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Recomendaciones</h2>
      <ul>
        {recommendations.map((rec, index) => (
          <li key={index}>{rec}</li>
        ))}
      </ul>
    </div>
  );
};

export default Recommendations;
