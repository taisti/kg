from backend.lexmapr_api.preprocessing import Preprocessing
from backend.lexmapr_api.processing import Processing
from backend.lexmapr_api.postprocessing import Postprocessing


def run(data_input: str):
    df_input, csv_text = Preprocessing(data_input).run()
    lexmapr_output = Processing(csv_text).run()
    resp = Postprocessing(df_input, lexmapr_output).run()
    return resp
