import requests
import time
import sys
import threading
import asyncio
import concurrent.futures

n = int(sys.argv[1])

headers = {'accept': 'application/json'}

url_work = 'http://localhost:5000/work'
url_us = 'http://localhost:5000/work/us'
url_us0 = 'http://localhost:5000/work/us/0'
url_us1 = 'http://localhost:5000/work/us/1'
url_emea = 'http://localhost:5000/work/emea'
url_asia = 'http://localhost:5000/work/asia'
url_asia0 = 'http://localhost:5000/work/asia/0'
url_asia1 = 'http://localhost:5000/work/asia/1'

def wake_up_servers():
    # make firsts requests to wake up workers
    requests.get(url_us0)
    requests.get(url_us1)
    requests.get(url_emea)
    requests.get(url_asia0)
    requests.get(url_asia1)

async def policy_s1():
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:

        loop = asyncio.get_event_loop()
        futures_emea = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_emea
            )
            for i in range(n)
        ]
    await asyncio.gather(*futures_emea)
    end_time = time.time()

    return end_time - start_time

async def policy_s2():
    partial_asia = int(n / 3)
    partial_us = int(n / 3)
    partial_eu = n - 2 * int(n / 3)

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:

        loop = asyncio.get_event_loop()
        futures_us = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_us
            )
            for i in range(partial_us)
        ]

        futures_asia = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_asia
            )
            for i in range(partial_asia)
        ]

        futures_emea = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_emea
            )
            for i in range(partial_eu)
        ]

    await asyncio.gather(*futures_us)
    await asyncio.gather(*futures_asia)
    await asyncio.gather(*futures_emea)
    end_time = time.time()

    return end_time - start_time

async def policy_s3():
    partial_asia = int(n / 5)
    partial_us = int(n / 5)
    partial_eu = n - 2 * partial_asia - 2 * partial_us

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:

        loop = asyncio.get_event_loop()
        futures_us_0 = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_us0
            )
            for i in range(partial_us)
        ]

        futures_us_1 = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_us1
            )
            for i in range(partial_us)
        ]

        futures_asia_0 = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_asia0
            )
            for i in range(partial_asia)
        ]

        futures_asia_1 = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_asia1
            )
            for i in range(partial_asia)
        ]

        futures_emea = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_emea
            )
            for i in range(partial_eu)
        ]

    await asyncio.gather(*futures_us_0)
    await asyncio.gather(*futures_us_1)
    await asyncio.gather(*futures_asia_0)
    await asyncio.gather(*futures_asia_1)
    await asyncio.gather(*futures_emea)
    end_time = time.time()

    return end_time - start_time

async def policy_s4():
    partial_asia = int(n / 19 * 3)
    partial_us = int(n / 19 * 4)
    partial_eu = n - 2 * partial_asia - 2 * partial_us

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:

        loop = asyncio.get_event_loop()
        futures_us_0 = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_us0
            )
            for i in range(partial_us)
        ]

        futures_us_1 = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_us1
            )
            for i in range(partial_us)
        ]

        futures_asia_0 = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_asia0
            )
            for i in range(partial_asia)
        ]

        futures_asia_1 = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_asia1
            )
            for i in range(partial_asia)
        ]

        futures_emea = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                url_emea
            )
            for i in range(partial_eu)
        ]

    await asyncio.gather(*futures_us_0)
    await asyncio.gather(*futures_us_1)
    await asyncio.gather(*futures_asia_0)
    await asyncio.gather(*futures_asia_1)
    await asyncio.gather(*futures_emea)
    end_time = time.time()

    return end_time - start_time

if __name__ == "__main__":

    print("Wake up servers\n")
    wake_up_servers()


    print("Started the program\n")


    if n <= 10:
        endtime = asyncio.run(policy_s1())

    elif n <= 50:
        endtime = asyncio.run(policy_s2())

    elif n <= 100:
        endtime = asyncio.run(policy_s3())

    else:
        endtime = asyncio.run(policy_s4())
        
    print("End time = " + str(endtime))
    print("Average time per request = " + str(endtime/n))

    print("\nClosing the program...")












