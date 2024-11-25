import unittest
from unittest.mock import patch, MagicMock
from frequency_of_issue_creation import frequencyOfIssueCreation
import matplotlib.pyplot as plt
from datetime import datetime

class TestFrequencyOfIssueCreation(unittest.TestCase):
    @patch("matplotlib.pyplot.show")  
    def test_run(self, mock_show):
        
        analyzer = frequencyOfIssueCreation()
       
        mock_issue_1 = MagicMock()
        mock_issue_1.created_date = datetime(2024, 9, 25, 14, 42, 50)

        mock_issue_2 = MagicMock()
        mock_issue_2.created_date = datetime(2024, 9, 25, 2, 34, 36)

        mock_issue_3 = MagicMock()
        mock_issue_3.created_date = datetime(2024, 9, 24, 22, 48, 9)
      
        analyzer.issues = [mock_issue_1, mock_issue_2, mock_issue_3]

        analyzer.run()

        mock_show.assert_called_once()

        plt.close('all')

if __name__ == "__main__":
    unittest.main()
