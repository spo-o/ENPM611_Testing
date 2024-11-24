import json
from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

class CommonIssuesAnalyser:
    """
    Analyzes common issues in the poetry_issues.json file and creates a graph representing these interesting data inputs.
    """
    
    def __init__(self, file_path: str, categories: Dict[str, List[str]]):
        """
        Constructor
        """
        self.file_path = file_path
        self.categories = categories
    
    def load_issues(self) -> List[Dict]:
        """
        Loads issues from the JSON file.
        """
        with open(self.file_path, 'r') as file:
            issues = json.load(file)
        return issues
    
    def categorize_issues(self, issues: List[Dict]) -> Dict[str, int]:
        """
        Categorizes issues into predefined categories.
        """
        category_counts = {category: 0 for category in self.categories}
        
        for issue in issues:
            title = issue.get('title', '').lower()
            for category, keywords in self.categories.items():
                if any(keyword in title for keyword in keywords):
                    category_counts[category] += 1
                    break
        
        return category_counts
    
    def calculate_resolution_times(self, issues: List[Dict]) -> Dict[str, List[int]]:
        """
        Calculates the resolution times for issues and aggregates them by category.
        """
        category_times = {category: [] for category in self.categories}
        
        for issue in issues:
            if issue['state'] == 'closed':
                created_date = datetime.strptime(issue['created_date'], '%Y-%m-%dT%H:%M:%S%z')
                closed_date = datetime.strptime(issue['updated_date'], '%Y-%m-%dT%H:%M:%S%z')
                resolution_time = (closed_date - created_date).days
                
                title = issue.get('title', '').lower()
                for category, keywords in self.categories.items():
                    if any(keyword in title for keyword in keywords):
                        category_times[category].append(resolution_time)
                        break
        
        return category_times
    
    def plot_category_counts(self, category_counts: Dict[str, int]):
        """
        Plots the category counts as a bar graph.
        """
        df = pd.DataFrame(list(category_counts.items()), columns=['Category', 'Count'])
        df = df.sort_values(by='Count', ascending=False)
        df.plot(kind='bar', x='Category', y='Count', figsize=(14, 8), title="Common Issues in Poetry")
        plt.xlabel("Category")
        plt.ylabel("Count")
        plt.show()
    
    def plot_resolution_times(self, category_times: Dict[str, List[int]]):
        """
        Plots the average resolution times for each category as a bar graph.
        """
        avg_times = {category: sum(times) / len(times) if times else 0 for category, times in category_times.items()}
        df = pd.DataFrame(list(avg_times.items()), columns=['Category', 'Average Resolution Time (days)'])
        df = df.sort_values(by='Average Resolution Time (days)', ascending=False)
        df.plot(kind='bar', x='Category', y='Average Resolution Time (days)', figsize=(14, 8), title="Average Resolution Time by Category")
        plt.xlabel("Category")
        plt.ylabel("Average Resolution Time (days)")
        plt.show()
    
    def run(self):
        """
        Runs the analysis and generates the graphs.
        """
        issues = self.load_issues()
        category_counts = self.categorize_issues(issues)
        self.plot_category_counts(category_counts)
        
        category_times = self.calculate_resolution_times(issues)
        self.plot_resolution_times(category_times)
