from datetime import datetime
import json

from pathlib import Path
DATA_FILE = Path(__file__).parent / "data" / "tasks.json"
DATA_FILE.parent.mkdir(exist_ok=True)


class Tasks:
    def __init__(self, title , deadline, priority):
        self.title = title
        self.deadline = deadline
        self.priority = priority
        self.completed = False


class TaskManager:

    def load_tasks(self):
            try:
                with open(DATA_FILE, "r") as file:
                    self.tasks = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError) :
                self.tasks = []        
            
    def __init__(self):
        self.tasks = []
        self.priorities = ["high" , "medium" , "low"]
        self.load_tasks()

    def save_tasks(self):
        with open(DATA_FILE , "w") as file:
            json.dump(self.tasks , file , indent=4)

    def _check_index(self ,index):
        if index < 0 or index >= len(self.tasks):
            raise ValueError(f"no task at index {index}")
   

    def add_task(self, title, deadline, priority):
        title = title.strip()
        deadline = deadline.strip()
        priority = priority.lower().strip()

        if not title:
            raise ValueError("title cannot be empty")

        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"invalid deadline: {deadline} (expected YYYY-MM-DD)")

        if priority not in self.priorities:
            raise ValueError(f"invalid priority: {priority} (expected low, medium, or high)")
        

        self.tasks.append({
                "title" : title,
                "deadline" : deadline,
                "priority" : priority,
                "completed" : False
            })
        self.save_tasks()

    def get_tasks(self):
        return self.tasks

    def view_tasks(self):
        if len(self.tasks) == 0:
            print("No tasks found.")
        else:
            today = datetime.today().date()
            for index, task in enumerate(self.tasks, start=1):
                deadline = datetime.strptime(task["deadline"], "%Y-%m-%d").date()
                if task["completed"]:
                    print(f"{index} - [x] {task['title']} | deadline: {task['deadline']} | priority: {task['priority']}")
                elif deadline <  today:
                    print(f"{index} - [ ] {task['title']} | deadline: {task['deadline']} | priority: {task['priority']} | OVERDUE")   
                else:
                    print(f"{index} - [ ] {task['title']} | deadline: {task['deadline']} | priority: {task['priority']}")


    def complete_task(self, index):
        self._check_index(index)

        self.tasks[index]["completed"] = True
        self.save_tasks()

    def delete_task(self , index):
        self._check_index(index)

        self.tasks.pop(index) 
        self.save_tasks() 

    def edit_title(self , index, new_title):
        self._check_index(index)
        if not new_title:
            raise ValueError("title cannot be empty")

        self.tasks[index]["title"] = new_title
        self.save_tasks()

    def edit_deadline(self , index , new_deadline):
        self._check_index(index)
        new_deadline = new_deadline.strip()

        try:
            datetime.strptime(new_deadline, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"invalid deadline: {new_deadline} (expected YYYY-MM-DD)")

        self.tasks[index]["deadline"] = new_deadline
        self.save_tasks()

    def edit_priority(self , index , new_priority):
        self._check_index(index)
        new_priority = new_priority.lower().strip()

        if new_priority not in self.priorities:
            raise ValueError(f"invalid priority: {new_priority} (expected low, medium, or high)")

        self.tasks[index]["priority"] = new_priority
        self.save_tasks()

     