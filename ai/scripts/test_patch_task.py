import requests


BASE_URL = "http://127.0.0.1:5000"

def test_patch_task():
    
    task_id = "sample-task-id"

    
    payload = {
        "completed": True
    }

    response = requests.patch(f"{BASE_URL}/task/{task_id}", json=payload)

    if response.status_code == 200:
        print(" Task updated successfully!")
        print("Response JSON:", response.json())
    else:
        print(" Failed to update task")
        print("Status code:", response.status_code)
        print("Response:", response.text)

if __name__ == "__main__":
    test_patch_task()
