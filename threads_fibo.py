def fibonacci(num):
    """
    Calculates the highest Fibo value or the value at given n
    :param num: n
    :return: nth fibonacci value
    """
    a,b = 0,1
    for item in range(num):
        a,b=b,a+b
    return a



# print(fibonacci(10))


#########################################
  # Fibo using threads in three steps #
#########################################

#coding: uft-8

import logging, threading
from queue import Queue

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

fibo_dict ={}
shared_queue = Queue()
input_list = [3,10,5,7]

# The condition
queue_condition = threading.Condition()

# Function to be executed by several threads

def fibonacci_task(condition):
    with condition:
        while shared_queue.empty():
            logger.info("[%s] - waiting for elements in queue.." % threading.current_thread().name)
            condition.wait()
        else:
            value = shared_queue.get()
            a,b = 0,1
            for item in range(value):
                a,b=b,a+b
                fibo_dict[value]=a
        shared_queue.task_done()
        logger.debug("[%s] fibonacci of key [%d] with result [%d] "% (threading.current_thread().name, value, fibo_dict[value]))

def queue_task(condition):
    logging.debug('Starting queue_task')
    with condition:
        for item in input_list:
            shared_queue.put(item)
        logging.debug("Notifying fibonacci_task threads that the queue is ready to cosume..")
        condition.notifyAll()

threads = [threading.Thread(
    daemon = True, target=fibonacci_task, args = (queue_condition,))for i in range(4)]


[thread.start() for thread in threads]

prod = threading.Thread(name='queue_task_thread', daemon=True, target=queue_task, args=(queue_condition, ))
prod.start()

[thread.join() for thread in threads]
