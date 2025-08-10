"""
Data loading utilities for M5 forecasting competition.

This module provides functions to load and preprocess all M5 competition datasets.
"""

import os
import pandas as pd
from typing import Dict, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class M5DataLoader:
    """Class to handle loading and basic preprocessing of M5 competition data."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize the data loader.
        
        Args:
            data_dir (str): Path to the directory containing M5 data files
        """
        self.data_dir = data_dir
        self.data_files = {
            'calendar': 'calendar.csv',
            'sales_train_validation': 'sales_train_validation.csv',
            'sales_train_evaluation': 'sales_train_evaluation.csv',
            'sample_submission': 'sample_submission.csv',
            'sell_prices': 'sell_prices.csv'
        }
        
    def _get_file_path(self, filename: str) -> str:
        """Get the full path to a data file."""
        return os.path.join(self.data_dir, filename)
    
    def load_calendar(self) -> pd.DataFrame:
        """
        Load calendar data.
        
        Returns:
            pd.DataFrame: Calendar data with date information and events
        """
        file_path = self._get_file_path(self.data_files['calendar'])
        logger.info(f"Loading calendar data from {file_path}")
        
        calendar = pd.read_csv(file_path)
        
        # Convert date column to datetime
        calendar['date'] = pd.to_datetime(calendar['date'])
        
        # Create additional time features
        calendar['year'] = calendar['date'].dt.year
        calendar['month'] = calendar['date'].dt.month
        calendar['day'] = calendar['date'].dt.day
        calendar['dayofweek'] = calendar['date'].dt.dayofweek
        calendar['quarter'] = calendar['date'].dt.quarter
        calendar['is_weekend'] = calendar['dayofweek'].isin([5, 6]).astype(int)
        
        logger.info(f"Calendar data loaded: {calendar.shape}")
        return calendar
    
    def load_sales_data(self, validation: bool = True) -> pd.DataFrame:
        """
        Load sales training data.
        
        Args:
            validation (bool): If True, load validation data; if False, load evaluation data
            
        Returns:
            pd.DataFrame: Sales training data
        """
        if validation:
            file_key = 'sales_train_validation'
        else:
            file_key = 'sales_train_evaluation'
            
        file_path = self._get_file_path(self.data_files[file_key])
        logger.info(f"Loading sales data from {file_path}")
        
        sales = pd.read_csv(file_path)
        logger.info(f"Sales data loaded: {sales.shape}")
        
        return sales
    
    def load_prices(self) -> pd.DataFrame:
        """
        Load sell prices data.
        
        Returns:
            pd.DataFrame: Price data for items across stores and weeks
        """
        file_path = self._get_file_path(self.data_files['sell_prices'])
        logger.info(f"Loading price data from {file_path}")
        
        prices = pd.read_csv(file_path)
        logger.info(f"Price data loaded: {prices.shape}")
        
        return prices
    
    def load_sample_submission(self) -> pd.DataFrame:
        """
        Load sample submission file.
        
        Returns:
            pd.DataFrame: Sample submission format
        """
        file_path = self._get_file_path(self.data_files['sample_submission'])
        logger.info(f"Loading sample submission from {file_path}")
        
        submission = pd.read_csv(file_path)
        logger.info(f"Sample submission loaded: {submission.shape}")
        
        return submission
    
    def load_all_data(self, validation: bool = True) -> Dict[str, pd.DataFrame]:
        """
        Load all M5 competition data.
        
        Args:
            validation (bool): If True, load validation sales data; if False, load evaluation data
            
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing all loaded datasets
        """
        logger.info("Loading all M5 competition data...")
        
        data = {
            'calendar': self.load_calendar(),
            'sales': self.load_sales_data(validation=validation),
            'prices': self.load_prices(),
            'sample_submission': self.load_sample_submission()
        }
        
        logger.info("All data loaded successfully!")
        return data
    
    def get_data_info(self) -> Dict[str, Dict]:
        """
        Get information about all data files.
        
        Returns:
            Dict: Information about each dataset
        """
        info = {}
        
        # Load all data
        data = self.load_all_data()
        
        for name, df in data.items():
            info[name] = {
                'shape': df.shape,
                'columns': list(df.columns),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
                'null_counts': df.isnull().sum().to_dict()
            }
        
        return info


