from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
from app.workflow import code_review_agent

app = FastAPI(title="AI Agent Workflow Engine")

# --- In-Memory Storage ---
run_storage = {}

# --- Pydantic Models for Input ---
class GraphCreationRequest(BaseModel):
    nodes: list
    edges: list

class RunRequest(BaseModel):
    initial_state: Dict[str, Any]

# --- Endpoints ---

@app.post("/graph/create")
async def create_graph(payload: GraphCreationRequest):
    return {"message": "Graph created", "graph_id": "code-review-agent-v1"}

@app.post("/graph/run")
async def run_workflow(request: RunRequest):
    run_id = str(uuid.uuid4())
    
    # Initialize storage
    run_storage[run_id] = {"status": "running", "state": None}

    try:
        result = await code_review_agent.run(request.initial_state)
        
        # Save result
        run_storage[run_id] = {
            "status": "completed",
            "final_state": result["final_state"],
            "execution_log": result["execution_log"]
        }
        
        return {
            "run_id": run_id,
            "status": "completed",
            "result": result
        }

    except Exception as e:
        run_storage[run_id] = {"status": "failed", "error": str(e)}
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/graph/state/{run_id}")
async def get_run_state(run_id: str):
    """
    Fetch the state of a specific workflow run[cite: 37].
    """
    if run_id not in run_storage:
        raise HTTPException(status_code=404, detail="Run ID not found")
    
    return run_storage[run_id]

@app.get("/")
async def root():
    return {"message": "Agent Workflow Engine is Running. Use /docs to test."}