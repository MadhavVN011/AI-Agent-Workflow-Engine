from app.engine import WorkflowEngine, State

# --- TOOL REGISTRY (Simple Version) --- [cite: 24]
def tool_count_lines(code: str) -> int:
    return len(code.split('\n'))

def tool_detect_print(code: str) -> bool:
    return "print(" in code

def tool_replace_print(code: str) -> str:
    # Simple mock fix: replace print with proper logging
    return code.replace("print(", "logger.info(")

# --- NODE DEFINITIONS (Option A Implementation) --- [cite: 46-50]

async def extract_metadata(state: State):
    code = state.get("code", "")
    state["line_count"] = tool_count_lines(code)
    state["functions_found"] = code.count("def ")
    # Initialize issues list if not present
    if "issues" not in state:
        state["issues"] = []

async def analyze_complexity(state: State):
    code = state.get("code", "")
    issues = []
    score = 100

    if tool_detect_print(code):
        issues.append("Uses 'print' instead of logger.")
        score -= 20

    if state["line_count"] > 50:
        issues.append("Code is too long (>50 lines).")
        score -= 10

    state["issues"] = issues
    state["quality_score"] = score

async def auto_fix(state: State):
    print(f"--- Fixing code (Current Score: {state['quality_score']}) ---")
    current_code = state["code"]
    
    if tool_detect_print(current_code):
        state["code"] = tool_replace_print(current_code)
        state["fixed_applied"] = True
    
    state["revisions"] = state.get("revisions", 0) + 1

# --- GRAPH CONSTRUCTION ---

def create_code_review_graph() -> WorkflowEngine:
    workflow = WorkflowEngine()

    workflow.add_node("extract", extract_metadata)
    workflow.add_node("analyze", analyze_complexity)
    workflow.add_node("fix", auto_fix)

    workflow.set_entry_point("extract")
    workflow.add_edge("extract", "analyze")

    def check_quality(state: State) -> str:
        score = state.get("quality_score", 0)
        revisions = state.get("revisions", 0)

        if score < 90 and revisions < 3:
            return "fix"
        return None 

    workflow.add_conditional_edge("analyze", check_quality)
    
    workflow.add_edge("fix", "analyze")

    return workflow

code_review_agent = create_code_review_graph()