import asyncio
import aiohttp

list_ = []


class UrlInfo:
    def __init__(self, url, pages, key_name):
        self.url = url
        self.pages = pages
        self.key_name = key_name


async def get(
        session: aiohttp.ClientSession,
        ui: UrlInfo,
        **kwargs
) -> list:
    urls = []
    for page in ui.pages:
        urls.append(ui.url + f"page={page}")
    for url in urls:
        print(f"Requesting {url}")
        resp = await session.request('GET', url=url, **kwargs)
        data = await resp.json()
        character_ = [{"id": x['id'], "name": x['name']} for x in data[ui.key_name]]
        list_.extend(character_)
    return list_


async def main(url_infos, **kwargs):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for ui in url_infos:
            tasks.append(get(session=session, ui=ui, **kwargs))
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        return htmls


if __name__ == '__main__':
    uis = [UrlInfo(url='https://rickandmortyapi.com/api/character/?', pages=(2, 4), key_name='results'),
           UrlInfo(url='https://spapi.dev/api/characters?', pages=(1, 2, 5, 6), key_name='data')]
    asyncio.run(main(uis))
    print(list_)
    print(sorted(list_, key=lambda k: k['id']))
