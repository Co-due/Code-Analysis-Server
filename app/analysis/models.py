from dataclasses import dataclass


@dataclass(frozen=True)
class Variable:
    depth: int
    target: str
    expr: str
    type: str = "variable"


'''
    @ id: 식별값
    @ depth: 깊이
    @ name: 변수 이름
    @ value: 변수 값

'''


@dataclass
class Condition:
    target: str
    cur: int
    start: int
    end: int
    step: int

    def copy_with_new_cur(self, new_cur):
        return Condition(self.target, new_cur, self.start, self.end, self.step)

    def changed_attr(self):
        if self.start == self.cur:
            return list(self.__dict__.keys())

        return ['cur']


@dataclass(frozen=True)
class For:
    id: int
    depth: int
    condition: Condition
    highlight: []
    type: str = "for"


'''
    @ id: 식별값
    @ depth: 깊이
    @ condition: 조건절
    @ type : 타입
'''


@dataclass(frozen=True)
class Print:
    id: int
    depth: int
    expr: str
    type: str = "print"


'''
    @ id: 식별값
    @ depth: 깊이
    @ name: 변수 이름
    @ value: 변수 값

'''