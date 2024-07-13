from unittest.mock import patch

import pytest

from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.analysis.stmt.models.for_stmt_obj import BodyObj
from app.visualize.analysis.stmt.models.if_stmt_obj import (
    IfConditionObj,
    ElifConditionObj,
    ElseConditionObj,
    ConditionObj,
    IfStmtObj,
)
from app.visualize.analysis.stmt.parser.expr.models.expr_obj import PrintObj
from app.visualize.generator.converter.if_converter import IfConverter
from app.visualize.generator.highlight.expr_highlight import ExprHighlight
from app.visualize.generator.models.if_viz import ConditionViz, IfElseChangeViz
from app.visualize.generator.visualization_manager import VisualizationManager


@pytest.mark.parametrize(
    "conditions, expected",
    [
        (
            (
                IfConditionObj(
                    id=1,
                    expressions=(
                        "a > b",
                        "12 > 10",
                    ),
                    result=True,
                ),
                ElifConditionObj(
                    id=2,
                    expressions=(
                        "a < b",
                        "12 < 10",
                    ),
                    result=False,
                ),
                ElseConditionObj(
                    id=3,
                    expressions=None,
                    result=False,
                ),
            ),
            (
                ConditionViz(id=1, expr="a > b", type="if"),
                ConditionViz(id=2, expr="a < b", type="elif"),
                ConditionViz(id=3, expr="", type="else"),
            ),
        )
    ],
)
def test_convert_to_if_else_define_viz(conditions: tuple[ConditionObj, ...], expected):
    actual = IfConverter.convert_to_if_else_define_viz(conditions, VisualizationManager())
    assert actual.conditions == expected


@pytest.mark.parametrize(
    "conditions",
    [
        ((PrintObj(value="abc ", expressions=("abc",))),),
        (
            (
                IfStmtObj(
                    conditions=(IfConditionObj(id=1, expressions=("a > b", "10 > 20"), result=False),),
                    body=BodyObj(cur_value=0, body_steps=(AssignStmtObj(targets="a", expr_stmt_obj="10"),)),
                    type="if",
                )
            )
        ),
    ],
)
def test_convert_to_if_else_define_viz_fail(conditions: tuple[ConditionObj, ...]):
    with pytest.raises(TypeError):
        IfConverter.convert_to_if_else_define_viz(conditions, VisualizationManager())


@pytest.mark.parametrize(
    "condition, condition_type, expected",
    [
        pytest.param(
            IfConditionObj(
                id=1,
                expressions=(
                    "a > b",
                    "12 > 10",
                ),
                result=True,
            ),
            "if",
            ConditionViz(id=1, expr="a > b", type="if"),
            id="if문 Condition viz 생성",
        ),
        pytest.param(
            ElifConditionObj(
                id=1,
                expressions=(
                    "a < b",
                    "12 < 10",
                ),
                result=False,
            ),
            "elif",
            ConditionViz(id=1, expr="a < b", type="elif"),
            id="elif문 Condition viz 생성",
        ),
        pytest.param(
            ElseConditionObj(
                id=1,
                expressions=None,
                result=False,
            ),
            "else",
            ConditionViz(id=1, expr="", type="else"),
            id="else Condition viz 생성",
        ),
    ],
)
def test__create_condition_viz(condition: ConditionObj, condition_type, expected):
    assert IfConverter._create__if_else_define_viz(condition) == expected


@pytest.mark.parametrize(
    "conditions,expected",
    [
        pytest.param(
            (IfConditionObj(id=1, expressions=("a > b", "10 > 20"), result=False),),
            [
                IfElseChangeViz(id=1, depth=1, expr="a > b", highlights=[0, 1, 2, 3, 4]),
                IfElseChangeViz(id=1, depth=1, expr="10 > 20", highlights=[0, 1, 2, 3, 4, 5, 6]),
                IfElseChangeViz(id=1, depth=1, expr="False", highlights=[0, 1, 2, 3, 4]),
            ],
            id="if문 False인 경우",
        ),
        pytest.param(
            (IfConditionObj(id=1, expressions=("a < b", "10 < 20"), result=True),),
            [
                IfElseChangeViz(id=1, depth=1, expr="a < b", highlights=[0, 1, 2, 3, 4]),
                IfElseChangeViz(id=1, depth=1, expr="10 < 20", highlights=[0, 1, 2, 3, 4, 5, 6]),
                IfElseChangeViz(id=1, depth=1, expr="True", highlights=[0, 1, 2, 3, 4]),
            ],
            id="elif문 True 경우",
        ),
    ],
)
def test_convert_to_if_else_change_viz(
    conditions: tuple[ConditionObj, ...], expected, mock_viz_manager_with_custom_depth
):
    with (
        patch.object(
            IfConverter,
            "_create_condition_evaluation_steps",
        ) as mock_create_condition_evaluation_steps,
        patch.object(
            IfConverter,
            "_create_condition_result",
            return_value=[IfElseChangeViz(id=1, depth=1, expr="True", highlights=[0])],
        ) as mock_create_condition_result,
    ):
        mock_viz_manager = mock_viz_manager_with_custom_depth(1)
        actual = IfConverter.convert_to_if_else_change_viz(conditions, mock_viz_manager)

        mock_create_condition_evaluation_steps.assert_called_with(conditions[0], mock_viz_manager)
        mock_create_condition_result.assert_called_with(conditions[0], mock_viz_manager)


@pytest.mark.parametrize(
    "condition,highlights, expected",
    [
        pytest.param(
            IfConditionObj(id=1, expressions=("a > b", "10 > 20"), result=False),
            [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5, 6]],
            [
                IfElseChangeViz(id=1, depth=1, expr="a > b", highlights=[0, 1, 2, 3, 4]),
                IfElseChangeViz(id=1, depth=1, expr="10 > 20", highlights=[0, 1, 2, 3, 4, 5, 6]),
            ],
            id="a > 10 조건식 평가 과정 success",
        ),
        pytest.param(
            IfConditionObj(id=1, expressions=("True",), result=False),
            [[0, 1, 2, 3]],
            [
                IfElseChangeViz(id=1, depth=1, expr="True", highlights=[0, 1, 2, 3]),
            ],
            id="True 조건식 평가 과정 success",
        ),
    ],
)
def test__create_condition_evaluation_steps(condition, highlights, expected, mock_viz_manager_with_custom_depth):
    with patch.object(ExprHighlight, "get_highlight_indexes", side_effect=[highlights]):
        actual = IfConverter._create_condition_evaluation_steps(condition, mock_viz_manager_with_custom_depth(1))
        assert actual == expected


@pytest.mark.parametrize(
    "condition,expected",
    [
        pytest.param(
            IfConditionObj(id=1, expressions=("a > b", "10 > 20"), result=True),
            [
                IfElseChangeViz(id=1, depth=1, expr="True", highlights=[0, 1, 2, 3]),
            ],
            id="최종 결과가 True 인 경우",
        ),
        pytest.param(
            IfConditionObj(id=1, expressions=("a < b", "20 < 10"), result=False),
            [
                IfElseChangeViz(id=1, depth=1, expr="False", highlights=[0, 1, 2, 3, 4]),
            ],
            id="최종 결과가 False 인 경우",
        ),
    ],
)
def test__create_condition_result(condition, expected, mock_viz_manager_with_custom_depth):
    actual = IfConverter._create_condition_result(condition, mock_viz_manager_with_custom_depth(1))
    assert actual == expected
