import ast

from app.visualize.analysis.element_manager import CodeElementManager
from app.visualize.analysis.stmt.expr.model.expr_obj import ExprObj
from app.visualize.analysis.stmt.parser.assign_stmt import AssignStmt
from app.visualize.analysis.stmt.parser.expr_stmt import ExprStmt
from app.visualize.analysis.stmt.parser.for_stmt import ForStmt


class StmtTraveler:

    @staticmethod
    def assign_travel(node: ast.Assign, elem_manager: CodeElementManager):
        return AssignStmt.parse(node.targets, node.value, elem_manager)

    @staticmethod
    def for_travel(node: ast.For, elem_manager: CodeElementManager):
        # parse condition
        condition_obj = ForStmt.parse(node.target, node.iter, elem_manager)
        # parse body
        body_odjs = StmtTraveler._for_body_travel(node, elem_manager, condition_obj)

        return {"condition": condition_obj, "body": body_odjs}

    @staticmethod
    def _for_body_travel(node: ast, elem_manager, condition_obj):
        body_odjs = []

        if isinstance(condition_obj, ExprObj):
            for i in range(condition_obj["start"], condition_obj["end"], condition_obj["step"]):
                for body in node.body:
                    StmtTraveler._internal_travel(node.body, elem_manager)
                    body_odjs.append(StmtTraveler._internal_travel(body, elem_manager))

        elif isinstance(condition_obj, "list"):
            raise NotImplementedError(f"[StmtTraveler] {type(condition_obj)}는 지원하지 않는 타입입니다.")
        else:
            raise TypeError(f"[StmtTraveler] {type(condition_obj)}는 잘못된 타입입니다.")

    @staticmethod
    def expr_travel(node: ast.Expr, elem_manager: CodeElementManager):
        return ExprStmt.parse(node.value, elem_manager)

    @staticmethod
    def _internal_travel(node: ast, elem_manager: CodeElementManager):
        if isinstance(node, ast.For):
            return StmtTraveler.for_travel(node, elem_manager)

        elif isinstance(node, ast.Expr):
            return StmtTraveler.expr_travel(node, elem_manager)

        else:
            raise TypeError(f"[StmtTraveler] {type(node)}는 잘못된 타입입니다.")
