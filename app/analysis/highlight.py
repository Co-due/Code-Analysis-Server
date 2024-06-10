from app.analysis.models import Condition


def for_highlight(condition: Condition):
    return condition.changed_attr()


def expr_highlights(parsed_exprs):
    highlights = []
    pre_expr = parsed_exprs[0]

    for cur_expr in parsed_exprs[:-1]:
        highlights.append(expr_highlight(pre_expr, cur_expr))
        pre_expr = cur_expr

    # 마지막 요소는 전체 인덱스 반환
    highlights.append(list(range(len(parsed_exprs[-1]))))

    return highlights


# 변경된 요소에 대한 인덱스 추출
def expr_highlight(pre_expr: list, cur_expr: list):
    highlight = []
    pre_idx = 0
    cur_idx = 0

    while cur_idx < len(cur_expr) or pre_idx < len(pre_expr):
        # 현재 인덱스가 범위를 넘지 않도록 조정
        if pre_idx+1 < len(pre_expr) and cur_idx < len(cur_expr) and pre_expr[pre_idx] != cur_expr[cur_idx]:
            pre_idx = pre_idx+1
            while cur_idx < len(cur_expr) and pre_expr[pre_idx] != cur_expr[cur_idx]:
                # 바뀐 부분의 인덱스 추가
                highlight.append(cur_idx)
                cur_idx += 1
        else:
            if pre_idx < len(pre_expr):
                pre_idx += 1
            if cur_idx < len(cur_expr):
                cur_idx += 1

    return highlight


def create_highlighted_expression(expr, highlight_indices):
    highlighted_expr = ""
    for idx, char in enumerate(expr):
        if idx in highlight_indices:
            highlighted_expr += f"{char}"

    return highlighted_expr