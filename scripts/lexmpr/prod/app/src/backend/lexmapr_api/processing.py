from typing import List
import pandas as pd
from backend.lexmapr_tool import LexMaprTool


class Processing:
    Tool = LexMaprTool('/home/adam/Desktop/Projects/PUT/TAISTI/kg/scripts/lexmpr/prod/app/conf/lex_mapr.json')

    def __init__(self, entities_text: pd.Series):
        self.entities_text = entities_text

    def run(self):
        out = self.run_lexmapr(self.entities_text)
        return out

    @staticmethod
    def run_lexmapr(entities_text: pd.Series) -> List[pd.DataFrame]:
        """
        Run LexMapr with user parsed input data

        Args:
            entities_text (str): list of entities in string format per recipe

        Returns:
            List[pd.DataFrame]: LexMapr out per recipe
        """

        def for_each_row(row: List[str]) -> pd.DataFrame:
            lexmapr_out = pd.DataFrame([Processing.Tool.run(txt) for txt in row])
            return lexmapr_out

        results = entities_text\
            .apply(for_each_row)\
            .tolist()
        return results
