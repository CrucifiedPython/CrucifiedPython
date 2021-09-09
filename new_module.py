import asyncio
import aiohttp 

list_ = []


async def get(
        session: aiohttp.ClientSession,
        page: str,
        **kwargs
) -> list:
    url = f"https://rickandmortyapi.com/api/character/?page={page}"
    print(f"Requesting {url}")
    resp = await session.request('GET', url=url, **kwargs)
    data = await resp.json()
    character_ = [{"id": x['id'], "name": x['name']} for x in data['results']]
    #character_ = [x['id'] for x in data['results']]
    list_.extend(character_)
    return list_


async def main(pages, **kwargs):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for p in pages:
            tasks.append(get(session=session, page=p, **kwargs))
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        return htmls


if __name__ == '__main__':
    pages = [1, 2, 3, 4]  # ...
    asyncio.run(main(pages))
    print(list_)
    print(sorted(list_, key=lambda k: k['id']))
