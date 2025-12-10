import asyncio
import inspect
from typing import Dict, Any, Callable, Optional, List

# Type definitions for clarity
State = Dict[str, Any]
NodeFunction = Callable[[State], Any]  

class WorkflowEngine:
    def __init__(self):
        self.nodes: Dict[str, NodeFunction] = {}
        self.edges: Dict[str, str] = {}  
        self.conditional_edges: Dict[str, Callable[[State], str]] = {} 
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: NodeFunction):
        self.nodes[name] = func

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, from_node: str, to_node: str):
        self.edges[from_node] = to_node

    def add_conditional_edge(self, from_node: str, condition_fn: Callable[[State], str]):
        self.conditional_edges[from_node] = condition_fn

    async def run(self, initial_state: State) -> Dict[str, Any]:
        if not self.entry_point:
            raise ValueError("Entry point not defined.")

        current_node_name = self.entry_point
        state = initial_state.copy()
        execution_log = []

        # Safety limit to prevent infinite loops during testing
        steps_count = 0
        MAX_STEPS = 20 

        while current_node_name:
            if steps_count >= MAX_STEPS:
                execution_log.append("MAX_STEPS_REACHED")
                break
            
            steps_count += 1
            execution_log.append(current_node_name)
            
            # Get the function for the current node
            node_func = self.nodes.get(current_node_name)
            if not node_func:
                raise ValueError(f"Node '{current_node_name}' not found.")

            # Execute Node (Handle both async and sync functions)
            if inspect.iscoroutinefunction(node_func):
                await node_func(state)
            else:
                node_func(state)

            # Determine next node
            # 1. Check conditional edges first (priority)
            if current_node_name in self.conditional_edges:
                condition_fn = self.conditional_edges[current_node_name]
                next_node = condition_fn(state)
                current_node_name = next_node
            
            # 2. Check static edges
            elif current_node_name in self.edges:
                current_node_name = self.edges[current_node_name]
            
            # 3. No edge? End of workflow.
            else:
                current_node_name = None

        return {
            "final_state": state,
            "execution_log": execution_log
        }