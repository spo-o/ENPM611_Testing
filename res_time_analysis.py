import matplotlib.pyplot as plt
import pandas as pd
from data_loader import DataLoader
from model import Issue

class ResolutionTimeAnalysis:
    def __init__(self):
        """
        Initialize the analysis class and load issues using DataLoader.
        """
        data_loader = DataLoader()
        self.issues = data_loader.load_issues()

    def run(self):
        """
        Perform the resolution time analysis and plot the results.
        """
        # Filter out issues that are still open (no resolution time)
        closed_issues = [issue for issue in self.issues if issue.state == 'closed']
        
        # Calculate resolution times
        resolution_times = [
            (pd.to_datetime(issue.updated_date) - pd.to_datetime(issue.created_date)).days
            for issue in closed_issues
        ]
        
        # Plot histogram of resolution times
        plt.figure(figsize=(14, 8))
        plt.hist(resolution_times, bins=20, edgecolor='black')
        plt.title("Resolution Times for Issues (in Days)")
        plt.xlabel("Days to Resolve")
        plt.ylabel("Number of Issues")
        plt.show()
