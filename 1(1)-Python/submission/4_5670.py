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
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""


def count(trie: Trie, query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for i, element in enumerate(query_seq):
        # 1. 다음 노드의 인덱스 찾기
        new_index = None
        for child_idx in trie[pointer].children:
            if trie[child_idx].body == element:
                new_index = child_idx
                break
        
        # 주어지는 모든 단어는 Trie에 존재하므로 new_index는 항상 존재함
        assert new_index is not None

        # 2. 버튼 입력 여부 판정 (분기점 또는 단어 종착지 확인)
        if i == 0:
            # 첫 글자는 상근이의 규칙 규칙 1에 의해 무조건 입력 버튼을 눌러야 함
            cnt += 1
        else:
            # 중간 글자의 경우, '이전 노드'의 분기 조건에 따라 결정됨
            # 자식이 여러 개이거나, 이전 노드가 다른 단어의 끝(is_end)인 경우 자동 입력 불가
            if len(trie[pointer].children) > 1 or trie[pointer].is_end:
                cnt += 1

        # 3. 포인터를 다음 노드로 이동 (트리 하강 - 필수 누락 수정)
        pointer = new_index

    return cnt


def main() -> None:
    # 표준 입력으로부터 모든 데이터를 한 번에 읽어옵니다.
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return

    idx = 0
    while idx < len(input_data):
        # 단어의 개수 N을 파싱합니다.
        N = int(input_data[idx])
        words = input_data[idx + 1 : idx + 1 + N]
        idx += 1 + N

        # 새로운 Trie 인스턴스를 생성하고 단어들을 주입합니다.
        trie: Trie[str] = Trie()
        for word in words:
            trie.push(word)

        # 각 단어별 버튼 입력 횟수의 총합을 구합니다.
        total_presses = 0
        for word in words:
            total_presses += count(trie, word)

        # 평균 입력 횟수를 계산하여 소수점 둘째 자리까지 반올림하여 출력합니다.
        print(f"{total_presses / N:.2f}")


if __name__ == "__main__":
    main()