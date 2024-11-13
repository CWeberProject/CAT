import os
import time
import json
import subprocess
import pyautogui
from PIL import ImageGrab
import webbrowser

def perform_action(json_data):

    """
    Perform the action based on the extracted action and coordinates from the JSON.
    Currently, it supports 'click' actions.

    :param action: The action to be performed (e.g., 'click')
    :param coordinates: The coordinates where the action will be performed
    """
    action = json_data.get("ACTION")
    element = json_data.get("ELEMENT")
    details = json_data.get("DETAILS")
    coordinates = json_data.get("COORDINATES")

    if action == "click" and coordinates:
        # pyautogui click action at the specified coordinates
        x1, y1, x2, y2 = coordinates

        x = x1+(x2/2)
        y = y1+(y2/2)
        print(f"Clicking at ({x}, {y})")
        pyautogui.click(x, y)
        time.sleep(1)  # Adding a short delay to avoid too fast execution
        
    elif action == "type" and coordinates:
        x1, y1, x2, y2 = coordinates
        x = x1+(x2/2)
        y = y1+(y2/2)
        print(f"Clicking at ({x}, {y})")
        pyautogui.click(x, y)
        # If the action was 'type', you could use pyautogui to type at certain coordinates
        print(f"Typing at {coordinates}")
        pyautogui.write(details)  # Example text to type, can be modified
        pyautogui.press("enter")
    elif action == "wait":
        time.sleep(5)
    else:
        print("Unsupported action or missing coordinates!")

def open_link_in_fullscreen(url):
    # Open the URL in the default browser
    webbrowser.open(url)
    
    # Wait a few seconds for the browser to load
    time.sleep(15)
    
    # Press F11 to enter full-screen mode
    pyautogui.press('f11')

def load_task(task_local_path, remote_user, remote_host, task_remote_base_path):
    # Prompt for task input
    task_input = input("Please enter a task: ")
    json_task = {
        "task": task_input
    }
    filename = 'task.json'
    with open(filename, 'w') as file:
        json.dump(json_task, file, indent=4)
    print(f"Data saved to {filename}")
    time.sleep(1)

    # Construct the scp command
    scp_command = [
        "scp",
        task_local_path,
        f"{remote_user}@{remote_host}:{task_remote_base_path}",
    ]

    # Execute the SCP command to copy the screenshot
    try:
        scp_result = subprocess.run(scp_command, check=True)
        print("Task successfully copied to remote server.")
    except subprocess.CalledProcessError as e:
        print(f"Error copying task: {e}")


    url_input = input("Please enter a valid url: ")
    open_link_in_fullscreen(url_input)

def load_screenshot(img_local_path,remote_user, remote_host, img_remote_base_path):
    # Save the screenshot to the specified file path
    screenshot = ImageGrab.grab()
    screenshot.save(img_local_path)
    print(f"Screenshot saved to {img_local_path}")
    time.sleep(2)
    # Construct the scp command
    scp_command = [
        "scp",
        img_local_path,
        f"{remote_user}@{remote_host}:{img_remote_base_path}",
    ]

    # Execute the SCP command to copy the screenshot
    try:
        scp_result = subprocess.run(scp_command, check=True)
        print("Screenshot successfully copied to remote server.")
    except subprocess.CalledProcessError as e:
        print(f"Error copying screenshot: {e}")


remote_user = os.getenv('REMOTE_USER'),
remote_host = os.getenv('REMOTE_HOST'),
img_remote_base_path = os.getenv('IMG_REMOTE_BASE_PATH')
img_local_base_path = os.getenv('IMG_LOCAL_BASE_PATH')
remote_base_path = os.getenv('REMOTE_BASE_PATH')
local_base_path = os.getenv('LOCAL_BASE_PATH')
task_remote_base_path = os.getenv('TASK_REMOTE_BASE_PATH')
task_local_path = os.getenv('TASK_LOCAL_PATH')


# Load a task from user input
load_task(task_local_path, remote_user, remote_host, task_remote_base_path)

# Construct the dynamic file name
img_file_name = f"screenshot_0.png"
img_local_path = os.path.join(img_local_base_path, img_file_name)
load_screenshot(img_local_path,remote_user, remote_host, img_remote_base_path)


i = 0
while True:
    # Construct the dynamic file name
    file_name = f"result_{i}.json"
    remote_path = f"{remote_base_path}/{file_name}"
    local_path = os.path.join(local_base_path, file_name)

    # Use SSH to check if the file exists on the remote server
    result = subprocess.run(
        ["ssh", f"{remote_user}@{remote_host}", f"test -f {remote_path} && echo 1 || echo 0"],
        capture_output=True, text=True
    )
    
    # Check the result from the SSH command (if the file exists, result.stdout will be '1')
    if result.stdout.strip() == '1':

        # Download result file
        print(f"File {file_name} exists. Downloading...")
        scp_command = ["scp",f"{remote_user}@{remote_host}:{remote_path}",local_path]
        scp_result = subprocess.run(scp_command)

        # Download parsed screenshot file
        scp_command = ["scp",f"{remote_user}@{remote_host}:{f"{remote_base_path}/{"labled_screenshot_"+str(i)+".png"}"}",
            os.path.join(local_base_path, f"labled_screenshot_"+str(i)+".png")
        ]
        scp_result = subprocess.run(scp_command)
        
        # Check if the file was downloaded successfully
        if scp_result.returncode == 0:
            print(f"Downloaded {file_name} successfully.")
            with open(local_path, 'r') as json_file:
                json_data = json.load(json_file)

            perform_action(json_data)

            # Construct the dynamic file name
            img_file_name = f"screenshot_{i+1}.png"
            img_local_path = os.path.join(img_local_base_path, img_file_name)
            load_screenshot(img_local_path,remote_user, remote_host, img_remote_base_path)

            i += 1  # Increment the file index for the next result
        else:
            print(f"Failed to download {file_name}.")
    else:
        print(f"File {file_name} does not exist yet. Waiting...")
