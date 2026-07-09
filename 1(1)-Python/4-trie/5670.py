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