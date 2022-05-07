import time
import threading
import schedule
import sympy
# 创建调度器
scheduler = schedule.Scheduler()

def myJob1 ():
    print (' Jobl:我10秒执行依次,每次执行3秒钟')
    time. sleep (3)

toCancel=scheduler.every (10).seconds.do(myJob1)

def myJob2 ():
    print (' Job2:我1分钟执行依次,每次执行5秒钟')
    time.sleep(5)

scheduler.every(1).minutes.do(myJob2)

def cancelTest():
    for _ in range (200):
        time. sleep (1)
    print('我取消了一个任务噢。。。')
    scheduler.cancel_job(toCancel)

threading.Thread(target=cancelTest).start()

while True:
    scheduler.run_pending()
    time.sleep(1)