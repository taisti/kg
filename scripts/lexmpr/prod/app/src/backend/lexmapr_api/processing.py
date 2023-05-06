from typing import List
import pandas as pd

import io

from backend.lexmapr_tool import LexMaprTool


class Processing:
    Headers = [
        "Sample_Id",
        "Sample_Desc",
        "Processed_Sample",
        "Processed_Sample (With Scientific Name)",
        "Matched_Components",
        "Match_Status(Macro Level)",
    ]

    OutputSelectedColumns = [
        "Sample_Id",
        "Matched_Components",
        "Match_Status(Macro Level)",
    ]

    Tool = LexMaprTool('/home/adam/Desktop/Projects/PUT/TAISTI/kg/scripts/lexmpr/prod/app/conf/lex_mapr.json')

    def __init__(self, csv_text: pd.Series):
        self.csv_text = csv_text

    def run(self):
        out = self.run_lexmapr(self.csv_text)
        parsed = self.parse_output(out)
        return parsed

    @staticmethod
    def run_lexmapr(csv_text: pd.Series) -> pd.Series:
        """
        Run LexMapr with user parsed input data

        Args:
            csv_text (str): csv string representation

        Returns:
            pd.Series: csv string representation
        """
        results = csv_text.apply(Processing.Tool.run)
        return results

    @staticmethod
    def parse_output(output: pd.Series) -> List[pd.DataFrame]:
        """
        Convert output string into a DataFrame with selected column names

        Args:
            output (pd.Series): csv string

        Returns:
            List[pd.DataFrame]: parsed csv for each output of lexmapr
        """

        def for_each_row(row: str):
            text_input = io.StringIO(row)
            df = pd\
                .read_csv(text_input, sep="\t", names=Processing.Headers)\
                .iloc[1:]
            df = df.loc[:, Processing.OutputSelectedColumns]

            return df

        dfs = [for_each_row(row) for row in output]
        return dfs
