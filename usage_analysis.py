
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from model import Issue,Event
import config
class UsageAnalysis:

        def __init__(self):  
                """
                Constructor
                """
                # Parameter is passed in via command line (--user)
                self.USER:str = config.get_parameter('user')
    

        def run(self):
                """
                Analyze and plot the frequency of each label used in issues.
                """
                issues:List[Issue] = DataLoader().get_issues()

                # Flatten all labels across all issues
                all_labels = [label for i in issues for label in i.labels]
                
                # Create DataFrame to calculate counts
                df = pd.DataFrame(all_labels, columns=['label'])
                label_counts = df['label'].value_counts()
                
                # Plot
                label_counts.plot(kind='bar', figsize=(14, 8), title="Label Usage in Issues")
                plt.xlabel("Label")
                plt.ylabel("Frequency")
                plt.show()
        
if __name__ == '__main__':
    # Invoke run method when running this module directly
    UsageAnalysis().run()