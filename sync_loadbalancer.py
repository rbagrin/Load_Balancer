import requests
import time
import sys
import threading

nr_requests = int(sys.argv[1])

url_work = 'http://localhost:5000/work'
url_us = 'http://localhost:5000/work/us'
url_us0 = 'http://localhost:5000/work/us/0'
url_us1 = 'http://localhost:5000/work/us/1'
url_emea = 'http://localhost:5000/work/emea'
url_asia = 'http://localhost:5000/work/asia'
url_asia0 = 'http://localhost:5000/work/asia/0'
url_asia1 = 'http://localhost:5000/work/asia/1'

# make firsts requests to wake up workers
def wake_up_servers():

    requests.get(url_us0)
    requests.get(url_us1)
    requests.get(url_emea)
    requests.get(url_asia0)
    requests.get(url_asia1)

def make_get_requests_s(n, url):

    for _ in range(n):
        requests.get(url)

def policy_sync1(n):

    start_time = time.time()
    make_get_requests_s(n, url_emea)
    end_time = time.time()

    return end_time - start_time

def policy_sync2(n):

    partial12 = int(n / 3)
    partial3 = n - 2 * partial12

    threads = list()

    start_time = time.time()

    asia = threading.Thread(target=make_get_requests_s, args=(partial12, url_asia,))
    threads.append(asia)
    asia.start()

    us = threading.Thread(target=make_get_requests_s, args=(partial12, url_us,))
    threads.append(us)
    us.start()

    emea = threading.Thread(target=make_get_requests_s, args=(partial3, url_emea,))
    threads.append(emea)
    emea.start()

    for thread in threads:
        thread.join()
    
    end_time = time.time()

    return end_time - start_time

def policy_sync3(n):

    partial1234 = int(n / 5)
    partial5 = n - 4 * partial1234

    threads = list()

    start_time = time.time()

    asia0 = threading.Thread(target=make_get_requests_s, args=(partial1234, url_asia0,))
    threads.append(asia0)
    asia0.start()

    asia1 = threading.Thread(target=make_get_requests_s, args=(partial1234, url_asia1,))
    threads.append(asia1)
    asia1.start()

    us0 = threading.Thread(target=make_get_requests_s, args=(partial1234, url_us0,))
    threads.append(us0)
    us0.start()

    us1 = threading.Thread(target=make_get_requests_s, args=(partial1234, url_us1,))
    threads.append(us1)
    us1.start()

    emea = threading.Thread(target=make_get_requests_s, args=(partial5, url_emea,))
    threads.append(emea)
    emea.start()

    for thread in threads:
        thread.join()
    
    end_time = time.time()

    return end_time - start_time

def policy_sync4(n):

    partial_asia = int(n / 19 * 3)
    partial_us = int(n / 19 * 4)
    partial_eu = n - 2 * partial_asia - 2 * partial_us

    threads = list()

    start_time = time.time()

    asia0 = threading.Thread(target=make_get_requests_s, args=(partial_asia, url_asia0,))
    threads.append(asia0)
    asia0.start()

    asia1 = threading.Thread(target=make_get_requests_s, args=(partial_asia, url_asia1,))
    threads.append(asia1)
    asia1.start()

    us0 = threading.Thread(target=make_get_requests_s, args=(partial_us, url_us0,))
    threads.append(us0)
    us0.start()

    us1 = threading.Thread(target=make_get_requests_s, args=(partial_us, url_us1,))
    threads.append(us1)
    us1.start()

    emea = threading.Thread(target=make_get_requests_s, args=(partial_eu, url_emea,))
    threads.append(emea)
    emea.start()

    for thread in threads:
        thread.join()
    
    end_time = time.time()

    return end_time - start_time

if __name__ == "__main__":

    print("Wake up servers\n")
    wake_up_servers()

    print("Started the program\n")

    if nr_requests <= 10:
        endtime = policy_sync1(nr_requests)

    elif nr_requests <= 50:
        endtime = policy_sync2(nr_requests)

    elif nr_requests <= 100:
        endtime = policy_sync3(nr_requests)
    
    else:
        endtime = policy_sync4(nr_requests)
        
    print("End time = " + str(endtime))
    print("Average time per request = " + str(endtime / nr_requests))

    print("\nClosing the program...")

