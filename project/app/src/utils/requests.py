import httpx


class Request:

    async def execute(self, method: str, url: str, headers: dict = None):
        if not headers:
            headers = {}
        async with httpx.AsyncClient() as client:
            match method:
                case "POST":
                    return await self.__post(url, headers, client)
                case "GET":
                    return await self.__get(url, headers, client)
                case _:
                    raise ValueError(f"Invalid method - {method}")

    async def __get(self, url: str, headers: dict, client: httpx.AsyncClient):
        response = await client.get(url, headers=headers)
        return response

    async def __post(self, url: str, headers: dict, client: httpx.AsyncClient):
        response = await client.post(url, headers=headers)
        return response
