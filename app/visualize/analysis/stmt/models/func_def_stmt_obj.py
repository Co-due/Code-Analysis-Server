import ast
from dataclasses import dataclass, field

from app.visualize.analysis.stmt.models.expr_stmt_obj import ExprStmtObj
from app.visualize.analysis.stmt.models.stmt_type import StmtType


@dataclass(frozen=True)
class FuncDetails:
    args: tuple[str, ...]
    body: ast


@dataclass(frozen=True)
class FuncDefStmtObj:
    target: str
    expr_stmt_obj: ExprStmtObj
    type: StmtType = field(default_factory=lambda: StmtType.FUNC_DEF, init=False)
