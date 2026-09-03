import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "goals.json"
DATA_FILE.parent.mkdir(exist_ok=True)

class Goal:
    def __init__(self , title):
        self.title = title
        #completion in percentage "100%"
        self.target = 100
        self.current = 0
        self.completed = False

    def update_progress(self, amount):
        self.current += amount
        if self.current >= self.target:
            self.completed = True
            self.current = self.target

    def to_dict(self):
            return {
                "title" : self.title,
                "target" : self.target,
                "current" : self.current,
                "completed" : self.completed
            }
    @classmethod
    def from_dict(cls, data):
        goal = cls(data["title"])

        goal.target = data["target"]
        goal.current = data["current"]
        goal.completed = data["completed"]

        return goal

class GoalManager:
    def __init__(self):
        self.goals = []
        self.load_goals()

    def add_goal(self,title):
        goal = Goal(title)
        self.goals.append(goal)
        self.save_goals()               

    def view_goals(self):
        if len(self.goals) == 0:
            print("No Goals Found!")
        else:
            for index,goal in enumerate(self.goals, start=1):
                if goal.completed:
                    print(f"{index} - [x] {goal.title} | Progress-{goal.current}%-")
                else:
                    print(f"{index} - [ ] {goal.title} | Progress-{goal.current}%-")    

    def update_goal(self):
        if len(self.goals) == 0:
            print("No Goals found!")
        else:
            self.view_goals()
            while True:
                try:
                    goal_number = int(input("which goal whould you like to update: "))

                    if 1 <= goal_number <= len(self.goals):
                        selected_goal = self.goals[goal_number - 1] 

                        while True:
                            try:
                                new_amount = int(input("How much progress: "))
                                if 1<= new_amount <= 100:
                                    selected_goal.update_progress(new_amount)
                                    self.save_goals()
                                    print("Goal updated")
                                    return
                                else:
                                    print("amount must be 1 - 100 !")
                            except ValueError:
                                print("cannot type in a string")        
                    else:
                        print("invalid option")
                except ValueError:
                    print("cannot type in a string")

    def delete_goal(self):
        if len(self.goals) == 0:
                    print("No Goals found!")
        else:
            self.view_goals()

            while True:
                    try:
                        goal_number = int(input("which goal whould you like to delete: "))
            
                        if 1 <= goal_number <= len(self.goals): 
                            self.goals.pop(goal_number - 1)
                            self.save_goals()
                            print("goal deleted")
                            break
                        else:
                            print("invalid option")
                    except ValueError:
                            print("cannot type in a string")

    def save_goals(self):
        goals_data = []

        for goal in self.goals:
            goals_data.append(goal.to_dict())

        with open("data/goals.json", "w") as file:
            json.dump(goals_data, file, indent=4)

    def load_goals(self):
        try:
            with open("data/goals.json", "r") as file:
                goals_data = json.load(file)
                self.goals = []  # clear list before loading

                for data in goals_data:
                    goal = Goal.from_dict(data)
                    self.goals.append(goal)
        except (FileNotFoundError, json.JSONDecodeError):
            self.goals = []