def melt_sales_data(sales_df: pd.DataFrame, calendar_df: pd.DataFrame) -> pd.DataFrame:
    """
    Melt sales data from wide format to long format and merge with calendar.
    
    Args:
        sales_df (pd.DataFrame): Sales data in wide format
        calendar_df (pd.DataFrame): Calendar data
        
    Returns:
        pd.DataFrame: Melted sales data with date information
    """
    logger.info("Melting sales data from wide to long format...")
    
    # Get ID columns (non-day columns)
    id_cols = [col for col in sales_df.columns if not col.startswith('d_')]
    day_cols = [col for col in sales_df.columns if col.startswith('d_')]
    
    # Melt the data
    melted = pd.melt(
        sales_df,
        id_vars=id_cols,
        value_vars=day_cols,
        var_name='d',
        value_name='sales'
    )
    
    # Merge with calendar to get actual dates
    melted = melted.merge(calendar_df[['d', 'date']], on='d', how='left')
    
    # Sort by item and date
    melted = melted.sort_values(['item_id', 'date']).reset_index(drop=True)
    
    logger.info(f"Melted sales data: {melted.shape}")
    return melted


def create_hierarchical_structure(sales_df: pd.DataFrame) -> Dict[str, list]:
    """
    Extract hierarchical structure from sales data.
    
    Args:
        sales_df (pd.DataFrame): Sales data
        
    Returns:
        Dict: Hierarchical structure information
    """
    hierarchy = {
        'states': sales_df['state_id'].unique().tolist(),
        'stores': sales_df['store_id'].unique().tolist(),
        'categories': sales_df['cat_id'].unique().tolist(),
        'departments': sales_df['dept_id'].unique().tolist(),
        'items': sales_df['item_id'].unique().tolist()
    }
    
    # Create store-state mapping
    store_state_map = sales_df[['store_id', 'state_id']].drop_duplicates()
    hierarchy['store_state_mapping'] = store_state_map.set_index('store_id')['state_id'].to_dict()
    
    # Create item hierarchy mapping
    item_hierarchy = sales_df[['item_id', 'dept_id', 'cat_id']].drop_duplicates()
    hierarchy['item_hierarchy'] = item_hierarchy.set_index('item_id').to_dict('index')
    
    return hierarchy


# Convenience functions
def load_data(data_dir: str = "data", validation: bool = True) -> Dict[str, pd.DataFrame]:
    """
    Convenience function to load all M5 data.
    
    Args:
        data_dir (str): Path to data directory
        validation (bool): Whether to load validation or evaluation data
        
    Returns:
        Dict[str, pd.DataFrame]: All loaded datasets
    """
    loader = M5DataLoader(data_dir)
    return loader.load_all_data(validation=validation)


def load_and_prepare_data(data_dir: str = "data", validation: bool = True, 
                         melt_sales: bool = False) -> Tuple[Dict[str, pd.DataFrame], Dict]:
    """
    Load and optionally prepare M5 data for modeling.
    
    Args:
        data_dir (str): Path to data directory
        validation (bool): Whether to load validation or evaluation data
        melt_sales (bool): Whether to melt sales data to long format
        
    Returns:
        Tuple: (data_dict, hierarchy_info)
    """
    loader = M5DataLoader(data_dir)
    data = loader.load_all_data(validation=validation)
    
    # Create hierarchical structure
    hierarchy = create_hierarchical_structure(data['sales'])
    
    # Optionally melt sales data
    if melt_sales:
        data['sales_melted'] = melt_sales_data(data['sales'], data['calendar'])
    
    return data, hierarchy


if __name__ == "__main__":
    # Example usage
    loader = M5DataLoader()
    
    # Load all data
    data = loader.load_all_data()
    
    # Print basic info
    info = loader.get_data_info()
    for name, details in info.items():
        print(f"\n{name.upper()}:")
        print(f"  Shape: {details['shape']}")
        print(f"  Memory: {details['memory_usage_mb']:.2f} MB")
        print(f"  Columns: {len(details['columns'])}")
