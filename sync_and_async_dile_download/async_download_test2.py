import httpx
import asyncio
from time import perf_counter
from tqdm import tqdm


def async_execute_time_deco(func):
    async def inner(*args):
        start = perf_counter()
        func_result = await func(*args)
        stop = perf_counter()
        executed_for = round(stop - start, 3)
        print(f"Function executed for {executed_for}")
        return func_result
    return inner

async def load_file(url: str, filename: str):
    with open(f"sync_and_async_dile_download/{filename}", 'wb') as file:
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', url=url) as stream:
                stream.raise_for_status()

                file_size = int(stream.headers.get('content-length', 0))
                tqdm_params = {
                    'desc': f'{filename} download in progress',
                    'miniters': 1,
                    'total': file_size,
                    'unit': 'it',
                    'unit_divisor': 1024,
                    'unit_scale': True
                }

                with tqdm(**tqdm_params) as progres_bar:
                    async for chunk in stream.aiter_bytes():
                        progres_bar.update(len(chunk))
                        file.write(chunk)


@async_execute_time_deco
async def main():
    urls = [
        ('http://ipv4.download.thinkbroadband.com/50MB.zip', '50MB.zip'),
        ('http://ipv4.download.thinkbroadband.com/100MB.zip','100MB.zip'),
        ('http://ipv4.download.thinkbroadband.com/200MB.zip', '200MB.zip')
    ]

    await asyncio.gather(*[load_file(url=url, filename=filename) for url, filename in urls])


if __name__ == '__main__':
    asyncio.run(main())