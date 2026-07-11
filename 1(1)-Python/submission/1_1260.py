from __future__ import annotations
import copy
from collections import deque
from collections import defaultdict
from typing import DefaultDict, List


"""
TODO:
- __init__ 구현하기
- add_edge 구현하기
- dfs 구현하기 (재귀 또는 스택 방식 선택)
- bfs 구현하기
"""


class Graph:
    def __init__(self, n: int) -> None:
        """
        그래프 초기화
        n: 정점의 개수 (1번부터 n번까지)
        """
        self.n = n
        
        self.graph: DefaultDict[int, List[int]] = defaultdict(list)

    
    def add_edge(self, u: int, v: int) -> None:
        """
        양방향 간선 추가
        """
        
        self.graph[u].append(v)
        self.graph[v].append(u)
        
        # 정점 번호가 작은 것부터 방문하기 위해 정렬 수행
        self.graph[u].sort()
        self.graph[v].sort()
    
    def dfs(self, start: int) -> list[int]:
        """
        깊이 우선 탐색 (DFS)
        
        구현 방법 선택:
        1. 재귀 방식: 함수 내부에서 재귀 함수 정의하여 구현
        2. 스택 방식: 명시적 스택을 사용하여 반복문으로 구현
        """
        
        visited: list[int] = []  # 방문한 노드들을 순서대로 기록할 리스트
        
        def _dfs(node: int) -> None:
            # 이미 방문한 노드라면 탐색하지 않고 종료
            if node in visited:
                return
            
            # 현재 노드 방문 처리
            visited.append(node)
            
            # 현재 노드와 연결된 다른 노드들을 작은 번호부터 순서대로 깊게 방문
            for neighbor in self.graph[node]:
                _dfs(neighbor)
                
        _dfs(start)  # 시작 노드부터 탐색 시작
        return visited
        
    
    def bfs(self, start: int) -> list[int]:
        """
        너비 우선 탐색 (BFS)
        큐를 사용하여 구현
        """
        
        visited: list[int] = []  # 방문한 노드들을 순서대로 기록할 리스트
        queue: deque[int] = deque([start])  # 탐색 예정인 노드들을 담을 큐 (시작 노드 탑재)
        check_set = {start}  # 중복 방문 예방을 위한 집합(Set)
        
        while queue:
            # 큐의 맨 앞에서 노드를 하나 꺼냅니다.
            current = queue.popleft()
            visited.append(current)
            
            # 현재 노드와 인접한 노드들을 확인
            for neighbor in self.graph[current]:
                if neighbor not in check_set:
                    check_set.add(neighbor)
                    queue.append(neighbor)  
                    ''' 아직 방문하지 않은 이웃을 탐색 예정 큐에 추가'''
                    
        return visited
        
    
    def search_and_print(self, start: int) -> None:
        """
        DFS와 BFS 결과를 출력
        """
        dfs_result = self.dfs(start)
        bfs_result = self.bfs(start)
        
        print(' '.join(map(str, dfs_result)))
        print(' '.join(map(str, bfs_result)))



from typing import Callable
import sys


"""
-아무것도 수정하지 마세요!
"""


def main() -> None:
    intify: Callable[[str], list[int]] = lambda l: [*map(int, l.split())]

    lines: list[str] = sys.stdin.readlines()

    N, M, V = intify(lines[0])
    
    graph = Graph(N)  # 그래프 생성
    
    for i in range(1, M + 1): # 간선 정보 입력
        u, v = intify(lines[i])
        graph.add_edge(u, v)
    
    graph.search_and_print(V) # DFS와 BFS 수행 및 출력


if __name__ == "__main__":
    main()
