import pytest
from binance.spot import Spot
from pydantic.error_wrappers import ValidationError

import os
from pathlib import Path
import tempfile
import json
from time import time

from binance_orders.core import settings
from binance_orders.utils import js


test_env_filepath = Path("./tests/.env_test")


@pytest.fixture()
def create_dir():
    with tempfile.TemporaryDirectory() as test_folder:
        yield test_folder


@pytest.fixture()
def make_test_json(create_dir):
    directory = Path(create_dir)
    test_json_path = directory / "test.json"

    test_dict = {
        "volume": 10000.0,
        "number": 5,
        "amountDif": 50.0,
        "side": "BUY",
        "priceMin": 26000.0,
        "priceMax": 27000.0,
    }

    with open(test_json_path, "w") as js_file:
        json.dump(test_dict, js_file)

    return test_json_path


@pytest.fixture()
def create_settings():
    settings_ = settings.Settings(
        _env_file=test_env_filepath, _env_file_encoding="utf-8"
    )
    return settings_


@pytest.fixture()
def create_client(create_settings):
    settings_ = create_settings

    client = Spot(
        settings_.api_key,
        settings_.api_secret,
        base_url=settings_.base_url,
    )

    return client


@pytest.fixture()
def create_params(create_settings):
    settings_ = create_settings
    params = js.load_request(settings_.params_file)
    return params


@pytest.fixture()
def create_id(create_params):
    params = create_params
    uniq_id = f"{params['side']}_{round(time())}"
    return uniq_id
