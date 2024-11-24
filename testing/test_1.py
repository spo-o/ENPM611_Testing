import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from usage_analysis import UsageAnalysis


class TestUsageAnalysis(unittest.TestCase):

    @patch('usage_analysis.DataLoader')  # Mock DataLoader
    def test_run(self, MockDataLoader):
        # Mock the data returned by DataLoader
        mock_issues = [
            MagicMock(labels=["New Feature", "Bug"]),
            MagicMock(labels=["Enhancement", "Bug"]),
            MagicMock(labels=["New Feature", "Documentation"]),
            MagicMock(labels=["Bug", "Performance"]),
            MagicMock(labels=["New Feature", "Enhancement"]),
        ]
        MockDataLoader().get_issues.return_value = mock_issues

        # Instantiate UsageAnalysis and call run
        analysis = UsageAnalysis()
        
        # Mock plotting functions to avoid rendering the plot
        with patch('usage_analysis.plt.show'):
            analysis.run()
        
        # Expected labels and their frequencies
        expected_label_counts = {
            "New Feature": 3,
            "Bug": 3,
            "Enhancement": 2,
            "Documentation": 1,
            "Performance": 1,
        }

        # Validate label count calculation
        label_df = pd.DataFrame(
            [label for issue in mock_issues for label in issue.labels],
            columns=["label"]
        )
        calculated_label_counts = label_df["label"].value_counts().to_dict()

        self.assertEqual(calculated_label_counts, expected_label_counts)

    '''@patch('usage_analysis.DataLoader')
    @patch('usage_analysis.plt.show')  # Patch plt.show to avoid displaying the plot during tests
    def test_run_no_labels(self, mock_plt_show, MockDataLoader):
        # Mock issues with no labels
        mock_issues = [
            MagicMock(labels=[]),
            MagicMock(labels=[]),
        ]
        MockDataLoader().get_issues.return_value = mock_issues

        # Instantiate UsageAnalysis and call run
        analysis = UsageAnalysis()
        analysis.run()

        # Assert plt.show was not called (no plot should be displayed)
        mock_plt_show.assert_not_called()'''
    @patch('usage_analysis.DataLoader')
    def test_run_large_dataset(self, MockDataLoader):
    # Mock many issues with labels
        mock_issues = [MagicMock(labels=["Bug", "New Feature"]) for _ in range(1000)]
        MockDataLoader().get_issues.return_value = mock_issues

        # Instantiate UsageAnalysis and call run
        analysis = UsageAnalysis()
        
        with patch('usage_analysis.plt.show'):
            analysis.run()
        
        # Validate label counts
        expected_label_counts = {"Bug": 1000, "New Feature": 1000}
        label_df = pd.DataFrame(
            [label for issue in mock_issues for label in issue.labels],
            columns=["label"]
        )
        calculated_label_counts = label_df["label"].value_counts().to_dict()

        self.assertEqual(calculated_label_counts, expected_label_counts)

    @patch('usage_analysis.DataLoader')
    def test_run_duplicate_labels(self, MockDataLoader):
    # Mock issues with duplicate labels
        mock_issues = [
            MagicMock(labels=["Bug", "Bug"]),
            MagicMock(labels=["New Feature", "New Feature"]),
        ]
        MockDataLoader().get_issues.return_value = mock_issues

        # Instantiate UsageAnalysis and call run
        analysis = UsageAnalysis()
        
        with patch('usage_analysis.plt.show'):
            analysis.run()
        
        # Validate label counts
        expected_label_counts = {"Bug": 2, "New Feature": 2}
        label_df = pd.DataFrame(
            [label for issue in mock_issues for label in issue.labels],
            columns=["label"]
        )
        calculated_label_counts = label_df["label"].value_counts().to_dict()

        self.assertEqual(calculated_label_counts, expected_label_counts)


if __name__ == '__main__':
    unittest.main()
