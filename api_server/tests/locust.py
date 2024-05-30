from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task
    def login(self):
        url = '/api/auth/login'
        params = {
            'username': 'user1',
            'password': 'password1'
        }
        headers = {
            'accept': '*/*'
        }
        self.client.post(
            url,
            params=params,
            headers=headers     
        )

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.1, 0.5)

