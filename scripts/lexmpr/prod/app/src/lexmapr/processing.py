import io
import logging
import subprocess
from tempfile import NamedTemporaryFile
from typing import List
import pandas as pd


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
            data (str): csv string representation

        Returns:
            pd.Series: csv string representation
        """

        def for_each_row(text: str) -> str:
            with NamedTemporaryFile(suffix=".csv") as file:
                file.write(bytes(text, "utf-8"))
                file.seek(0)
                cmd = ["scripts/lexmapr.sh", file.name]
                proc = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                o, e = proc.communicate()

                output = o.decode("utf-8")
                error = e.decode("utf-8")
                status_code = proc.returncode

                if error:
                    logging.error("error=" + error)

                if status_code:
                    logging.warning("status_code=" + str(status_code))  # type: ignore

                return output

        results = csv_text.apply(for_each_row)
        return results

    @staticmethod
    def parse_output(output: pd.Series) -> List[pd.DataFrame]:
        """
        Convert output string into a DataFrame with selected column names

        Args:
            input (pd.Series): csv string

        Returns:
            List[pd.DataFrame]: parsed csv for each output of lexmapr
        """

        def for_each_row(row: str):
            text_input = io.StringIO(row)
            df = pd.read_csv(
                text_input, sep="\t", names=Processing.Headers
            ).iloc[1:]
            df = df.loc[:, Processing.OutputSelectedColumns]

            return df

        dfs = [for_each_row(row) for row in output]
        return dfs
