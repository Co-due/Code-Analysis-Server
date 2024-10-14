from app.visualize.analysis.stmt.models.user_func_stmt_obj import UserFuncStmtObj
from app.visualize.generator.models.user_func_viz import CallUserFuncViz, CreateCallStackViz, Argument
from app.visualize.generator.visualization_manager import VisualizationManager
from app.visualize.utils.utils import getStringType


class UserFuncConverter:

    @staticmethod
    def convert_to_call_user_func(user_func_stmt_obj: UserFuncStmtObj, viz_manager: VisualizationManager):

        return CallUserFuncViz(
            id=user_func_stmt_obj.id,
            assignName="",
            depth=viz_manager.get_depth(),
            signature=user_func_stmt_obj.func_signature[0],
            code=viz_manager.get_code_by_idx(user_func_stmt_obj.id),
        )

    @staticmethod
    def convert_to_create_call_stack(user_func_stmt_obj: UserFuncStmtObj, viz_manager: VisualizationManager):
        arguments = [
            Argument(str(arg_value), arg_name, getStringType(arg_value))
            for arg_name, arg_value in user_func_stmt_obj.args.items()
        ]

        return CreateCallStackViz(
            args=arguments,
            callStackName=user_func_stmt_obj.func_name,
            code=viz_manager.get_code_by_idx(user_func_stmt_obj.id),
        )

    @staticmethod
    def convert_to_end_user_func():
        return 0
