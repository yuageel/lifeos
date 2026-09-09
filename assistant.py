import os
import requests
from datetime import date
from dotenv import load_dotenv



load_dotenv()

API_URL = "https://api.anthropic.com/v1/messages"

class Assistant:
    def __init__(self, finance_manager, task_manager):
        self.finance_manager = finance_manager
        self.task_manager = task_manager

    def build_tools(self):
        return [
            {
                "name": "add_spending",
                "description": "Record money the user spent.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number"},
                        "category": {"type": "string", "enum": self.finance_manager.categories},
                        "description": {"type": "string"},
                    },
                    "required": ["amount", "category", "description"],
                },
            },
                    {
                "name": "add_income",
                "description": "Record money the user received.",
                "input_schema": {
                    "type": "object",
                    "properties": {"amount": {"type": "number"}},
                    "required": ["amount"],
                },
            },
            {
                "name": "add_task",
                "description": "Add a task the user needs to do.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "deadline": {"type": "string", "description": "YYYY-MM-DD"},
                        "priority": {"type": "string", "enum": self.task_manager.priorities},
                    },
                    "required": ["title", "deadline", "priority"],
                },
            },
        ]

    def _system_prompt(self):
        return (
            f"You are a personal assistant for a tracker app. "
            f"Today's date is {date.today().isoformat()}. "
            f"Use the tools to record what the user tells you. "
            f"Be brief."
        )

    def _call_api(self, user_message):
        response = requests.post(
            API_URL,
            headers={
                "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-5",
                "max_tokens": 1000,
                "system": self._system_prompt(),
                "tools": self.build_tools(),
                "messages": [{"role": "user", "content": user_message}],
            },
        )
        data = response.json()

        if "content" not in data:
            print(f"API error: {data}")
            return {"content": []}

        return data


    def run_tool(self, name, args):
        try:
            if name == "add_spending":
                self.finance_manager.add_spending(
                    args["amount"], args["category"], args["description"]
                )
                return f"Added spending: {args['amount']} SAR, {args['category']}"

            if name == "add_income":
                self.finance_manager.add_income(args["amount"])
                return f"Added income: {args['amount']} SAR"

            if name == "add_task":
                self.task_manager.add_task(
                    args["title"], args["deadline"], args["priority"]
                )
                return f"Added task: {args['title']} (due {args['deadline']})"

            return f"unknown tool: {name}"

        except ValueError as error:
            return f"failed: {error}"


    def handle_message(self, user_message):
        data = self._call_api(user_message)

        for block in data["content"]:
            if block["type"] == "text":
                print(block["text"])
            elif block["type"] == "tool_use":
                print(self.run_tool(block["name"], block["input"]))
