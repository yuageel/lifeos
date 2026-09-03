from tasks import add_task , view_tasks ,complete_task, delete_task, edit_task
from goals import GoalManager
from finance import FinanceManager

goal_manager = GoalManager()
finance_manager = FinanceManager()

# main loop
while True:

    print("1 - tasks.")
    print("2 - goals.")
    print("3 - finance.")
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
                add_task()

            elif option_1 == "2":
                print("------------TASKS--------------")
                view_tasks()
                print("--------------------------------")

            elif option_1 == "3":
                complete_task()
                
            elif option_1 == "4":
                delete_task()

            elif option_1 == "5":
                edit_task()
                              
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

                    if amount > 0:
                        finance_manager.add_income(amount)
                        print("income added successfully")
                    else:
                        print("amount must be greater than 0")

                except ValueError:
                    print("please enter a valid number")


            elif option_3 == "2":
                try:
                    amount = float(input("spending amount: "))

                    if amount <= 0:
                        print("amount must be greater than 0")
                        continue

                    print("\nAvailable categories:")
                    for category in finance_manager.categories:
                        print(f"- {category}")

                    category = input("category: ").lower().strip()
                    description = str(input("description: "))

                    finance_manager.add_spending(
                        amount,
                        category,
                        description
                    )

                except ValueError:
                    print("please enter a valid number")


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
        
    #exit
    elif option == "0":
        print("exit")
        break

    else:
        print("invalid option")