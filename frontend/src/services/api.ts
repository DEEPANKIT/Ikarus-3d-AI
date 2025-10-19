import axios, { AxiosInstance, AxiosResponse } from "axios";
import {
  Product,
  RecommendationRequest,
  RecommendationResponse,
  AnalyticsData,
  ApiResponse,
  SearchFilters,
  PaginationParams,
} from "../types";

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000",
      timeout: 10000,
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        console.log(
          `API Request: ${config.method?.toUpperCase()} ${config.url}`
        );
        return config;
      },
      (error) => {
        console.error("API Request Error:", error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response: AxiosResponse) => {
        console.log(`API Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error) => {
        console.error("API Response Error:", error);
        return Promise.reject(error);
      }
    );
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.api.get("/health");
      return response.status === 200;
    } catch (error) {
      console.error("Health check failed:", error);
      return false;
    }
  }

  // Test backend connection
  async testBackend(): Promise<any> {
    try {
      const response = await this.api.get("/api/v1/test");
      return response.data;
    } catch (error) {
      console.error("Backend test failed:", error);
      throw error;
    }
  }

  // Get sample products
  async getSampleProducts(): Promise<any> {
    try {
      const response = await this.api.get("/api/v1/products/sample");
      return response.data;
    } catch (error) {
      console.error("Failed to get sample products:", error);
      throw error;
    }
  }

  // Generate AI description
  async generateAIDescription(
    productId: string,
    productData: any
  ): Promise<any> {
    try {
      const response = await this.api.post(
        `/api/v1/products/${productId}/generate-description`,
        productData
      );
      return response.data;
    } catch (error) {
      console.error("Failed to generate AI description:", error);
      throw error;
    }
  }

  // Get analytics overview
  async getAnalyticsOverview(): Promise<any> {
    try {
      const response = await this.api.get("/api/v1/analytics/overview");
      return response.data;
    } catch (error) {
      console.error("Failed to get analytics overview:", error);
      throw error;
    }
  }

  // Get analytics summary
  async getAnalyticsSummary(): Promise<any> {
    try {
      const response = await this.api.get("/api/v1/analytics/summary");
      return response.data;
    } catch (error) {
      console.error("Failed to get analytics summary:", error);
      throw error;
    }
  }

  // Get product recommendations
  async getRecommendations(
    request: RecommendationRequest
  ): Promise<RecommendationResponse> {
    try {
      const response = await this.api.post<ApiResponse<RecommendationResponse>>(
        "/api/v1/recommendations",
        request
      );
      return response.data.data;
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      throw new Error("Failed to fetch recommendations");
    }
  }

  // Get analytics data
  async getAnalytics(): Promise<AnalyticsData> {
    try {
      const response = await this.api.get<ApiResponse<AnalyticsData>>(
        "/api/v1/analytics"
      );
      return response.data.data;
    } catch (error) {
      console.error("Error fetching analytics:", error);
      throw new Error("Failed to fetch analytics data");
    }
  }

  // Get all products with filters and pagination
  async getProducts(
    filters?: SearchFilters,
    pagination?: PaginationParams
  ): Promise<{ products: Product[]; total: number }> {
    try {
      const params = new URLSearchParams();

      if (filters) {
        if (filters.categories) {
          filters.categories.forEach((cat) => params.append("categories", cat));
        }
        if (filters.brands) {
          filters.brands.forEach((brand) => params.append("brands", brand));
        }
        if (filters.materials) {
          filters.materials.forEach((material) =>
            params.append("materials", material)
          );
        }
        if (filters.countries) {
          filters.countries.forEach((country) =>
            params.append("countries", country)
          );
        }
        if (filters.price_min !== undefined) {
          params.append("price_min", filters.price_min.toString());
        }
        if (filters.price_max !== undefined) {
          params.append("price_max", filters.price_max.toString());
        }
      }

      if (pagination) {
        params.append("page", pagination.page.toString());
        params.append("limit", pagination.limit.toString());
        if (pagination.sort_by) {
          params.append("sort_by", pagination.sort_by);
        }
        if (pagination.sort_order) {
          params.append("sort_order", pagination.sort_order);
        }
      }

      const response = await this.api.get<
        ApiResponse<{ products: Product[]; total: number }>
      >(`/api/v1/products?${params.toString()}`);
      return response.data.data;
    } catch (error) {
      console.error("Error fetching products:", error);
      throw new Error("Failed to fetch products");
    }
  }

  // Get single product by ID
  async getProduct(id: string): Promise<Product> {
    try {
      const response = await this.api.get<ApiResponse<Product>>(
        `/api/v1/products/${id}`
      );
      return response.data.data;
    } catch (error) {
      console.error("Error fetching product:", error);
      throw new Error("Failed to fetch product");
    }
  }

  // Search products
  async searchProducts(
    query: string,
    filters?: SearchFilters,
    pagination?: PaginationParams
  ): Promise<{ products: Product[]; total: number }> {
    try {
      const params = new URLSearchParams();
      params.append("q", query);

      if (filters) {
        if (filters.categories) {
          filters.categories.forEach((cat) => params.append("categories", cat));
        }
        if (filters.brands) {
          filters.brands.forEach((brand) => params.append("brands", brand));
        }
        if (filters.materials) {
          filters.materials.forEach((material) =>
            params.append("materials", material)
          );
        }
        if (filters.countries) {
          filters.countries.forEach((country) =>
            params.append("countries", country)
          );
        }
        if (filters.price_min !== undefined) {
          params.append("price_min", filters.price_min.toString());
        }
        if (filters.price_max !== undefined) {
          params.append("price_max", filters.price_max.toString());
        }
      }

      if (pagination) {
        params.append("page", pagination.page.toString());
        params.append("limit", pagination.limit.toString());
        if (pagination.sort_by) {
          params.append("sort_by", pagination.sort_by);
        }
        if (pagination.sort_order) {
          params.append("sort_order", pagination.sort_order);
        }
      }

      const response = await this.api.get<
        ApiResponse<{ products: Product[]; total: number }>
      >(`/api/v1/search?${params.toString()}`);
      return response.data.data;
    } catch (error) {
      console.error("Error searching products:", error);
      throw new Error("Failed to search products");
    }
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;
