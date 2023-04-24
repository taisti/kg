from src.lexmapr.preprocessing import Preprocessing
from src.lexmapr.processing import Processing
from src.lexmapr.postprocessing import Postprocessing


def run(input: str):
    df_input, csv_text = Preprocessing(input).run()
    lexmapr_output = Processing(csv_text).run()
    response = Postprocessing(df_input, lexmapr_output).run()
    return response
