from lib import Trie
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