# This classes enables jobs while the bot is running
# last edit: 21.04.2018 (callFEELD)

import threading 
import time

class Job(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)

    def stuff_to_do(self):
        pass

    def run(self):
        self.stuff_to_do()


class Repeating_Job(Job):

    def __init__(self, job_name, interval_in_seconds):
        threading.Thread.__init__(self)
        self.interval = int(interval_in_seconds)
        self.job_name = job_name

    def run(self):
        self.stuff_to_do()
        time.sleep(self.interval)
        self.run()



r_job = Repeating_Job("one", 5)
r_job2 = Repeating_Job("two", 3)
r_job.start()
r_job2.start()