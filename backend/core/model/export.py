# core/model/export.py
from core.model.workflow import Workflow

def export_to_python(workflow: Workflow, func_name="run_workflow"):
    code = [f"def {func_name}(inputs):"]
    code.append("    ctx = dict(inputs)")
    for node in workflow.nodes:
        if node.type == "AND":
            expr = f"ctx['{node.outputs[0]}'] = ctx['{node.inputs[0]}'] and ctx['{node.inputs[1]}']"
        elif node.type == "OR":
            expr = f"ctx['{node.outputs[0]}'] = ctx['{node.inputs[0]}'] or ctx['{node.inputs[1]}']"
        elif node.type == "NOT":
            expr = f"ctx['{node.outputs[0]}'] = not ctx['{node.inputs[0]}']"
        else:
            expr = f"# Unsupported node {node.type}"
        code.append(f"    {expr}")
    code.append("    return ctx")
    return "\n".join(code)
