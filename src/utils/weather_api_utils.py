import aiohttp


async def get_weather_by_date(date: str):
    session = aiohttp.ClientSession()

    # date example - 2023-03-19
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/moscow/{date}/{date}?unitGroup=metric&include=days&key=LZNGP9R5WS55CXBTUREGA5S5N&contentType=json"
    async with session.get(url=url) as response:
        response_text = await response.json()

    return response_text
