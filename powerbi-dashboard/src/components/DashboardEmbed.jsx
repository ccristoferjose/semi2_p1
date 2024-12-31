const DashboardEmbed = ({ iframeSrc }) => (
    <iframe
      src={iframeSrc}
      style={{
        width: "100%",
        height: "600px",
        border: "none",
      }}
      title="Power BI Dashboard"
    />
  );
  
  export default DashboardEmbed;
  