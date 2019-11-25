# Asynchronous requests with thread pool
import asyncio
import concurrent.futures
import requests
import time
import sys

nr_requests = int(sys.argv[1])
url = 'http://localhost:5000/work/emea'

async def main():

    with concurrent.futures.ThreadPoolExecutor(max_workers=nr_requests) as executor:

        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url
            )
            for i in range(nr_requests)
        ]
        for response in await asyncio.gather(*futures):
            if response.status_code != 200:
                print(response.status_code)


loop = asyncio.get_event_loop() 

start_time = time.time()
loop.run_until_complete(main())
end_time = time.time() - start_time
print(end_time)
print(end_time/nr_requests)


