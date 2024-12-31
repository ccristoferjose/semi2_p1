import React from "react";
import DashboardTitle from "../components/DashboardTitle.jsx";
import DashboardEmbed from "../components/DashboardEmbed";
import Recommendations from "../components/Recommendations";

const Dashboard1 = () => {
  const iframeSrc =
    "https://app.powerbi.com/view?r=eyJrIjoiYjU1YWQ0YzYtNzYyMy00YzdmLTlmNWEtNjE0MGQ4ODg5ZmM2IiwidCI6IjIzYjVhMmVmLTM0OTYtNGEwYy04Y2ExLWI1ODM3OWI3YTQ0YyIsImMiOjR9";

  return (
    <div style={{ padding: "20px" }}>
      <DashboardTitle title="Análisis de Mortalidad y Datos COVID-19 En Guatemala y el Mundo" />
      <DashboardEmbed iframeSrc={iframeSrc} />
      <Recommendations />
    </div>
  );
};

export default Dashboard1;
