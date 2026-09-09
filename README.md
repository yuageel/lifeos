# LifeOS

LifeOS is a personal productivity and finance tracking application built in Python.

I am building this project while learning software engineering and AI engineering.

## Version 0.1.0

The current version is a command-line application with JSON persistence.

## Architecture

LifeOS separates business logic from interfaces.

**Managers** (`TaskManager`, `FinanceManager`, `GoalManager`) own all data
and validation. They take parameters, raise `ValueError` on invalid input,
and persist to JSON. They never print or read input.

**Interfaces** (`main.py`, `assistant.py`) handle presentation. They collect
input, catch errors from the managers, and display results.


### Features

#### Tasks
- Add tasks
- Edit tasks
- Delete tasks
- Complete tasks
- Deadlines
- Priorities
- Overdue detection

#### Goals
- Add goals
- Track progress
- Complete goals
- Delete goals

#### Finance
- Add income
- Add spending
- Spending categories
- Current balance
- Transaction history
- Spending totals by category

## Technologies

- Python
- JSON
- Object-Oriented Programming
- Git
- AI-powered features

## Roadmap

Future versions will explore:

- Data analysis
- Machine learning
- SQL databases
- FastAPI
- Web frontend
