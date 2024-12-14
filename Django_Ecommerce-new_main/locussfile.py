from locust import HttpUser, task, between

class HelloWordUser(HttpUser): 
    
    wait_time = between(1, 5) 
    
    @task
    def hello_word(self):
        self.client.get("")
    