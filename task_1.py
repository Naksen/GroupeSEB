import requests
import xmltodict
import json
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_and_save_exchange_rates():
    """
    Получает курсы валют USD/RUB и EUR/RUB за последнюю неделю относительно текущей даты
    с использованием открытого API Центрального банка России. Результат сохраняется в JSON файл.
    """
    base_url = "http://www.cbr.ru/scripts/XML_daily.asp"

    current_day = datetime.now()

    previous_days = [current_day - timedelta(days=i) for i in range(0, 7)]
    formatted_previous_days = [day.strftime("%d.%m.%Y") for day in previous_days]

    currency_data = []

    for date in formatted_previous_days:
        try:
            response = requests.get(f"{base_url}?date_req={date}")
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {e}")
            return

        if response.status_code != 200:
            logger.error(f"API request error: {response.status_code}")
            return

        try:
            xml_data = xmltodict.parse(response.text)
            usd_rate, eur_rate = None, None

            for valute in xml_data["ValCurs"]["Valute"]:
                char_code = valute["CharCode"]
                value = valute["Value"].replace(",", ".")

                if char_code == "USD":
                    usd_rate = float(value)
                elif char_code == "EUR":
                    eur_rate = float(value)

            currency_data.append(
                {
                    "date": date,
                    "USD/RUB": usd_rate,
                    "EUR/RUB": eur_rate,
                }
            )

        except xmltodict.ParsingInterrupted:
            logger.error("Error processing XML")
            return

    json_file_name = f"currency_data_{current_day.strftime('%d-%m-%Y')}.json"
    try:
        with open(json_file_name, "w") as json_file:
            json.dump(currency_data, json_file, indent=2)
    except OSError:
        logger.error("OSError")
        return


get_and_save_exchange_rates()
