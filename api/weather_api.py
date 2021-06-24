import fastapi
import httpx

from models.location import Location
from models.umbrella_status import UmbrellaStatus

router = fastapi.APIRouter()


@router.get('/api/umbrella', response_model=UmbrellaStatus)
async def do_i_need_an_umbrella(location: Location = fastapi.Depends()):
    url = f"https://weather.talkpython.fm/api/weather?city={location.city}&country={location.country}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

        data = resp.json()
        weather = data.get('weather', {})
        category = weather.get('category', 'unknown')
        forecast = data.get('forecast', {})

    status = UmbrellaStatus(bring_umbrella=category.lower().strip() == 'rain', temp=forecast.get('temp', 0))

    return status
