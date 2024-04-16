import pandas as pd
from datetime import datetime
from tkinter import messagebox

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


def get_squat_sum_month(month, year):
    """
    This function reads the squat count data from a CSV file and returns the sum of squat counts for a given month and year.

    """
    # Read CSV file
    try:
        df = pd.read_csv('squat_count.csv')
    except FileNotFoundError:
        print("Error: squat_count.csv file not found.")
        return None

    # Filter DataFrame based on month and year
    filtered_df = df[(df['Month'] == month) & (df['Year'] == year)]

    # Calculate sum of squat counts
    squat_count_sum = filtered_df['Count'].sum()

    return squat_count_sum

def confirm_save(squats_count):
    answer = messagebox.askokcancel("Confirmation", "Are you sure you want to save?")
    if answer:
        # If the user clicks OK, save to database
        print("Saved to database")
        save_squat_count(squats_count)
        messagebox.showinfo("Save Successful", "Data saved successfully")
    else:
        # If the user clicks Cancel, don't save
        print("User clicked Cancel, data not saved")