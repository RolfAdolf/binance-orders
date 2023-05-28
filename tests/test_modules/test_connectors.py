from pydantic.error_wrappers import ValidationError

import copy

from binance_orders.api import connectors


def test_place_order(create_settings, create_client, create_params):
    client = create_client
    settings = create_settings
    if_raised = False
    params = create_params

    args = {
        "client": client,
        "symbol": settings.symbol,
        "side": params["side"],
        "quantity": params["quantity"],
        "price": params["price"],
        "order_type": "LIMIT",
        "time_in_force": "GTC",
    }

    args_1 = copy.copy(args)
    args_2 = copy.copy(args)
    args_3 = copy.copy(args)

    args_1["side"] = "#ERROR"
    args_2["order_type"] = "#ERROR"
    args_3["time_in_force"] = "#ERROR"

    for args in (args_1, args_2, args_3):
        try:
            connectors.place_order(**args)
            if_raised = False
            break
        except ValueError:
            if_raised = True

    assert if_raised, "ValueError has not been raised."


def test_get_last_orders(create_settings, create_client, create_params, create_id):
    """Check if id of the last order matches with
    the set id of the order id which has been just placed"""
    settings = create_settings
    client = create_client
    params = create_params
    uniq_id = create_id

    args = {
        "client": client,
        "symbol": settings.symbol,
        "side": params["side"],
        "quantity": round(params["quantity"], 6),
        "price": round(params["price"], 2),
        "order_type": "LIMIT",
        "time_in_force": "GTC",
        "newClientOrderId": uniq_id,
    }

    connectors.place_order(**args)

    response = connectors.get_last_orders(client, settings.symbol, limit=1)

    assert response[0]["clientOrderId"] == uniq_id, (
        f"{uniq_id} " f"is not equal to {response['clientOrderId']}"
    )


def test_get_precisions(create_settings, create_client):
    btc_precision = 8
    usdt_precision = 8

    base_precision, quote_precision = connectors.get_precisions(
        create_client,
        create_settings.symbol,
    )

    assert base_precision == btc_precision, "Wrong precision of BTC"
    assert quote_precision == usdt_precision, "Wrong precision of USDT"
