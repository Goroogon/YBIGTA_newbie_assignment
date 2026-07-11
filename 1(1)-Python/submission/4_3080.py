from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        # 현재 탐색 중인 노드의 인덱스 포인터 (항상 루트인 0부터 시작)
        current_idx: int = 0  

        for element in seq:
            # 일치하는 자식 인덱스를 찾기 위한 임시 변수 (찾지 못하면 None 상태 유지)
            found_idx: Optional[int] = None
            
            # 현재 노드가 가진 자식 인덱스 배열(children)을 순회하며 선형 탐색 수행
            child_idx: int
            for child_idx in self[current_idx].children:
                if self[child_idx].body == element:
                    found_idx = child_idx
                    break
            
            # 일치하는 자식 노드가 없는 경우, 새로운 노드를 생성하여 리스트 끝에 추가
            if found_idx is None:
                new_node: TrieNode[T] = TrieNode(body=element)
                self.append(new_node)
                
                # 새 노드가 부여받은 가장 마지막 인덱스 번호를 획득
                found_idx = len(self) - 1  
                # 부모 노드의 자식 배열에 새로운 인덱스 주입 (링크 바인딩)
                self[current_idx].children.append(found_idx)
            
            # 포인터를 하위 자식 노드의 인덱스로 갱신하여 트리 아래로 하강
            current_idx = found_idx
            
        # 모든 시퀀스 탐색 및 삽입이 완료되면, 해당 종착지 노드의 단어 종단 플래그를 True로 활성화
        self[current_idx].is_end = True


import sys


"""
TODO:
- 일단 lib.py의 Trie Class부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""


def main() -> None:
    # 1. 빠른 입력을 통해 단어 리스트 받기
    input_data = sys.stdin.read().splitlines()
    N = int(input_data[0])
    names = input_data[1:N+1]

    # 2. Trie에 모든 이름을 정수(ASCII) 리스트 형태로 주입
    trie: Trie[int] = Trie()
    for name in names:
        trie.push([ord(char) for char in name])

    # 3. 팩토리얼 값 사전 연산 (최대 자식 수 27개에 대해 처리)
    MOD = 1_000_000_007
    fact = [1] * 28
    for i in range(1, 28):
        fact[i] = (fact[i - 1] * i) % MOD

    # 4. 반복문 스택을 이용한 트라이 트리 전수 탐색 (DFS)
    ans = 1
    stack = [0]  # 루트 노드(인덱스 0)부터 시작

    while stack:
        curr_idx = stack.pop()
        
        # 현재 노드의 순수 자식 노드 개수
        children_count = len(trie[curr_idx].children)
        
        # 중간에 끝나는 단어가 있다면 분기 선택지에 1개 추가 (공백 단어 배치용)
        if trie[curr_idx].is_end:
            children_count += 1
            
        # 분기 경우의 수(팩토리얼)를 정답에 곱해줌
        if children_count > 0:
            ans = (ans * fact[children_count]) % MOD
            
        # 다음 자식 노드들을 스택에 쌓아서 탐색 이어가기
        for child_idx in trie[curr_idx].children:
            stack.append(child_idx)

    print(ans)


if __name__ == "__main__":
    main()