import networkx as nx
import pytest
from main import find_shortest_path

# 测试用例 1: 起始单词和目标单词都在图中
def test_case_1():
    G1 = nx.DiGraph()
    G1.add_edge("a", "b")
    G1.add_edge("b", "c")
    result = find_shortest_path(G1, "a", "c")
    expected = (["a", "b", "c"], [("a", "b"), ("b", "c")], 2)
    assert result == expected

# 测试用例 2: 起始单词和目标单词存在至少1条路径
def test_case_2():
    G2 = nx.DiGraph()
    G2.add_edge("a", "b")
    G2.add_edge("b", "c")
    G2.add_edge("c", "a")
    result = find_shortest_path(G2, "a", "c")
    expected = (["a", "b", "c"], [("a", "b"), ("b", "c")], 2)
    assert result == expected

# 测试用例 3: 起始单词或目标单词不在图中
def test_case_3():
    G3 = nx.DiGraph()
    G3.add_edge("a", "b")
    G3.add_edge("c", "d")
    result = find_shortest_path(G3, "x", "a")
    expected = "No word1 or word2 in the graph!"
    assert result == expected

# 测试用例 4: 起始单词和目标单词都在图中，但不存在路径
def test_case_4():
    G4 = nx.DiGraph()
    G4.add_edge("a", "b")
    G4.add_edge("c", "d")
    result = find_shortest_path(G4, "a", "d")
    expected = (None, None, None)
    assert result == expected

# 运行测试
pytest.main()
