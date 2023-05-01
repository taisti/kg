# Running the program directly

1. Add working directory to the PATH environmental variable.
2. If you do not have lexmapr installed, clone https://github.com/taisti/LexMapr.git and install the package. If your machine is set up to work with a different code page than the default POSIX one (i.e. you are on Windows), modify the ontohelper.py file and set up encoding in the do_output_tsv function.

`		with (open(output_file_basename + '.tsv', 'w', encoding='utf-8')) as output_handle:`
`			output_handle.write('\n'.join(output))`

Run the `pip install .` command once again inside the cloned repository. Go back to this directory.
3. Run the `src/main.py` file (make sure you are running it from the top of the repository, as for now it uses hardcoded relative path to lexmapr config file). 
4. Open the browser, go to 127.0.0.1:5000.
5. Choose a file to analyze (file format in the `scripts/test.csv`)
6. Press submit.

Optionally you can access the method via a REST api. Endpoint for the api: 127.0.0.1:5000/api/lexmapr 


# How to install

Create `.env` file with `APP_PATH` env with path to current working directory.

```.env
APP_PATH=/home/user/lexmapr_api
```

## Linux
```bash
# Install Docker CLI
apt-get install docker
apt-get install docker-compose
# Run service container
docker-compose up
```

## MacOs

```bash
# Install Docker CLI
brew install docker
brew install docker-compose
# Run service container
docker-compose up
```

## Windows

[WSL](https://dev.to/_nicolas_louis_/how-to-run-docker-on-windows-without-docker-desktop-hik)

Then in WSL terminal run `docker-compose up` to start docker container


# How to operate container
1. Start - `docker-compose up`
2. Pause - `docker-compose down`
3. Exit -  `docker-compose rm`

# How to send recipe
Send `POST` requests to http://127.0.0.1:5000 with **raw** body having **CSV** string data with 
column `title,ingredients,directions,link,source,NER,ingredients_entities`.

Example `POSTMAN` request can be find in [`lexmapr.postman_collection.json`](lexmapr.postman_collection.json). 

[How to import?](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#importing-data-into-postman)

Example
> POST http://127.0.0.1:5000/
>
> title,ingredients,directions,link,source,NER,ingredients_entities\
> "3 1/2 c. bite size shredded rice biscuits""","In a heavy 2-quart saucepan, mix brown sugar, nuts, evaporated milk and butter or margarine. Stir over medium heat until mixture bubbles all over top. Boil and stir 5 minutes more. Take off heat. Stir in vanilla and cereal; mix well. Using 2 teaspoons, drop and shape into 30 clusters on wax paper. Let stand until firm, about 30 minutes.",www.cookbooks.com/Recipe-Details.aspx?id=44874,Gathered,,"[""brown sugar"", ""milk"", ""vanilla"", ""nuts"", ""butter"", ""bite size shredded rice biscuits""]","[{""start"": 0, ""end"": 1, ""type"": ""QUANTITY"", ""entity"": ""1""},{""start"": 2, ""end"": 4, ""type"": ""UNIT"", ""entity"": ""c.""},{""start"": 5, ""end"": 18, ""type"": ""PHYSICAL_QUALITY"", ""entity"": ""firmly packed""},{""start"": 19, ""end"": 24, ""type"": ""COLOR"", ""entity"": ""brown""},{""start"": 25, ""end"": 30, ""type"": ""FOOD"", ""entity"": ""sugar""},{""start"": 31, ""end"": 34, ""type"": ""QUANTITY"", ""entity"": ""1/2""},{""start"": 35, ""end"": 37, ""type"": ""UNIT"", ""entity"": ""c.""},{""start"": 38, ""end"": 48, ""type"": ""PHYSICAL_QUALITY"", ""entity"": ""evaporated""},{""start"": 49, ""end"": 53, ""type"": ""FOOD"", ""entity"": ""milk""},{""start"": 54, ""end"": 57, ""type"": ""QUANTITY"", ""entity"": ""1/2""},{""start"": 58, ""end"": 61, ""type"": ""UNIT"", ""entity"": ""tsp""},{""start"": 63, ""end"": 70, ""type"": ""FOOD"", ""entity"": ""vanilla""},{""start"": 71, ""end"": 74, ""type"": ""QUANTITY"", ""entity"": ""1/2""},{""start"": 75, ""end"": 77, ""type"": ""UNIT"", ""entity"": ""c.""},{""start"": 78, ""end"": 84, ""type"": ""PROCESS"", ""entity"": ""broken""},{""start"": 85, ""end"": 89, ""type"": ""FOOD"", ""entity"": ""nuts""},{""start"": 91, ""end"": 97, ""type"": ""FOOD"", ""entity"": ""pecans""},{""start"": 99, ""end"": 100, ""type"": ""QUANTITY"", ""entity"": ""2""},{""start"": 101, ""end"": 105, ""type"": ""UNIT"", ""entity"": ""Tbsp""},{""start"": 107, ""end"": 113, ""type"": ""FOOD"", ""entity"": ""butter""},{""start"": 117, ""end"": 126, ""type"": ""FOOD"", ""entity"": ""margarine""},{""start"": 127, ""end"": 132, ""type"": ""QUANTITY"", ""entity"": ""3 1/2""},{""start"": 133, ""end"": 135, ""type"": ""UNIT"", ""entity"": ""c.""},{""start"": 136, ""end"": 140, ""type"": ""PROCESS"", ""entity"": ""bite""},{""start"": 146, ""end"": 154, ""type"": ""PROCESS"", ""entity"": ""shredded""},{""start"": 155, ""end"": 168, ""type"": ""FOOD"", ""entity"": ""rice biscuits""}]"
