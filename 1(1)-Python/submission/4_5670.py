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

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index = None 
        # 첫 글자는 항상 눌러야 하며, 중간 분기점이나 단어 종착지(is_end)가 있으면 버튼을 눌러야 합니다.
        if pointer == 0 or len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1

        new_index = None
        # 현재 노드의 자식들 중에서 글자가 일치하는 다음 노드의 인덱스를 찾습니다.
        for child_idx in trie[pointer].children:
            if trie[child_idx].body == element:
                new_index = child_idx
                break

    return cnt + int(len(trie[0].children) == 1)


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