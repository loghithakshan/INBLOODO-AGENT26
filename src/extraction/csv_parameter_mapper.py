import pandas as pd
import io
import logging

logger = logging.getLogger(__name__)

def extract_parameters_from_csv(content: bytes) -> dict:
    """
    Extract medical parameters from CSV file.
    Handles multiple formats: one parameter per row or one per column.
    """
    try:
        df = pd.read_csv(io.BytesIO(content))
        params = {}
        
        logger.debug(f"CSV shape: {df.shape}, columns: {list(df.columns)}")
        
        # Strategy 1: Try to parse as parameter=value pairs (2 columns)
        if df.shape[1] == 2:
            col1, col2 = df.columns
            for idx in range(len(df)):
                key = str(df[col1].iloc[idx]).lower().strip()
                try:
                    value = float(df[col2].iloc[idx])
                    params[key] = value
                except (ValueError, TypeError):
                    logger.debug(f"Skipping row: {key} = {df[col2].iloc[idx]}")
                    pass
        
        # Strategy 2: Try to parse as header=parameter, values=data
        elif df.shape[0] > 0:
            for col in df.columns:
                col_lower = col.lower().strip()
                try:
                    # Get first numeric value in column
                    if pd.api.types.is_numeric_dtype(df[col]):
                        value = float(df[col].iloc[0])
                        params[col_lower] = value
                    else:
                        # Try to convert to float
                        value = float(df[col].iloc[0])
                        params[col_lower] = value
                except (ValueError, TypeError):
                    logger.debug(f"Skipping column {col}: cannot parse as numeric")
                    pass
        
        logger.info(f"CSV extraction: Found {len(params)} parameters from {len(df.columns)} columns")
        return params
        
    except Exception as e:
        logger.error(f"CSV parsing error: {str(e)}")
        return {}

