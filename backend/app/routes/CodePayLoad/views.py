from http.client import HTTPException
from platform import node
import traceback
from fastapi import APIRouter
from app.utils.grok import debug_code
from .schemas import CodePayLoadIn,CodePayLoadOut
import ast

router = APIRouter()

# -------------- AST Analyzers --------------
# This module analyzes Python code for potential risks using the Abstract Syntax Tree (AST) module.
class RiskAnalyzer:
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)

    def find_division_risks(self):
        risky_lines = []
        # This method looks for division operations that could lead to runtime errors (e.g., division by zero).
        # It returns a list of tuples containing the line number and the code segment.
        # It uses ast.walk to traverse the AST and identify division operations.
        # If a division operation is found, it captures the line number and the source code segment
        # using ast.get_source_segment or ast.unparse.
        for node in ast.walk(self.tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                segment = ast.get_source_segment(self.code, node) or ast.unparse(node)
                risky_lines.append((node.lineno, segment))
        return risky_lines

    def find_eval_usage(self):
        risky_lines = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
                segment = ast.get_source_segment(self.code, node) or ast.unparse(node)
                risky_lines.append((node.lineno, segment))
        return risky_lines
    


@router.post("/", response_model=CodePayLoadOut) 
async def receive_snippet(payload: CodePayLoadIn):
    try:
        analyzer = RiskAnalyzer(payload.code)
        risks = analyzer.find_division_risks() + analyzer.find_eval_usage()
        if not risks:
            return {"code": payload.code, "length": len(payload.code), "message": "No obvious risks found via AST."}
        response = debug_code(risks)
        response = "\n".join(response) if isinstance(response, list) else response
    except ValueError as ve:
        print("🔥 ValueError in /snippets/:", ve)
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(ve))
        return {"code": payload.code, "length": len(payload.code), "message": f"Error analyzing code: {str(ve)}"}
    except Exception as e:
        print("🔥 Error in /snippets/:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
        return {"code": payload.code, "length": len(payload.code), "message": f"Error analyzing code: {str(e)}"}
    return {"code": payload.code, "length": len(payload.code), "message": response}



