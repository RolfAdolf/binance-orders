import numpy as np
from binance.spot import Spot
from binance.error import ClientError

import re
from typing import Dict, List, Tuple

from binance_orders.core.settings import settings
from binance_orders.utils import js, preprocess
from binance_orders.api import connectors


def make_quants_prs(
    params: Dict,
) -> Tuple[np.ndarray[float]]:
    try:
        return preprocess.get_quants_prices(**params)
    except TypeError as e:
        miss_vars = re.findall(r"'\w*'", str(e))
        raise KeyError(
            f"There are no such keys in your json-file: " f"{', '.join(miss_vars)}"
        )


def make_args(
    client: Spot,
    params: Dict,
    quantities: np.ndarray[float],
    prices: np.ndarray[float],
) -> List[Dict]:
    """
    Make arguments for the order placing requests
    :param Spot client: Client for Binance Spot API
    :param Dict params: Frontend parameters for API request
    :param np.ndarray[float] quantities: The quantities of suborders
    :param np.ndarray[float] prices: The prices of suborders
    :return: List of argument to iterate over it
    """

    args = []
    for quantity, price in zip(quantities, prices):
        args.append(
            {
                "client": client,
                "symbol": settings.symbol,
                "side": params["side"],
                "quantity": quantity,
                "price": price,
                "order_type": "LIMIT",
                "time_in_force": "GTC",
            }
        )

    return args


def make_orders(arg_list: List[Dict]):
    for kwargs in arg_list:
        try:
            connectors.place_order(**kwargs)

        except ClientError as client_err:
            print("\n", client_err.error_code, client_err.error_message)
            print(f"quantity: {kwargs['quantity']}")
            print(f"price: {kwargs['price']}")

            err_code = client_err.error_code
            err_mess = client_err.error_message

            # Precision is over the maximum defined for this asset.
            if err_code == -1111:
                base_precision, quote_precision = connectors.get_precisions(
                    kwargs["client"], settings.symbol
                )
                kwargs["quantity"] = round(kwargs["quantity"], base_precision)
                kwargs["price"] = round(kwargs["price"], quote_precision)
                arg_list.append(kwargs)

            elif err_code == -1013 and "PRICE_FILTER" in err_mess:
                kwargs["price"] = round(kwargs["price"], 2)
                arg_list.append(kwargs)

            elif err_code == -1013 and "LOT_SIZE" in err_mess:
                kwargs["quantity"] = round(kwargs["quantity"], 6)
                arg_list.append(kwargs)

            # TODO: Add other filter handlings


def main():
    # Read parameters from file
    params = js.load_request(settings.params_file)

    # Preprocess parameters
    quantities, prices = make_quants_prs(params)

    # Get client
    client = connectors.get_client(
        api_key=settings.api_key,
        api_secret=settings.api_secret,
        base_url=settings.base_url,
    )

    # Get list of arguments
    arg_list = make_args(client, params, quantities, prices)

    make_orders(arg_list)

    print(
        "\n",
        connectors.get_last_orders(
            client=client, symbol=settings.symbol, limit=params["number"],
        ),
    )


if __name__ == "__main__":
    main()
