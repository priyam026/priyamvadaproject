
import threading
from queue import Queue
from spider import Spider
from dom import *
from gen import *
from download import *


PROJECT_NAME = 'web'
HOMEPAGE = 'https://en.wikipedia.org/wiki/Special:Search?search=list+of+keywords+in+python&go=Go&ns0=1'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME +'/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        th = threading.Thread(target=work)
        th.daemon = True
        th.start()


# Do the next job in the queue

def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        jobs()


create_workers()
crawl()
save(response,"web/files")