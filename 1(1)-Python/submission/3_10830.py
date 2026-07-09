from __future__ import annotations
import copy


"""
TODO:
- __setitem__ 구현하기
- __pow__ 구현하기 (__matmul__을 활용해봅시다)
- __repr__ 구현하기
"""


class Matrix:
    MOD = 1000

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    @staticmethod
    def full(n: int, shape: tuple[int, int]) -> Matrix:
        return Matrix([[n] * shape[1] for _ in range(shape[0])])

    @staticmethod
    def zeros(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(0, shape)

    @staticmethod
    def ones(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(1, shape)

    @staticmethod
    def eye(n: int) -> Matrix:
        matrix = Matrix.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1
        return matrix

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.matrix), len(self.matrix[0]))

    def clone(self) -> Matrix:
        return Matrix(copy.deepcopy(self.matrix))

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.matrix[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        self.matrix[key[0]][key[1]] = value

    def __matmul__(self, matrix: Matrix) -> Matrix:
        x, m = self.shape
        m1, y = matrix.shape
        assert m == m1

        result = self.zeros((x, y))

        for i in range(x):
            for j in range(y):
                for k in range(m):
                    result[i, j] += self[i, k] * matrix[k, j]

        return result

    def __pow__(self, n: int) -> Matrix:
        # 기저 조건 1: 모든 행렬의 0제곱은 단위행렬(Identity Matrix)입니다
        if n == 0:
            return Matrix.eye(self.shape[0])
        
        # 기저 조건 2: 지수가 1이면 자기 자신을 반환하되, 
        # 초기 원소가 MOD(1000) 이상일 수 있으므로 안전하게 나머지 연산을 처리한 복사본을 만듭니다.
        base = self.clone()
        for i in range(base.shape[0]):
            for j in range(base.shape[1]):
                base[i, j] %= self.MOD

        if n == 1:
            return base

        # 분할 정복 (Divide and Conquer): n을 절반으로 나눈 거듭제곱을 재귀적으로 호출
        half = base ** (n // 2)

        # n이 짝수인 경우: 행렬^(n//2) @ 행렬^(n//2)
        if n % 2 == 0:
            return half @ half
        # n이 홀수인 경우: (행렬^(n//2) @ 행렬^(n//2)) @ 행렬^1
        else:
            return (half @ half) @ base

    def __repr__(self) -> str:
        return "\n".join(" ".join(map(str, row)) for row in self.matrix)


from typing import Callable
import sys


"""
-아무것도 수정하지 마세요!
"""


def main() -> None:
    intify: Callable[[str], list[int]] = lambda l: [*map(int, l.split())]

    lines: list[str] = sys.stdin.readlines()

    N, B = intify(lines[0])
    matrix: list[list[int]] = [*map(intify, lines[1:])]

    Matrix.MOD = 1000
    modmat = Matrix(matrix)

    print(modmat ** B)


if __name__ == "__main__":
    main()