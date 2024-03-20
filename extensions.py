import requests
import json
from config import keys



class APIException(Exception):
    pass
class ValutaException:
    @staticmethod
    def convert(quote: str, base: str, amout: str):
        if quote == base:
            raise APIException(f"невозможно перевести одинаковые валюты {base}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f" не удалось обработать валюту {quote}")

        try:
            base_tiker = keys[base]
        except KeyError:
            raise APIException(f"не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"не удалось обработать количество {amount}")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}')
        total_quote = json.loads(r.content)[keys[quote]]

        return total_quote
