import React, { useState, useEffect, useCallback } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Alert,
} from "@mui/material";
import { Search as SearchIcon } from "@mui/icons-material";
import apiService from "../services/api";

interface Product {
  id: string;
  title: string;
  brand: string;
  price: string;
  description: string;
  image: string;
  categories: string | string[];
  material?: string;
  ai_description?: string;
}

const RecommendationPage: React.FC = () => {
  const [query, setQuery] = useState("");
  const [recommendations, setRecommendations] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState<string>("checking");
  const [error, setError] = useState<string | null>(null);
  const [generatingAI, setGeneratingAI] = useState<Set<string>>(new Set());

  const testBackendConnection = useCallback(async () => {
    try {
      const isHealthy = await apiService.healthCheck();
      if (isHealthy) {
        setBackendStatus("connected");
        await loadSampleProducts();
      } else {
        setBackendStatus("disconnected");
      }
    } catch (error) {
      setBackendStatus("disconnected");
      console.error("Backend connection failed:", error);
    }
  }, []);

  useEffect(() => {
    // Test backend connection and load sample products
    testBackendConnection();
  }, [testBackendConnection]);

  const loadSampleProducts = async () => {
    try {
      console.log("Loading sample products...");
      const response = await apiService.getSampleProducts();
      console.log("Sample products response:", response);
      console.log(
        "Image URLs:",
        response.products?.map((p: any) => p.image)
      );
      setRecommendations(response.products || []);
    } catch (error) {
      console.error("Failed to load sample products:", error);
      setError("Failed to load products. Please check backend connection.");
    }
  };

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      console.log("Searching for:", query);
      // For now, filter existing products based on query
      const response = await apiService.getSampleProducts();
      const allProducts = response.products || [];

      console.log("All products:", allProducts);

      const filteredProducts = allProducts.filter(
        (product: any) =>
          product.title.toLowerCase().includes(query.toLowerCase()) ||
          product.description.toLowerCase().includes(query.toLowerCase()) ||
          product.material.toLowerCase().includes(query.toLowerCase())
      );

      console.log("Filtered products:", filteredProducts);
      setRecommendations(filteredProducts);
    } catch (error) {
      setError("Failed to get recommendations. Please try again.");
      console.error("Search error:", error);
    } finally {
      setLoading(false);
    }
  };

  const generateAIDescription = async (product: Product) => {
    if (product.ai_description) return; // Already generated

    setGeneratingAI((prev) => new Set(prev).add(product.id));

    try {
      const response = await apiService.generateAIDescription(product.id, {
        title: product.title,
        brand: product.brand,
        material: product.material,
        categories: product.categories,
        price: product.price,
        description: product.description,
      });

      // Update the product with AI description
      setRecommendations((prev) =>
        prev.map((p) =>
          p.id === product.id
            ? { ...p, ai_description: response.ai_description }
            : p
        )
      );
    } catch (error) {
      console.error("Failed to generate AI description:", error);
    } finally {
      setGeneratingAI((prev) => {
        const newSet = new Set(prev);
        newSet.delete(product.id);
        return newSet;
      });
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        AI-Powered Product Recommendations
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 4 }}>
        Describe what you're looking for and get personalized furniture
        recommendations
      </Typography>

      {/* Backend Status Indicator */}
      {backendStatus === "checking" && (
        <Alert severity="info" sx={{ mb: 2 }}>
          Checking backend connection...
        </Alert>
      )}
      {backendStatus === "connected" && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Backend connected! Ready to provide recommendations.
        </Alert>
      )}
      {backendStatus === "disconnected" && (
        <Alert severity="warning" sx={{ mb: 2 }}>
          Backend disconnected. Some features may not work properly.
        </Alert>
      )}

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 3, mb: 4 }}>
        <Box sx={{ display: "flex", gap: 2, alignItems: "flex-end" }}>
          <TextField
            fullWidth
            label="What are you looking for?"
            placeholder="e.g., Modern black leather sofa for living room"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            multiline
            rows={2}
            variant="outlined"
          />
          <Button
            variant="contained"
            size="large"
            onClick={handleSearch}
            disabled={loading || !query.trim()}
            startIcon={
              loading ? <CircularProgress size={20} /> : <SearchIcon />
            }
          >
            {loading ? "Searching..." : "Find Products"}
          </Button>
        </Box>
      </Paper>

      {recommendations.length > 0 && (
        <Box>
          <Typography variant="h5" gutterBottom>
            Recommended Products
          </Typography>
          <Grid container spacing={3}>
            {recommendations.map((product) => (
              <Grid item xs={12} sm={6} md={4} key={product.id}>
                <Card>
                  <Box
                    sx={{
                      height: 200,
                      backgroundColor: "#e3f2fd",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      position: "relative",
                      overflow: "hidden",
                    }}
                  >
                    <img
                      src={product.image}
                      alt={product.title}
                      style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        position: "absolute",
                        top: 0,
                        left: 0,
                      }}
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.style.display = "none";
                        // Show fallback text
                        const parent = target.parentElement;
                        if (parent) {
                          parent.innerHTML = `
                            <div style="
                              display: flex;
                              flex-direction: column;
                              align-items: center;
                              justify-content: center;
                              height: 100%;
                              color: #666;
                              font-family: Arial, sans-serif;
                              text-align: center;
                              padding: 20px;
                            ">
                              <div style="font-size: 24px; margin-bottom: 8px;">📦</div>
                              <div style="font-size: 14px; font-weight: bold;">${
                                product.brand
                              }</div>
                              <div style="font-size: 12px;">${
                                product.material || "Product"
                              }</div>
                            </div>
                          `;
                        }
                      }}
                    />
                  </Box>
                  <CardContent>
                    <Typography variant="h6" component="h2" noWrap>
                      {product.title}
                    </Typography>
                    <Typography color="text.secondary" gutterBottom>
                      {product.brand}
                    </Typography>
                    <Typography variant="h6" color="primary">
                      {product.price}
                    </Typography>

                    {/* AI Generated Description */}
                    <Box sx={{ mt: 2 }}>
                      {product.ai_description ? (
                        <Box>
                          <Typography
                            variant="subtitle2"
                            color="primary"
                            gutterBottom
                          >
                            🤖 AI Generated Description
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {product.ai_description}
                          </Typography>
                        </Box>
                      ) : (
                        <Button
                          variant="outlined"
                          size="small"
                          onClick={() => generateAIDescription(product)}
                          disabled={generatingAI.has(product.id)}
                          startIcon={
                            generatingAI.has(product.id) ? (
                              <CircularProgress size={16} />
                            ) : null
                          }
                        >
                          {generatingAI.has(product.id)
                            ? "Generating..."
                            : "Generate AI Description"}
                        </Button>
                      )}
                    </Box>

                    <Box sx={{ mt: 1 }}>
                      {(Array.isArray(product.categories)
                        ? product.categories
                        : product.categories.split(", ")
                      )
                        .slice(0, 3)
                        .map((category: string) => (
                          <Chip
                            key={category}
                            label={category.trim()}
                            size="small"
                            sx={{ mr: 0.5, mb: 0.5 }}
                          />
                        ))}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {recommendations.length === 0 && !loading && query && (
        <Box sx={{ textAlign: "center", py: 4 }}>
          <Typography variant="h6" color="text.secondary">
            No recommendations found. Try a different search term.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default RecommendationPage;
