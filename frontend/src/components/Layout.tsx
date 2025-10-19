import React from "react";
import { AppBar, Toolbar, Typography, Container, Box } from "@mui/material";
import { useNavigate, useLocation } from "react-router-dom";
import { Button } from "@mui/material";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const navigationItems = [
    { label: "Recommendations", path: "/recommendations" },
    { label: "Analytics", path: "/analytics" },
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography
            variant="h6"
            component="div"
            sx={{ flexGrow: 1, cursor: "pointer" }}
            onClick={() => navigate("/")}
          >
            Ikarus 3D
          </Typography>
          {navigationItems.map((item) => (
            <Button
              key={item.path}
              color="inherit"
              onClick={() => navigate(item.path)}
              sx={{
                mx: 1,
                backgroundColor:
                  location.pathname === item.path
                    ? "rgba(255,255,255,0.1)"
                    : "transparent",
              }}
            >
              {item.label}
            </Button>
          ))}
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        {children}
      </Container>
    </Box>
  );
};

export default Layout;



