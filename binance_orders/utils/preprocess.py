import numpy as np

from typing import List, Dict, Tuple


def get_amounts(
    volume: float,
    n_orders: int = 1,
    amount_dif: float = 0,
) -> np.ndarray:
    """
    Calculate amounts of the orders.

    :param float volume: Total volume of suborders
    :param int n_orders: Number of the suborders
    :param float amount_dif: Limits of deviations of suborder values
    :return:
        Amounts of the suborders
    """

    # Calculate deviations in the segment
    # [-amount_dif; +amount_dif) for each suborder
    diffs = np.random.uniform(-amount_dif, amount_dif, size=n_orders)

    # Calculate the residual volume
    s = sum(diffs)

    # Calculate average amount of each order
    # and add the deviations
    amount_avg = (volume - s) / n_orders
    amounts = amount_avg + diffs

    return amounts


def get_prices(
    n_orders: int,
    price_min: float,
    price_max: float,
) -> np.ndarray:
    """Calculate prices for the orders."""
    return np.random.uniform(price_min, price_max, size=n_orders)


def get_quantities(
    amounts: np.ndarray[float],
    prices: np.ndarray[float],
) -> np.ndarray[float]:
    """
    Calculate how much currency (crypto) a user wants to buy
    or sell based on the market price ($) and amounts ($).

    :param List[float] amounts: Volumes of each order
    :param prices: final prices of each order
    :return: List of quantities of the order.
    """
    try:
        return amounts / prices
    except TypeError:
        amounts = np.array(amounts)
        prices = np.array(prices)
        return amounts / prices


def get_quants_prices(
    volume: float,
    number: int,
    amountDif: float,
    priceMin: float,
    priceMax: float,
    **kwargs,
) -> Tuple[np.ndarray[float]]:
    amounts = get_amounts(volume, number, amountDif)

    prices = get_prices(
        number,
        priceMin,
        priceMax,
    )

    quants = get_quantities(amounts, prices)

    return quants, prices
