"""
Ikarus 3D Data Analysis Script
Comprehensive EDA for furniture product dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Any
import json
from collections import Counter
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class IkarusDataAnalyzer:
    """Comprehensive data analysis for Ikarus 3D furniture dataset"""
    
    def __init__(self, data_path: str = "data/raw/intern_data_ikarus.csv"):
        """Initialize analyzer with data path"""
        self.data_path = Path(data_path)
        self.df = None
        self.analysis_results = {}
        
    def load_data(self) -> pd.DataFrame:
        """Load and validate dataset"""
        try:
            logger.info(f"Loading data from {self.data_path}")
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Dataset loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def basic_info(self) -> Dict[str, Any]:
        """Get basic dataset information"""
        logger.info("Analyzing basic dataset information")
        
        info = {
            "shape": self.df.shape,
            "columns": list(self.df.columns),
            "dtypes": self.df.dtypes.to_dict(),
            "missing_values": self.df.isnull().sum().to_dict(),
            "duplicates": self.df.duplicated().sum(),
            "memory_usage": self.df.memory_usage(deep=True).sum()
        }
        
        self.analysis_results["basic_info"] = info
        return info
    
    def price_analysis(self) -> Dict[str, Any]:
        """Analyze price distribution and statistics"""
        logger.info("Analyzing price data")
        
        # Clean price data
        df_price = self.df.copy()
        df_price['price_clean'] = df_price['price'].str.replace('$', '').astype(float)
        
        price_stats = {
            "count": df_price['price_clean'].count(),
            "mean": df_price['price_clean'].mean(),
            "median": df_price['price_clean'].median(),
            "std": df_price['price_clean'].std(),
            "min": df_price['price_clean'].min(),
            "max": df_price['price_clean'].max(),
            "q25": df_price['price_clean'].quantile(0.25),
            "q75": df_price['price_clean'].quantile(0.75),
            "outliers": len(df_price[df_price['price_clean'] > df_price['price_clean'].quantile(0.99)])
        }
        
        self.analysis_results["price_analysis"] = price_stats
        return price_stats
    
    def category_analysis(self) -> Dict[str, Any]:
        """Analyze product categories"""
        logger.info("Analyzing category distribution")
        
        # Parse categories (they're stored as string representations of lists)
        categories = []
        for cat_str in self.df['categories'].dropna():
            try:
                # Clean and parse category string
                cat_list = eval(cat_str) if isinstance(cat_str, str) else cat_str
                categories.extend(cat_list)
            except:
                continue
        
        category_counts = Counter(categories)
        
        category_stats = {
            "total_categories": len(category_counts),
            "top_10_categories": dict(category_counts.most_common(10)),
            "category_distribution": dict(category_counts),
            "avg_categories_per_product": len(categories) / len(self.df)
        }
        
        self.analysis_results["category_analysis"] = category_stats
        return category_stats
    
    def brand_analysis(self) -> Dict[str, Any]:
        """Analyze brand distribution"""
        logger.info("Analyzing brand data")
        
        brand_counts = self.df['brand'].value_counts()
        
        brand_stats = {
            "total_brands": len(brand_counts),
            "top_10_brands": brand_counts.head(10).to_dict(),
            "brand_diversity": len(brand_counts) / len(self.df),
            "most_common_brand": brand_counts.index[0] if len(brand_counts) > 0 else None,
            "brands_with_multiple_products": len(brand_counts[brand_counts > 1])
        }
        
        self.analysis_results["brand_analysis"] = brand_stats
        return brand_stats
    
    def material_analysis(self) -> Dict[str, Any]:
        """Analyze material composition"""
        logger.info("Analyzing material data")
        
        material_counts = self.df['material'].value_counts()
        
        material_stats = {
            "total_materials": len(material_counts),
            "top_materials": material_counts.head(10).to_dict(),
            "material_diversity": len(material_counts) / len(self.df),
            "most_common_material": material_counts.index[0] if len(material_counts) > 0 else None
        }
        
        self.analysis_results["material_analysis"] = material_stats
        return material_stats
    
    def geographic_analysis(self) -> Dict[str, Any]:
        """Analyze country of origin"""
        logger.info("Analyzing geographic distribution")
        
        country_counts = self.df['country_of_origin'].value_counts()
        
        geo_stats = {
            "total_countries": len(country_counts),
            "top_countries": country_counts.head(10).to_dict(),
            "geographic_diversity": len(country_counts) / len(self.df),
            "most_common_country": country_counts.index[0] if len(country_counts) > 0 else None
        }
        
        self.analysis_results["geographic_analysis"] = geo_stats
        return geo_stats
    
    def text_analysis(self) -> Dict[str, Any]:
        """Analyze text content (titles, descriptions)"""
        logger.info("Analyzing text content")
        
        # Title analysis
        title_lengths = self.df['title'].str.len()
        
        # Description analysis
        desc_lengths = self.df['description'].str.len()
        
        text_stats = {
            "title_stats": {
                "avg_length": title_lengths.mean(),
                "min_length": title_lengths.min(),
                "max_length": title_lengths.max(),
                "std_length": title_lengths.std()
            },
            "description_stats": {
                "avg_length": desc_lengths.mean(),
                "min_length": desc_lengths.min(),
                "max_length": desc_lengths.max(),
                "std_length": desc_lengths.std()
            },
            "products_with_descriptions": desc_lengths.notna().sum(),
            "products_without_descriptions": desc_lengths.isna().sum()
        }
        
        self.analysis_results["text_analysis"] = text_stats
        return text_stats
    
    def image_analysis(self) -> Dict[str, Any]:
        """Analyze image data"""
        logger.info("Analyzing image data")
        
        # Parse image URLs
        image_counts = []
        for img_str in self.df['images'].dropna():
            try:
                img_list = eval(img_str) if isinstance(img_str, str) else img_str
                image_counts.append(len(img_list))
            except:
                image_counts.append(0)
        
        image_stats = {
            "products_with_images": len([x for x in image_counts if x > 0]),
            "products_without_images": len([x for x in image_counts if x == 0]),
            "avg_images_per_product": np.mean(image_counts) if image_counts else 0,
            "max_images_per_product": max(image_counts) if image_counts else 0,
            "min_images_per_product": min(image_counts) if image_counts else 0
        }
        
        self.analysis_results["image_analysis"] = image_stats
        return image_stats
    
    def generate_insights(self) -> List[str]:
        """Generate key insights from the analysis"""
        insights = []
        
        # Price insights
        price_data = self.analysis_results.get("price_analysis", {})
        if price_data:
            insights.append(f"Price range: ${price_data.get('min', 0):.2f} - ${price_data.get('max', 0):.2f}")
            insights.append(f"Average price: ${price_data.get('mean', 0):.2f}")
            insights.append(f"Price standard deviation: ${price_data.get('std', 0):.2f}")
        
        # Category insights
        cat_data = self.analysis_results.get("category_analysis", {})
        if cat_data:
            top_cat = list(cat_data.get("top_10_categories", {}).keys())[:3]
            insights.append(f"Top categories: {', '.join(top_cat)}")
        
        # Brand insights
        brand_data = self.analysis_results.get("brand_analysis", {})
        if brand_data:
            insights.append(f"Total brands: {brand_data.get('total_brands', 0)}")
            insights.append(f"Brand diversity: {brand_data.get('brand_diversity', 0):.2%}")
        
        # Material insights
        material_data = self.analysis_results.get("material_analysis", {})
        if material_data:
            top_material = list(material_data.get("top_materials", {}).keys())[:3]
            insights.append(f"Top materials: {', '.join(top_material)}")
        
        return insights
    
    def run_full_analysis(self) -> Dict[str, Any]:
        """Run complete data analysis"""
        logger.info("Starting comprehensive data analysis")
        
        # Load data
        self.load_data()
        
        # Run all analyses
        self.basic_info()
        self.price_analysis()
        self.category_analysis()
        self.brand_analysis()
        self.material_analysis()
        self.geographic_analysis()
        self.text_analysis()
        self.image_analysis()
        
        # Generate insights
        insights = self.generate_insights()
        self.analysis_results["insights"] = insights
        
        logger.info("Data analysis completed successfully")
        return self.analysis_results
    
    def save_results(self, output_path: str = "data/processed/analysis_results.json"):
        """Save analysis results to JSON file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.analysis_results, f, indent=2, default=str)
        
        logger.info(f"Analysis results saved to {output_path}")

def main():
    """Main execution function"""
    analyzer = IkarusDataAnalyzer()
    
    try:
        # Run full analysis
        results = analyzer.run_full_analysis()
        
        # Print key insights
        print("\n" + "="*50)
        print("IKARUS 3D DATASET ANALYSIS RESULTS")
        print("="*50)
        
        insights = results.get("insights", [])
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
        
        print("\n" + "="*50)
        print("Analysis completed successfully!")
        
        # Save results
        analyzer.save_results()
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    main()



