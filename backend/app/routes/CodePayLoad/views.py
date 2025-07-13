import ast
from http.client import HTTPException
import traceback
from app.utils.riskAnalyzer import RiskAnalyzer
from fastapi import APIRouter
from app.utils.grok import debug_code,debug_issues
from .schemas import CodePayLoadIn, CodePayLoadOut

router = APIRouter()

def getAst(code:str):
    try:
        parse_tree = ast.parse(code)
        return ast.dump(parse_tree, indent=4)
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Syntax error in code: {e}")

@router.post("/", response_model=CodePayLoadOut) 
async def receive_snippet(payload: CodePayLoadIn):
    try:
        analyzer = RiskAnalyzer(payload.code)
        risks = analyzer.flatten_risks()
        if risks == []:
            response = debug_code(payload.code,getAst(payload.code))
        else:
            response = debug_issues(risks)
        
        # In case response is a list, join it
        if isinstance(response, list):
            response = "\n".join(response)

        return {
            "code": payload.code,
            "length": len(payload.code),
            "message": response
        }

    except ValueError as ve:
        print("ValueError in /snippets/:", ve)
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        print("Error in /snippets/:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
