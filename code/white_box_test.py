import networkx as nx
import pytest
from main import query_bridge_words

# 测试用例 1: 无桥接词
def test_no_bridge_words():
    G = nx.DiGraph()
    result = query_bridge_words(G, "the", "and")
    assert result == []

# 测试用例 2: 有一个桥接词
def test_one_bridge_word():
    G = nx.DiGraph()
    G.add_edges_from([("the", "is"), ("is", "a"), ("a", "book")])
    result = query_bridge_words(G, "the", "a")
    assert result == ["is"]

# 测试用例 3: 有多个桥接词
def test_multiple_bridge_words():
    G = nx.DiGraph()
    G.add_edges_from([("the", "is"), ("is", "a"), ("the", "are"), ("are", "a")])
    result = query_bridge_words(G, "the", "a")
    assert set(result) == {"is", "are"}

# 测试用例 4: word1 是 word2 的前驱节点
def test_word1_predecessor_of_word2():
    G = nx.DiGraph()
    G.add_edges_from([("the", "is"), ("is", "a")])
    result = query_bridge_words(G, "the", "is")
    assert result == []

# 测试用例 5: word2 是 word1 的后继节点
def test_word2_successor_of_word1():
    G = nx.DiGraph()
    G.add_edges_from([("the", "is"), ("is", "a")])
    result = query_bridge_words(G, "is", "the")
    assert result == []

# 测试用例 6: word1 和 word2 相同
def test_word1_equals_word2():
    G = nx.DiGraph()
    G.add_edge("the", "the")
    result = query_bridge_words(G, "the", "the")
    assert result == ['the']

# 测试用例 7: word1 或 word2 不在图中
def test_word1_or_word2_not_in_graph():
    G = nx.DiGraph()
    G.add_edge("the", "is")
    result = query_bridge_words(G, "bogus", "the")
    assert result == []

# 运行测试
pytest.main()
