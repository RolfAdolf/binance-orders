from binance.spot import Spot

from typing import List, Dict, Tuple
from enum import Enum


class SideType(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP_LOSS = "STOP_LOSS"
    STOP_LOSS_LIMIT = "STOP_LOSS_LIMIT"
    TAKE_PROFIT = "TAKE_PROFIT"
    TAKE_PROFIT_LIMIT = "TAKE_PROFIT_LIMIT"
    LIMIT_MAKER = "LIMIT_MAKER"


class TimeInForceType(Enum):
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"


def get_client(
    api_key: str,
    api_secret: str,
    base_url: str = "https://api.binance.com",
    *args,
    **kwargs,
) -> Spot:
    """
    Get the API Spot Connector.
    :param str api_key: Get it on the https://www.binancezh.top/en/my/settings/api-management
    :param str api_secret: Get it on the https://www.binancezh.top/en/my/settings/api-management
    :param str base_url: Url of the API of Binance
    :return: Return the Binance API spot connector
    """
    return Spot(
        api_key=api_key,
        api_secret=api_secret,
        base_url=base_url,
        *args,
        **kwargs,
    )


def place_order(
    client: Spot,
    symbol: str,
    side: str,
    quantity: float,
    price: float,
    order_type: OrderType = OrderType.LIMIT,
    time_in_force: TimeInForceType = TimeInForceType.GTC,
    *args,
    **kwargs,
) -> None:
    """
    Place an order for a certain currency in the amount of quantity
    with a price equal to the price variable.

    :param str client: Binance spot connector.
    :param str symbol: Currency pair
    :param str side: 'SELL' or 'BUY' parameter
    :param float quantity: Order volume ($)
    :param float price: Currency price ($)
    :param str order_type: Type of the order
    :param str time_in_force: This sets how long an order will be active before expiration.

    :raises ValueError: if the side is not 'BUY' or 'SELL'
    :raises ValueError: if the order_type is not valid for type of the order.
    :raises ValueError: if the time_in_force is not valid for timeInForce of the order.
    """
    side = SideType(side).value
    order_type = OrderType(order_type).value
    time_in_force = TimeInForceType(time_in_force).value

    client.new_order(
        symbol=symbol,
        side=side,
        type=order_type,
        quantity=quantity,
        price=price,
        timeInForce=time_in_force,
        *args,
        **kwargs,
    )


def get_last_orders(
    client: Spot,
    symbol: str,
    limit: int,
) -> List[Dict]:
    """
    Get last $limit$ orders of your account.
    :param Spot client: Binance Spot API client
    :param str symbol: Pair of currencies
    :param limit: Number of output orders
    :return: List of the orders
    """
    return client.get_orders(symbol=symbol, limit=limit)


def get_precisions(client: Spot, symbol: str) -> Tuple[int]:
    response = client.exchange_info(symbol=symbol)
    base_precision = response["symbols"][0]["baseAssetPrecision"]
    quote_precision = response["symbols"][0]["quotePrecision"]
    return base_precision, quote_precision
