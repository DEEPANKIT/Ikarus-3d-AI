// TypeScript type definitions for Ikarus 3D Application

export interface Product {
  id: string;
  title: string;
  brand: string;
  price: string;
  description: string;
  images: string[];
  categories: string[];
  material: string;
  color: string;
  country_of_origin: string;
  manufacturer: string;
  package_dimensions: string;
  uniq_id: string;
}

export interface RecommendationRequest {
  query: string;
  limit?: number;
  filters?: {
    categories?: string[];
    price_range?: [number, number];
    brand?: string[];
    material?: string[];
  };
}

export interface RecommendationResponse {
  recommendations: Product[];
  query: string;
  total_found: number;
  processing_time: number;
}

export interface AnalyticsData {
  total_products: number;
  average_price: number;
  price_range: {
    min: number;
    max: number;
  };
  category_distribution: Array<{
    category: string;
    count: number;
    percentage: number;
  }>;
  brand_distribution: Array<{
    brand: string;
    count: number;
    percentage: number;
  }>;
  material_distribution: Array<{
    material: string;
    count: number;
    percentage: number;
  }>;
  geographic_distribution: Array<{
    country: string;
    count: number;
    percentage: number;
  }>;
  price_distribution: Array<{
    range: string;
    count: number;
  }>;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

export interface SearchFilters {
  categories?: string[];
  price_min?: number;
  price_max?: number;
  brands?: string[];
  materials?: string[];
  countries?: string[];
}

export interface PaginationParams {
  page: number;
  limit: number;
  sort_by?: string;
  sort_order?: "asc" | "desc";
}



