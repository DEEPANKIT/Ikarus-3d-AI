import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { QueryClient, QueryClientProvider } from "react-query";

// Import pages
import RecommendationPage from "./pages/RecommendationPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import ProductDetailPage from "./pages/ProductDetailPage";
import Layout from "./components/Layout";

// Create theme
const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#1976d2",
    },
    secondary: {
      main: "#dc004e",
    },
  },
});

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<RecommendationPage />} />
              <Route path="/recommendations" element={<RecommendationPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/product/:id" element={<ProductDetailPage />} />
            </Routes>
          </Layout>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;



