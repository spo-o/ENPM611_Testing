from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd
from data_loader import DataLoader
from model import Issue
import config

class IssueTriageAnalyser:
    """
    Implements a new analysis of GitHub issues and outputs the result of that analysis.
    """
    
    def __init__(self):
        """
        Constructor
        """
        # Parameters passed in via command line
        self.USER: str = config.get_parameter('user')
        self.LABEL: str = config.get_parameter('label')
    
    def run(self):
        """
        Starting point for this analysis.
        """
        issues: List[Issue] = DataLoader().get_issues()
        
        # Overall Analysis
        self.overall_analysis(issues)
        
        # Subset Analysis by User
        if self.USER:
            self.analysis_by_user(issues, self.USER)
        
        # Subset Analysis by Label
        if self.LABEL:
            self.analysis_by_label(issues, self.LABEL)
    
    def overall_analysis(self, issues: List[Issue]):
        """
        Provides overall insights about issues, contributors, etc.
        """
        # Count issues by state (open/closed)
        state_counts = self.count_issues_by_state(issues)
        self.plot_state_counts(state_counts)
        
        # Count issues by label
        label_counts = self.count_issues_by_label(issues)
        self.plot_label_counts(label_counts)
        
        # Count issues by creator
        creator_counts = self.count_issues_by_creator(issues)
        self.plot_creator_counts(creator_counts)
    
    def analysis_by_user(self, issues: List[Issue], user: str):
        """
        Provides insights about issues created by a specific user.
        """
        user_issues = [issue for issue in issues if issue.creator == user]
        print(f"Total issues created by {user}: {len(user_issues)}")
        
        # Count issues by state for the user
        state_counts = self.count_issues_by_state(user_issues)
        self.plot_state_counts(state_counts, title=f"Issues by State for {user}")
    
    def analysis_by_label(self, issues: List[Issue], label: str):
        """
        Provides insights about issues with a specific label.
        """
        label_issues = [issue for issue in issues if label in issue.labels]
        print(f"Total issues with label '{label}': {len(label_issues)}")
        
        # Count issues by state for the label
        state_counts = self.count_issues_by_state(label_issues)
        self.plot_state_counts(state_counts, title=f"Issues by State with Label '{label}'")
    
    def count_issues_by_state(self, issues: List[Issue]) -> Dict[str, int]:
        state_counts = {'open': 0, 'closed': 0}
        for issue in issues:
            state_counts[issue.state] += 1
        return state_counts
    
    def plot_state_counts(self, state_counts: Dict[str, int], title: str = 'Issues by State'):
        plt.bar(state_counts.keys(), state_counts.values())
        plt.title(title)
        plt.xlabel('State')
        plt.ylabel('Count')
        plt.show()
    
    def count_issues_by_label(self, issues: List[Issue]) -> Dict[str, int]:
        label_counts = {}
        for issue in issues:
            for label in issue.labels:
                if label not in label_counts:
                    label_counts[label] = 0
                label_counts[label] += 1
        return label_counts
    
    def plot_label_counts(self, label_counts: Dict[str, int]):
        df = pd.DataFrame(list(label_counts.items()), columns=['Label', 'Count'])
        df = df.sort_values(by='Count', ascending=False)
        df.plot(kind='bar', x='Label', y='Count', figsize=(14, 8), title="Issues by Label")
        plt.xlabel("Label")
        plt.ylabel("Count")
        plt.show()
    
    def count_issues_by_creator(self, issues: List[Issue]) -> Dict[str, int]:
        creator_counts = {}
        for issue in issues:
            if issue.creator not in creator_counts:
                creator_counts[issue.creator] = 0
            creator_counts[issue.creator] += 1
        return creator_counts
    
    def plot_creator_counts(self, creator_counts: Dict[str, int]):
        df = pd.DataFrame(list(creator_counts.items()), columns=['Creator', 'Count'])
        df = df.sort_values(by='Count', ascending=False)
        df.plot(kind='bar', x='Creator', y='Count', figsize=(14, 8), title="Issues by Creator")
        plt.xlabel("Creator")
        plt.ylabel("Count")
        plt.show()

if __name__ == '__main__':
    IssueTriageAnalyser().run()