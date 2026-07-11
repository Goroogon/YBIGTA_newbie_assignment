from lib import Trie
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