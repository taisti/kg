import io
import json
import pprint
from typing import List
import pandas as pd


class Preprocessing:
    Columns = [
        "title",
        "ingredients",
        "directions",
        "link",
        "source",
        "NER",
        "ingredients_entities",
    ]

    def __init__(self, input: str):
        self.input = input

    def run(self):
        df = self.parse_input(self.input)
        entities = self.merge_important_entities(df["ingredients_entities"])
        csv_text = self.convert_entities_to_lexmapr_input(entities)
        return df, csv_text

    @staticmethod
    def parse_input(input: str) -> pd.DataFrame:
        """
        Convert input csv string with columns

        `title,ingredients,directions,link,source,NER,ingredients_entities`

        into a DataFrame

        Args:
            input (str): csv string

        Returns:
            pd.DataFrame: parsed csv
        """
        text = io.StringIO(input)
        df = pd.read_csv(text, sep=",")
        return df

    @staticmethod
    def merge_important_entities(entities: pd.Series) -> pd.Series:
        """
        Connect entities into string if not QUANTITY or UNIT entity type

        Args:
            entities (pd.Series): text with QUANTITY and UNITS entities

        Returns:
            pd.Series: text without QUANTITY and UNIT entities
        """

        def for_each_row(row: str):
            entities = json.loads(row)
            text = [
                ent["entity"]
                for ent in entities
                if ent["type"] not in ["QUANTITY", "UNIT"]
            ]
            return text

        merged_entities = entities.apply(for_each_row)
        return merged_entities

    @staticmethod
    def convert_entities_to_lexmapr_input(entities: pd.Series) -> pd.Series:
        """
        Converts entities to csv input format

        Args:
            entities (pd.Series): entities without QUANTITY and UNIT

        Returns:
            pd.Series: csv string
        """

        def for_each_row(entities: List[str]):
            ids = list(range(len(entities)))
            df = pd.DataFrame({"Id": ids, "Text": entities})
            s = io.StringIO()
            df.to_csv(s, index=False)
            data_for_lexmapr = s.getvalue()
            return data_for_lexmapr

        csv_text = entities.apply(for_each_row)
        return csv_text
