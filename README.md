# 🤖 AI Agent Workflow Engine

> **A backend-only graph engine for building stateful AI agents.**
> *Submitted for the AI Engineering Internship Assignment.*

---

## 🚀 Overview

This project is a lightweight, **async-first workflow engine** built with **FastAPI**. It allows you to define workflows as graphs where nodes (Python functions) modify a shared state.

It was built to demonstrate:
* **Graph Logic:** Handling nodes, edges, and conditional branching.
* **State Management:** Passing context (state) between decoupled steps.
* **Cyclic Execution:** Supporting loops (e.g., "retry until fixed").
* **Clean API Design:** RESTful endpoints for creating and running workflows.

---

## 🛠️ Tech Stack

* **Language:** Python 3.12+
* **Framework:** FastAPI
* **Server:** Uvicorn
* **Architecture:** Modular Graph Engine (Nodes & Edges)

---

## 📂 Project Structure

```text
ai-agent-workflow-engine/
├── app/
│   ├── engine.py        # 🧠 Core Graph Engine (The Logic)
│   ├── workflow.py      # ⚙️ Code Review Agent (The Implementation)
│   ├── main.py          # 🔌 API Server (The Interface)
│   └── __init__.py
├── requirements.txt     # 📦 Dependencies
└── README.md            # 📄 Documentation

⚡ How to Run
1. Clone & Install

git clone [https://github.com/MadhavVN011/AI-Agent-Workflow-Engine.git](https://github.com/MadhavVN011/AI-Agent-Workflow-Engine.git)
cd AI-Agent-Workflow-Engine

# Create virtual environment (Recommended)
python -m venv venv
.\venv\Scripts\Activate  # Windows
# source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

2. Start the Server

python -m uvicorn app.main:app --reload
The API will be live at: http://127.0.0.1:8000

🧪 Testing the "Code Review Agent"
This project implements Option A: Code Review Mini-Agent. It takes bad code, detects issues, and automatically fixes them in a loop.

Step 1: Open Swagger UI: http://127.0.0.1:8000/docs

Step 2: Use the POST /graph/run endpoint.

Step 3: Paste this JSON payload:

{
  "initial_state": {
    "code": "def hello():\n    print('debugging')\n    return True"
  }
}

Step 4: Execute! You will see the agent loop through extract -> analyze -> fix -> analyze until the code is corrected (replacing print with logger).

