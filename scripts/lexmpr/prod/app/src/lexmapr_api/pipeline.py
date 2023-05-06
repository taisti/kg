from src.lexmapr_api.preprocessing import Preprocessing
from src.lexmapr_api.processing import Processing
from src.lexmapr_api.postprocessing import Postprocessing
import json

def run(input: str):
    df_input, csv_text = Preprocessing(input).run()
    lexmapr_output = Processing(csv_text).run()
    resp = Postprocessing(df_input, lexmapr_output).run()
    return resp
