from datetime import datetime
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "finance.json"
DATA_FILE.parent.mkdir(exist_ok=True)


class Transaction:
    def __init__(self, amount):
        self.amount = amount
        self.date = datetime.now()


class Income(Transaction):
    def __init__(self, amount):
        super().__init__(amount)

    def to_dict(self):
        return{
            "type" : "income",
            "amount" : self.amount,
            "date" : self.date.isoformat()
        }    

    @classmethod
    def from_dict(cls, data):
        income = cls(data["amount"])
        income.date = datetime.fromisoformat(data["date"])
        return income

class Spending(Transaction):
    def __init__(self, amount, category, description):
        super().__init__(amount)
        self.category = category
        self.description = description

    def to_dict(self):
        return {
            "type" : "spending",
            "amount" : self.amount,
            "date" : self.date.isoformat(),
            "category" : self.category,
            "discription" : self.description
        }    

    @classmethod
    def from_dict(cls, data):
        spending = cls(
            data["amount"],
            data["category"],
            data["description"]
        )

        spending.date = datetime.fromisoformat(data["date"])
        return spending

class FinanceManager:
    def __init__(self):
        self.incomes = []
        self.spendings = []
        self.categories = [
            "food",
            "transport",
            "shopping",
            "entertainment",
            "bills",
            "education",
            "other"
        ]
        self.load_finance()

    def load_finance(self):
        try:
            with open("data/finance.json", "r") as file:
                finance_data = json.load(file)

            self.incomes = []
            self.spendings = []

            for data in finance_data["incomes"]:
                income = Income.from_dict(data)
                self.incomes.append(income)

            for data in finance_data["spendings"]:
                spending = Spending.from_dict(data)
                self.spendings.append(spending)

        except (FileNotFoundError, json.JSONDecodeError):
            self.incomes = []
            self.spendings = []    

    def add_income(self, amount):
        income = Income(amount)

        self.incomes.append(income)
        self.save_finance()

    def add_spending(self, amount, category, description):
        category = category.lower().strip()

        if category in self.categories:
            spending = Spending(amount, category, description)
            self.spendings.append(spending)
            self.save_finance()
            return True

        return False


    def get_balance(self):
        total_income = 0
        total_spending = 0

        for income in self.incomes:
            total_income += income.amount

        for spending in self.spendings:
            total_spending += spending.amount

        return total_income - total_spending

    def view_history(self):
        transactions = self.incomes + self.spendings

        if len(transactions) == 0:
            print("No transactions found")
            return

        transactions.sort(key=lambda transaction: transaction.date)

        for transaction in transactions:
            date = transaction.date.strftime("%Y-%m-%d %H:%M")

            if isinstance(transaction , Income):
                print(f"{date} | +{transaction.amount} SAR | Income")
            elif isinstance(transaction , Spending):
                print(
                f"{date} | -{transaction.amount} SAR | "
                f"{transaction.category} | {transaction.description}")

    def view_spending_by_category(self):
        if len(self.spendings) == 0:
            print("No spending found")
            return

        totals = {}

        for category in self.categories:
            totals[category] = 0

        for spending in self.spendings:
            totals[spending.category] += spending.amount

        for category, total in totals.items():
            if total > 0:
                print(f"{category}: {total} SAR") 

    def save_finance(self):
        income_data = []
        for income in self.incomes:
            income_data.append(income.to_dict())

        spending_data = []
        for spending in self.spendings:
            spending_data.append(spending.to_dict())

        finance_data = {
            "incomes" : income_data,
            "spendings" : spending_data
        }
        
        with open("data/finance.json", "w") as file:
            json.dump(finance_data,file , indent=4)               




