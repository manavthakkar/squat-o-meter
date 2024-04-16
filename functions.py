import pandas as pd
from datetime import datetime

def save_squat_count(squat_count):
    # Get current date
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year
    
    # Create a DataFrame
    data = {'Day': [day],
            'Month': [month],
            'Year': [year],
            'Count': [squat_count]}
    
    new_df = pd.DataFrame(data)
    
    try:
        # Try loading existing CSV file
        existing_df = pd.read_csv('squat_count.csv')
        
        # Append new data to existing DataFrame
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    except FileNotFoundError:
        # If the file doesn't exist, use the new DataFrame
        updated_df = new_df
    
    # Save updated DataFrame to CSV
    updated_df.to_csv('squat_count.csv', index=False)