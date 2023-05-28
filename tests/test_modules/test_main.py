from copy import copy

from binance_orders.main import make_quants_prs, make_orders


def test_make_quants_prs():
    # Check the TypeError handling
    # Call function without arguments
    if_raised = False
    args = {}

    try:
        make_quants_prs(args)
    except KeyError:
        if_raised = True
    assert if_raised, "The KeyError was not raised"


def test_make_orders(create_client, create_settings, create_params, create_id):
    # Let's place two orders
    client = create_client
    settings = create_settings
    params = create_params
    first_uniq_id = create_id + "_1"
    second_uniq_id = create_id + "_2"

    args = {
        "client": client,
        "symbol": settings.symbol,
        "side": params["side"],
        "quantity": params["quantity"],
        "price": params["price"],
        "order_type": "LIMIT",
        "time_in_force": "GTC",
    }

    args_1 = copy(args)
    args_2 = copy(args)

    args_1["newClientOrderId"] = first_uniq_id
    args_2["newClientOrderId"] = second_uniq_id

    # This code will place two orders
    make_orders([args_1, args_2])

    # Let's get two last orders
    response = client.get_orders(symbol=settings.symbol, limit=2)

    second_id = response[0]["clientOrderId"]
    first_id = response[1]["clientOrderId"]

    assert first_uniq_id in (first_id, second_id)
    assert second_uniq_id in (first_id, second_id)
