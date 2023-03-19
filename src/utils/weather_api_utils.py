import request


def get_weather_by_date(date: str):
    # date example - 2023-03-19
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/moscow/{date}/{date}?unitGroup=metric&include=days&key=LZNGP9R5WS55CXBTUREGA5S5N&contentType=json"
    response = request.get(url).text

    return response
