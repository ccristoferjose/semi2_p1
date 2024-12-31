import React from "react";
import { AppBar, Toolbar, Typography } from "@mui/material";

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" style={{ flexGrow: 1 }}>
          Power BI Dashboards
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
