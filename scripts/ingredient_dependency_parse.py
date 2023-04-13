
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from spacy import displacy
import spacy

def create_html_representation(text,number):
    return f"""
<!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS v5.2.1 -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">

</head>

<body>
  <div class="container">
    <div class="row justify-content-center align-items-center g-2">
        <div class="col-8">
            {text}
        </div>
    </div>
    <div class="row justify-content-center align-items-center g-2">
        <div class="col-12">
            <img src="ingredient{number}.svg"/>
        </div>
    </div>
    <div class="row justify-content-center align-items-center g-2">
        <div class="col-12 border-top">
            <a name="" id="" class="btn btn-primary" href="page{number-1}.html" role="button">Previous</a>
            <a name="" id="" class="btn btn-primary" href="page{number+1}.html" role="button">Next</a>
        </div>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"
    integrity="sha384-oBqDVmMz9ATKxIep9tiCxS/Z9fNfEXiDAYTujMAeBAsjFuCZSmKbSSUnQlmh/jp3" crossorigin="anonymous">
  </script>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.min.js"
    integrity="sha384-7VPbUDkoPSGFnVtYi0QogXtr74QeVeeIs99Qfg5YCF+TidwNdjvaKZX19NZ/e6oz" crossorigin="anonymous">
  </script>
</body>

</html>
    """

data = pd.read_csv('../samples/nyt-ingredients-snapshot-2015.csv')
nlp = spacy.load("en_core_web_lg")
ind = 1
cc_ind = 1
found = False
cc_ings = 0
for ingredient in tqdm(data.input):
    if type(ingredient) == str:
        ingre = nlp(ingredient)
        contains_cc = False
        contains_sub = False
        
        for token in ingre:
            if token.dep_ == 'ROOT':
                root_token = token
            if token.dep_ == 'cc' and token.text == 'or':
                contains_cc = True
            if token.dep_ == 'ROOT' and 'or' in list([child.text for child in token.children]):
                contains_sub = True
        if contains_cc and contains_sub:
            cc_ings += 1
            svg = displacy.render(ingre, style='dep', options={'compact':True},jupyter=False)
            output_path = Path(f"../docs/ingredientes_dependency_parse/ingredient{cc_ind}.svg")
            output_html = Path(f"../docs/ingredientes_dependency_parse/page{cc_ind}.html")
            output_path.open("w", encoding="utf-8").write(svg)
            output_html.open("w", encoding="utf-8").write(create_html_representation(ingredient, cc_ind))
            cc_ind += 1
    ind += 1

    if cc_ind == 20:
        break
