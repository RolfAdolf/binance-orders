from binance_orders.utils import js, preprocess


def test_load_request(make_test_json):
    test_dict = js.load_request(make_test_json)

    match test_dict:
        case {
            "volume": volume,
            "number": number,
            "amountDif": amountDif,
            "side": side,
            "priceMin": priceMin,
            "priceMax": priceMax,
        }:
            pass_the_test = True
        case _:
            pass_the_test = False
    assert pass_the_test, "Not enough keys in test_dict"


def test_get_amounts():
    volume = 10000
    amount_dif = 50

    for i in range(5, 10):
        amounts = preprocess.get_amounts(
            volume=volume, n_orders=i, amount_dif=amount_dif
        )
        assert (
            round(sum(amounts)) == volume
        ), "Sum of amounts is not equal to the volume"


def test_get_prices():
    priceMin = 9999
    priceMax = 10000
    for i in preprocess.get_prices(5, priceMin, priceMax):
        assert i <= 10000, "Value greater than priceMax"
        assert i >= 9999, "Value lower than priceMin"


def test_get_quantities():
    # Pass the regular lists in the function to test
    # exception handling
    amounts = [1, 2, 3]
    prices = [3, 2, 1]
    assert len(preprocess.get_quantities(amounts, prices)) == len(amounts)


def test_get_quants_prices(make_test_json):
    params = js.load_request(make_test_json)

    result = preprocess.get_quants_prices(**params)

    assert len(result) == 2
