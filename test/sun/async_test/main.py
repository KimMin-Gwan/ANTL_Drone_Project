import asyncio
import time
from threading import Thread
my_number=0
async def print_async():
    while True:
        m=get_number()
        print(m) 
        await asyncio.sleep(1)
        
def print_thread():
    while True:
        int_number=int(input("input_your number"))
        set_number(int_number)
        time.sleep(3)




def set_number(a):
    global my_number
    my_number=a

def get_number():
    return my_number
 
thread_a=Thread(target=print_thread)

thread_a.start()
asyncio.run(print_async())



        