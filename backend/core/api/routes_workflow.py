# backend/core/api/routes_workflow.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

from core.model.workflow import Workflow
from core.runtime.executor import WorkflowExecutor

router = APIRouter(tags=["workflow"])

class WorkflowRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    connections: List[Dict[str, str]]
    inputs: Dict[str, Any] = {}

@router.post("/run")
async def run_workflow(req: WorkflowRequest):
    workflow = Workflow.from_dict(req.dict())
    executor = WorkflowExecutor(workflow)
    result = executor.run(req.inputs)
    return result
