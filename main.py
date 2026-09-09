from tasks import TaskManager
from goals import GoalManager
from finance import FinanceManager
from assistant import Assistant
import requests

goal_manager = GoalManager()
finance_manager = FinanceManager()
task_manager = TaskManager()

assistant = Assistant(finance_manager, task_manager)


def ask_task_index(task_manager):
    """Show tasks and get a valid 0-based index. Returns None if cancelled."""
    task_manager.view_tasks()

    while True:
        answer = input("which task? (0 to cancel) ").strip()

        if not answer.isdigit():
            print("please enter a number")
            continue

        number = int(answer)

        if number == 0:
            return None

        if 1 <= number <= len(task_manager.get_tasks()):
            return number - 1

        print("no task with that number")

# main loop
while True:

    print("1 - tasks.")
    print("2 - goals.")
    print("3 - finance.")
    print("4 - assistant.")
    print("0 - exit .")

    option = input("choose an option: ")
    # tasks menu
    if option == "1":
        while True:
            print("1 - add task")
            print("2 - view tasks")
            print("3 - complete task")
            print("4 - delete task")
            print("5 - edit task")
            print("0 - back")

            option_1 = input("choose an option: ")

            if option_1 == "1":
                while True:
                    title = input("title: ")
                    deadline = input("deadline (YYYY-MM-DD): ")
                    priority = input("priority (high/medium/low): ")
                    try:
                        task_manager.add_task(title , deadline, priority)
                        print("task added")
                        break
                    except ValueError as error:
                        print(error)    

            elif option_1 == "2":
                task_manager.view_tasks()

            elif option_1 == "3":
                if not task_manager.get_tasks():
                    print("no tasks available")
                    continue

                index = ask_task_index(task_manager)

                if index is not None:
                    task_manager.complete_task(index)
                    print("task completed")
                            
            elif option_1 == "4":
                if not task_manager.get_tasks():
                    print("no tasks available")
                    continue

                index = ask_task_index(task_manager)

                if index is not None:
                    task_manager.delete_task(index)
                    print("task deleted")

            elif option_1 == "5":
                if not task_manager.get_tasks():
                    print("no tasks available")
                    continue

                index = ask_task_index(task_manager)

                if index is None:
                    continue

                print("1 - edit title")
                print("2 - edit deadline")
                print("3 - edit priority")
                print("0 - cancel")

                field = input("which field? ")

                if field == "1":
                    new_title = input("new title: ")
                    try:
                        task_manager.edit_title(index, new_title)
                        print("title updated")
                    except ValueError as error:
                        print(error)

                elif field == "2":
                    new_deadline = input("new deadline (YYYY-MM-DD): ")
                    try:
                        task_manager.edit_deadline(index, new_deadline)
                        print("deadline updated")
                    except ValueError as error:
                        print(error)

                elif field == "3":
                    new_priority = input("new priority (high/medium/low): ")
                    try:
                        task_manager.edit_priority(index, new_priority)
                        print("priority updated")
                    except ValueError as error:
                        print(error)

                elif field == "0":
                    print("cancelled")

                else:
                    print("invalid option")
                                        
            elif option_1 == "0":
                print("going back")
                break        
            else:
                print("invalid option")

   # Goals menu
    elif option == "2":
        while True:
            print("1 - add goal")
            print("2 - view goal")
            print("3 - update goal")
            print("4 - delete goal")
            print("0 - back")
        
            option_2 = input("choose an option: ")
        
            if option_2 == "1":
                title = input("enter goal title: ")
                goal_manager.add_goal(title)
        
            elif option_2 == "2":
                goal_manager.view_goals()
        
            elif option_2 == "3":
                goal_manager.update_goal()

            elif option_2 == "4":
                goal_manager.delete_goal()

            elif option_2 == "0":
                print("going back")
                break        
            else:
                print("invalid option")
        
    # finance menu
    elif option == "3":
        while True:
            print("\n===== FINANCE =====")
            print("1 - add income")
            print("2 - add spending")
            print("3 - view current balance")
            print("4 - view transaction history")
            print("5 - view spending by category")
            print("0 - back")

            option_3 = input("choose an option: ")

            if option_3 == "1":
                try:
                    amount = float(input("income amount: "))
                except ValueError:
                    print("please enter a valid number")
                    continue

                try:
                    finance_manager.add_income(amount)
                    print("income added successfully")
                except ValueError as error:
                    print(error)


            elif option_3 == "2":
                try:
                    amount = float(input("spending amount: "))
                except ValueError:
                    print("please enter a valid number")
                    continue

                print("\nAvailable categories:")
                for category in finance_manager.categories:
                    print(f"- {category}")

                category = input("category: ")
                description = input("description: ")

                try:
                    finance_manager.add_spending(amount, category, description)
                    print("spending added successfully")
                except ValueError as error:
                    print(error)



            elif option_3 == "3":
                balance = finance_manager.get_balance()
                print(f"Current balance: {balance:.2f} SAR")


            elif option_3 == "4":
                finance_manager.view_history()


            elif option_3 == "5":
                finance_manager.view_spending_by_category()


            elif option_3 == "0":
                print("going back")
                break


            else:
                print("invalid option")

    elif option == "4":
        print("type a message, or 'back' to return")
        while True:
            message = input("> ")
            if message.lower().strip() == "back":
                break
            try:
                assistant.handle_message(message)            
            except requests.RequestException as error:
                print(f"connection problem: {error}")
    #exit
    elif option == "0":
        print("exit")
        break

    else:
        print("invalid option")