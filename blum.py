import requests
import time
import os

auth_token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiQUNDRVNTIiwiaXNzIjoiYmx1bSIsInN1YiI6Ijg3YzI0OTgwLWI1NGItNGY2MS04Nzc0LWIzM2M4NTBhZGIxMiIsImV4cCI6MTcyNTIxNTM4NCwiaWF0IjoxNzI1MjExNzg0fQ.MDm1pt25-IJgLWjr1eE9veX2_HK7ZKa558swXel_PX8"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "authorization": auth_token,
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128", "Microsoft Edge WebView2";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
}

user_me_url = "https://gateway.blum.codes/v1/user/me"
balance_me_url = "https://game-domain.blum.codes/api/v1/user/balance"
tasks_url = "https://game-domain.blum.codes/api/v1/tasks"
claim_task_url_template = "https://game-domain.blum.codes/api/v1/tasks/{}/claim"
start_task_url_template = "https://game-domain.blum.codes/api/v1/tasks/{}/start"
farming_start_url = "https://game-domain.blum.codes/api/v1/farming/start"

def get_user_info():
    for attempt in range(3): 
        response = requests.get(user_me_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code in [520, 500, 412]:
                print(f"status code {response.status_code}. Retrying...")
                time.sleep(2) 
        else:
            print(f"Failed to retrieve user info: {response.status_code}")
            return None

def start_farming():
    for attempt in range(3):  
        response = requests.post(farming_start_url, headers=headers)
        if response.status_code == 200:
            print("Farming started successfully.")
        elif response.status_code in [520, 500, 412]:
                print(f"status code {response.status_code}. Retrying...")
                time.sleep(2) 
        else:
            print(f"Failed to start farming: {response.status_code}")

def process_tasks():
    tasks_data = get_tasks()
    
    if isinstance(tasks_data, list):
        not_started_tasks = []
        failed_to_start_tasks = []
        
        for task_group in tasks_data:
            if isinstance(task_group, dict) and "tasks" in task_group:
                for task in task_group["tasks"]:
                    task_id = task.get('id')
                    status = task.get('status')
                    title = task.get('title')
                    
                    print(f"ID: {task_id}, Status: {status}, Title: {title}")

                    if status == "NOT_STARTED":
                        try:
                            start_task(task_id)
                            print(f"Task {task_id} started successfully.")
                        except Exception as e:
                            print(f"Failed to start task {task_id}: {e}")
                            failed_to_start_tasks.append(task_id)
                    
                    try:
                        claimed = claim_task(task_id)
                        if claimed:
                            print(f"Task {task_id} claimed successfully.")
                        else:
                            print(f"Task {task_id} already claimed.")
                    except Exception as e:
                        print(f"Failed to claim task {task_id}: {e}")
                        
    else:
        print("Unexpected response format for tasks.")

def get_tasks():
    for attempt in range(3):
        response = requests.get(tasks_url, headers=headers)
        if response.status_code == 200:
            return response.json() 
        elif response.status_code in [520, 500, 412]:
            print(f"status code {response.status_code}. Retrying...")
            time.sleep(2) 
        else:
            print(f"Failed to retrieve tasks: {response.status_code}")
            return {}

def get_user_balance():
    for attempt in range(3): 
        response = requests.get(balance_me_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code in [520, 500, 412]:
            print(f"status code {response.status_code}. Retrying...")
            time.sleep(2)  
        else:
            print(f"Failed to retrieve user balance: {response.status_code}")
            return None

def start_task(task_id):
    start_task_url = f"https://game-domain.blum.codes/api/v1/tasks/{task_id}/start"
    for attempt in range(3):  
        response = requests.post(start_task_url, headers=headers)
        if response.status_code == 200:
            print(f"Task {task_id} started successfully.")
            return True
        elif response.status_code in [520, 500, 412]:
            print(f"Failed to start task {task_id}, status code {response.status_code}. Retrying...")
            time.sleep(2) 
        else:
            print(f"Failed to start task {task_id}: {response.status_code}")
            return False
    return False

def claim_task(task_id):
    claim_url = f"{tasks_url}/{task_id}/claim"
    for attempt in range(3): 
        response = requests.post(claim_url, headers=headers)
        if response.status_code == 200:
            print(f"Task {task_id} claimed successfully.")
            return True
        elif response.status_code in [520, 500, 412]:
            print(f"Failed to claim task {task_id}, status code {response.status_code}. Retrying...")
            time.sleep(2) 
        elif response.status_code == 400:
            print(f"Task {task_id} already claimed.")
            return False
        else:
            print(f"Failed to claim task {task_id}: {response.status_code}")
            return False
    return False
               
if __name__ == "__main__":
    os.system('cls')
    print("BLUM by @xazhm | https://github.com/xazhm")
    data = get_tasks()
    user_info = get_user_info()
    if user_info:
        username = user_info.get('username', 'Unknown')
        print("User Info:")
        print(f"> {username}")
    
    user_balance = get_user_balance()
    if user_balance:
        available_balance = user_balance.get('availableBalance', '0')
        play_passes = user_balance.get('playPasses', 0)
        print("Balance:")
        print(f"{available_balance} | playPasses {play_passes}")
        print("FARMING:")
        start_farming()
    
    tasks_data = get_tasks()
    if tasks_data:
        not_started_tasks = []
        failed_to_start_tasks = []
        for task_group in tasks_data:
            if "tasks" in task_group:
                for task in task_group["tasks"]:
                    task_status = task.get("status")
                    if task_status == "NOT_STARTED":
                        task_id = task.get("id")
                        task_title = task.get("title")
                        print(f"ID: {task_id}, Status: {task_status}, Title: {task_title}")
                        if not start_task(task_id):
                            failed_to_start_tasks.append(task_id)
                        else:
                            not_started_tasks.append(task_id)

        print("\nCLAIM TASKS:")
        for task_id in not_started_tasks:
            claim_task(task_id)
        
        print("\nCLAIM TASKS [2]:")
        process_tasks()
        
        if failed_to_start_tasks:
            print("\nFailed to start tasks:")
            for task_id in failed_to_start_tasks:
                print(f"ID: {task_id} failed to start.")
    
    print("\nCLAIM TASKS [3]:")
    process_tasks()
    print("\nDONE 100%!")