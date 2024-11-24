from typing import List
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from data_loader import DataLoader
from model import Issue

class frequencyOfIssueCreation:
    def __init__(self):
        self.issues: List[Issue] = DataLoader().get_issues()

    def run(self):
        """
        Analyze and plot the frequency of issue creation over time.
        """
        # Extract issue creation dates
        creation_dates = [issue.created_date for issue in self.issues]
        
        # Convert to pandas DataFrame for time-based grouping
        df = pd.DataFrame(creation_dates, columns=['created_date'])
        df['created_date'] = pd.to_datetime(df['created_date'])
        
        # Group by month or week to analyze frequency over time
        frequency_df = df.groupby(df['created_date'].dt.to_period('M')).size()
        
        # Plot
        frequency_df.plot(kind='line', figsize=(14, 8), title="Frequency of Issue Creation Over Time")
        plt.xlabel("Date")
        plt.ylabel("Number of Issues Created")
        plt.show()

    
