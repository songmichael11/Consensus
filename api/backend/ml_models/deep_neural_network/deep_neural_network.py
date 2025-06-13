import pandas as pd
import numpy as np
import json
import os
from tensorflow.keras.models import load_model

# Cache for model and preprocessing parameters to avoid reloading
_model_cache = None
_params_cache = None

def load_preprocessor(params_file):
    """Load preprocessing parameters from saved file."""
    with open(params_file, 'r') as f:
        params = json.load(f)
    return params

def validate_input_data(data, params):
    """Validate that input data has all required columns."""
    required_columns = params['numerical_features'] + params['categorical_features']
    missing_columns = [col for col in required_columns if col not in data.columns]
    
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Check for any NaN values
    if data.isnull().any().any():
        raise ValueError("Input data contains NaN values. Please clean your data first.")
    
    return True

def preprocess_data(data, params):
    """Manually apply preprocessing transformations."""
    # Validate input first
    validate_input_data(data, params)
    
    # Separate numerical and categorical data
    numerical_data = data[params['numerical_features']]
    categorical_data = data[params['categorical_features']]
    
    # Apply StandardScaler transformation manually
    scaler_mean = np.array(params['scaler_mean'])
    scaler_scale = np.array(params['scaler_scale'])
    numerical_scaled = (numerical_data.values - scaler_mean) / scaler_scale
    
    # Apply OneHotEncoder transformation manually
    categorical_encoded = []
    for i, feature in enumerate(params['categorical_features']):
        feature_categories = params['encoder_categories'][i]
        feature_values = categorical_data[feature].values
        
        # Create one-hot encoding for this feature
        encoded_feature = np.zeros((len(feature_values), len(feature_categories)))
        for j, value in enumerate(feature_values):
            if value in feature_categories:
                category_idx = feature_categories.index(value)
                encoded_feature[j, category_idx] = 1
            # If unknown category, all zeros (handle_unknown='ignore' behavior)
        
        categorical_encoded.append(encoded_feature)
    
    # Combine numerical and categorical features
    if categorical_encoded:
        categorical_combined = np.hstack(categorical_encoded)
        processed_data = np.hstack([numerical_scaled, categorical_combined])
    else:
        processed_data = numerical_scaled
    
    return processed_data

def get_model_and_params():
    """Load and cache the model and preprocessing parameters."""
    global _model_cache, _params_cache
    
    if _model_cache is None or _params_cache is None:
        # Get the directory where this file is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'Unemployment_AI_Optimized.keras')
        params_path = os.path.join(current_dir, 'preprocessing_params_optimized.json')
        
        # Load model and preprocessing parameters
        _model_cache = load_model(model_path)
        _params_cache = load_preprocessor(params_path)
    
    return _model_cache, _params_cache

def map_frontend_to_model_features(frontend_data):
    """Map frontend feature names to model expected names."""
    # Frontend uses different naming convention than the training data
    feature_mapping = {
        'Population': 'Population, total',
        'GDP_per_capita': 'GDP per capita (current US$)',
        'Trade_union_density': 'Trade union density', 
        'Unemployment_rate': 'Gini index',  # Frontend passes GINI as unemployment_rate for this context
        'Health': 'Health spending',
        'Education': 'Education spending',
        'Housing': 'Housing spending', 
        'Community_development': 'Community development spending',
        'Corporate_tax_rate': 'Combined corporate income tax rate',
        'Inflation': 'Inflation, consumer prices (annual %)',
        'IRLT': 'IRLT'
    }
    
    # Map region data
    if frontend_data.get('Region_East_Asia_and_Pacific', 0) == 1:
        region = 'East Asia and Pacific'
    elif frontend_data.get('Region_Europe_and_Central_Asia', 0) == 1:
        region = 'Europe and Central Asia'
    elif frontend_data.get('Region_Latin_America_and_Caribbean', 0) == 1:
        region = 'Latin America and Caribbean'
    elif frontend_data.get('Region_Middle_East_and_North_Africa', 0) == 1:
        region = 'Middle East and North Africa'
    else:
        region = 'Europe and Central Asia'  # Default
    
    # Create mapped data
    mapped_data = {}
    for frontend_key, model_key in feature_mapping.items():
        if frontend_key in frontend_data:
            mapped_data[model_key] = frontend_data[frontend_key]
    
    mapped_data['Region'] = region
    
    return mapped_data

def predict_unemployment_rate(new_data):
    """
    Make unemployment rate prediction on new data.
    
    Args:
        new_data: Dictionary with frontend feature names
    
    Returns:
        Predicted unemployment rate
    """
    try:
        # Get cached model and parameters
        model, params = get_model_and_params()
        
        # Map frontend data to model expected format
        mapped_data = map_frontend_to_model_features(new_data)
        
        # Convert to DataFrame for preprocessing
        df = pd.DataFrame([mapped_data])
        
        # Preprocess the new data
        processed_data = preprocess_data(df, params)
        
        # Make prediction
        prediction = model.predict(processed_data, verbose=0)
        
        # Convert to standard Python float for JSON serialization
        return float(prediction.flatten()[0])
        
    except Exception as e:
        raise Exception(f"Error making DNN prediction: {str(e)}")