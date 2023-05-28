# Binance orders

## Setup

To install all dependencies you can use `poetry`. If you need `pip`-installation you can check
all dependencies in the `pyproject.toml`-file.

```commandline
git clone https://github.com/RolfAdolf/binance-orders.git

cd binance-orders


poetry init

poetry install

poetry shell

cat pyproject.toml
```

Before using the script, you need to create an environment file `.env` with the following fields, 
as shown below. Place this file in the root directory of the project
`binance-orders/.env`:
```commandline
# API KEYS
API_KEY=                                    
                            
API_SECRET=

# Frontend Input
PARAMS_FILE='order_params.json'             # json-file with input

# Url of the Binance API-service
BASE_URL=https://testnet.binance.vision     # or use https://api.binance.com

# Which currency will be ordered
SYMBOL='BTCUSDT'                            # or other pair you want 
```

You can get keys in the 
[API-management site](# Get this keys in https://www.binance.com/en/my/settings/api-management)
or [For testnet](https://testnet.binance.vision/key/generate).

You need also create file with json-input. Name of this file should match the `PARAM_FILE` 
parameter in `.env`-file of the project:
```commandline
{"volume": 10000.0, "number": 5, "amountDif": 50.0, "side": "BUY", "priceMin": 26000.0, "priceMax": 27000.0}
```

Both files should be located in the root project directory (`binance-orders/`).

If you need to run the tests, you need to specify these files similarly 
and place them to the `./tests` directory 
(`./tests/.env_test` and `./tests/test_params.json`).
It is recommended to use a test platform (`testnet.binance.vision`) for tests.


## Run script

Run script as python module.

```commandline
python3 -m binance_orders.main
```

## Run tests

You car run test and check the coverage of code with `pytest`.

### Tests
```commandline
pytest --cov binance_orders
```

### Check the coverage
```commandline
coverage report
```

## Use Docker

### Run script in the docker-container

```commandline
docker build . -t test_script:latest

docker run -it --rm --name try_script test_script
```

If you need to run the tests in the container, uncomment the last raw
in the `./docker/run_main_with_tests.sh` file.

***
### Contacts
For all questions, please contact:

`Telegram`: @Nadir_Devrishev


`Mail`: n.devrishev@gmail.com