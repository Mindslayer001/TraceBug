from platform import node
from fastapi import APIRouter
from .schemas import CodePayLoadIn,CodePayLoadOut
import ast

router = APIRouter()

@router.post("/", response_model=CodePayLoadOut) 
async def receive_snippet(payload: CodePayLoadIn):
    getAst(payload.code)
    return {"code": payload.code, "length": len(payload.code)}


def getAst(code: str):
    node = ast.parse(code)
    print("AST of the dumped code:")
    print(ast.dump(node, indent=4))
    return ast.dump(node)


