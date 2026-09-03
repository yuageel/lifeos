from datetime import datetime
import json
from pathlib import Path



DATA_FILE = Path(__file__).parent / "data" / "tasks.json"
DATA_FILE.parent.mkdir(exist_ok=True)



def load_tasks():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) :
        return []

    
tasks = load_tasks()
priorities = ["low","medium","high"]

def add_task():
    new_task = input("enter task title: ")
    while True:
        try:
            task_deadline = input("enter task deadline (YYYY-MM-DD):").strip()
            datetime.strptime(task_deadline, "%Y-%m-%d")
            break
        except ValueError:
            print("invalid input")    

    while True:
        task_priority = input("enter priority (low/medium/high): ").lower().strip()
        if task_priority in priorities:
            break
        else:
            print("invalid priority!")

    tasks.append({
                "title" : new_task ,
                 "completed" : False,
                 "priority" : task_priority,
                 "deadline" : task_deadline
                 })
    save_tasks()
    
    print("task added successfully")


def view_tasks():
    if len(tasks) == 0:
        print("No tasks found.")
    else:
        today = datetime.today().date()
        for index, task in enumerate(tasks, start=1):
            deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
            if task["completed"]:
                print(f"{index} - [x] {task['title']} | deadline: {task['deadline']} | priority: {task['priority']}")
            elif deadline <  today:
                print(f"{index} - [ ] {task['title']} | deadline: {task['deadline']} | priority: {task['priority']} | OVERDUE")   
            else:
                print(f"{index} - [ ] {task['title']} | deadline: {task['deadline']} | priority: {task['priority']}")


def complete_task():
    if len(tasks) == 0:
        print("No tasks available")
    else:    
        view_tasks()
        while True:
            try:
                task_number = int(input("which task number: "))
                if 1 <= task_number <= len(tasks):
                    task_number -= 1
                    tasks[task_number]["completed"] = True
                    save_tasks()
                    print("task set to complete")
                    break
                else:
                    print("No task found")
            except ValueError:
                print("cannot type a string")

def delete_task():
    if len(tasks) == 0:
        print("No tasks available")
    else:    
        view_tasks()
        while True:
            try:
                task_number = int(input("which task do you want to delete : "))
                if 1 <= task_number <= len(tasks):
                    task_number -= 1
                    tasks.pop(task_number)
                    save_tasks()
                    print("task deleted")
                    break
                else:
                    print("no task found")
            except ValueError:
                print("cannot type a string")

def edit_task():
    if len(tasks) == 0:
        print("no tasks available")
    else:
            
        while True:
            view_tasks()
            try:
                task_number = int(input("which task do you want to edit ( 0 to cancel): "))
                if 1 <= task_number <= len(tasks):
                    task_number -= 1
                    
                    print("1 - edit title")
                    print("2 - edit deadline")
                    print("3 - edit priority")
                    print("0 - go back")
                    while True:
                        try:
                            part = int(input("which part would you like to edit: "))
                            if part == 1:
                                tasks[task_number]["title"] = input("enter new task title: ")
                                save_tasks()
                                print("title updated!")
                                return
                            elif part == 2:
                                while True:
                                    try:
                                        new_deadline = input("enter NEW task deadline (YYYY-MM-DD): ").strip()
                                        datetime.strptime(new_deadline, "%Y-%m-%d")
                                        tasks[task_number]["deadline"] = new_deadline
                                        save_tasks()
                                        print("deadline updated")
                                        return
                                    except ValueError:
                                        print("invalid input")
                                 

                            elif part == 3:
                                while True:
                                    new_priority = input("enter priority (low/medium/high): ").lower().strip()
                                    if new_priority in priorities:
                                        tasks[task_number]["priority"] = new_priority
                                        save_tasks()
                                        print("priority updated")
                                        return
                                    else:
                                         print("invalid priority!")

                            elif part == 0 :
                                return

                            else:
                                print("invalid option")
                        except ValueError:
                            print("cannot type a string")

                elif task_number == 0:
                    return
                else:
                    print("no task found")
            except ValueError:
                    print("cannot type a string")    

    

        



def save_tasks():
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)