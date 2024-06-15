import networkx as nx
import matplotlib.pyplot as plt
import re
from collections import defaultdict
import random
import numpy as np


def read_text(file_path):
    # 打开文件，读取内容，进行预处理
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # 预处理：去除标点
    text = re.sub(r'[^\w\s]', '', text)

    # 转换为小写
    text = text.lower()

    # 忽略非字母字符
    text = re.sub(r'[^[a-zA-Z]]+', '', text)

    # 去除多余的空白字符
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def generate_graph(text):
    # 分词，建立节点和边的关系
    G = nx.DiGraph()

    # 创建一个字典来存储边的权重
    edge_weights = defaultdict(int)

    # 使用空格分割单词
    words = text.split(' ')

    # 遍历单词列表，计算相邻词对的权重
    for i in range(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]
        # 更新边权重
        edge_weights[(word1, word2)] += 1

        # 如果还没有这条边，添加到图中
        if not G.has_edge(word1, word2):
            G.add_edge(word1, word2)

    # 使用edge_weights字典来设置边的权重
    nx.set_edge_attributes(G, edge_weights, 'weight')

    return G


def show_graph(G):
    # 使用spectral_layout布局算法
    pos = nx.spectral_layout(G)
    # 定义距离阈值
    threshold = 0.5  # 调整这个值来控制节点之间的最小距离

    # 定义扰动幅度
    perturbation_scale = 0.5  # 调整这个值来控制扰动幅度

    # 检查节点之间的距离，并给它们添加扰动
    moved = True
    while moved:
        moved = False
        for i in pos:
            for j in pos:
                if i != j:
                    # 计算两点之间的距离
                    distance = np.linalg.norm(np.array(pos[i]) - np.array(pos[j]))
                    if distance < threshold:
                        # 如果距离小于阈值，给节点 j 添加扰动
                        pos[j] += np.random.normal(0, perturbation_scale, size=len(pos[i]))
                        moved = True
    # 绘制有向图
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='black', node_size=1500, linewidths=2, font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


def query_bridge_words(G, word1, word2):

    bridge_words = []

    # 遍历所有节点，检查是否存在桥接词
    for node in G.nodes():
        if word1 in G.predecessors(node) and word2 in G.successors(node):
            bridge_words.append(node)

    return bridge_words


# 生成新文本
def generateNewText(inputText, G):
    # 预处理输入文本
    words = inputText.split()
    processed_words = [word.strip(".,!?()[]{}:;\"'<>") for word in words]

    # 遍历单词列表，查询桥接词
    new_words = []
    for i in range(len(processed_words) - 1):
        word1 = processed_words[i]
        word2 = processed_words[i + 1]

        # 查询桥接词
        bridge_words = query_bridge_words(G, word1, word2)

        # 插入桥接词
        if bridge_words:
            new_words.append(word1)
            new_words.extend(bridge_words)
        else:
            new_words.append(word1)

    # 添加最后一个单词
    new_words.append(processed_words[-1])

    # 生成新文本
    new_text = ' '.join(new_words)
    return new_text


# 计算最短路径
def find_shortest_path(G, word1, word2):
    if word1 not in G or word2 not in G:
        return ("No word1 or word2 in the graph!")
    try:
        # 计算最短路径
        shortest_path = nx.shortest_path(G, source=word1, target=word2)
        # 计算路径长度
        path_length = nx.shortest_path_length(G, source=word1, target=word2)
        # 将节点路径转换为边路径
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        return shortest_path, path_edges, path_length
    except nx.NetworkXNoPath:
        # 如果没有路径返回None
        return None, None, None


# 展示最短路径
def draw_graph_with_highlighted_path(G, shortest_path, path_edges, path_length):
    # 使用spectral_layout布局算法
    pos = nx.spectral_layout(G)
    # 定义距离阈值
    threshold = 0.5  # 调整这个值来控制节点之间的最小距离

    # 定义扰动幅度
    perturbation_scale = 0.5  # 调整这个值来控制扰动幅度

    # 检查节点之间的距离，并给它们添加扰动
    moved = True
    while moved:
        moved = False
        for i in pos:
            for j in pos:
                if i != j:
                    # 计算两点之间的距离
                    distance = np.linalg.norm(np.array(pos[i]) - np.array(pos[j]))
                    if distance < threshold:
                        # 如果距离小于阈值，给节点 j 添加扰动
                        pos[j] += np.random.normal(0, perturbation_scale, size=len(pos[i]))
                        moved = True
    # 绘制有向图
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='black', node_size=1500, linewidths=2, font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # 绘制最短路径
    edge_colors = ['red' if (u, v) in path_edges else 'black' for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2)

    # 标记最短路径的节点
    node_colors = ['red' if node in shortest_path else 'skyblue' for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1500)

    # 标注路径长度
    plt.text(0.5, 0.95, f"Shortest Path Length: {path_length}", horizontalalignment='center', verticalalignment='center', transform=plt.gcf().transFigure)

    plt.show()


# 随机游走
def random_walk(G):
    # 随机选择一个起始节点
    current_node = random.choice(list(G.nodes()))
    walk = [current_node]
    visited_edges = set()

    while True:
        # 获取当前节点的所有出边
        neighbors = list(G.neighbors(current_node))
        if not neighbors:
            break
        # 随机选择一个未访问的出边
        next_node = random.choice(neighbors)
        edge = (current_node, next_node)
        if edge in visited_edges:
            visited_edges.add(edge)
            walk.append(next_node)
            break
        visited_edges.add(edge)
        walk.append(next_node)
        current_node = next_node

    return walk


# 主函数
def main():
    # 接收用户输入
    file_path = input("请输入文本文件路径: ")

    # 读取文本文件
    text = read_text(file_path)

    # 生成有向图
    G = generate_graph(text)

    # 展示有向图
    show_graph(G)

    # 用户选择后续功能
    while True:
        choice = input("请选择功能(1: 查询桥接词, 2: 生成新文本, 3: 计算最短路径, 4: 随机游走, q: 退出）: ")
        if choice == '1':
            word1 = input("请输入第一个单词: ")
            word2 = input("请输入第二个单词: ")
            # 检查单词是否在图中
            if word1 not in G or word2 not in G:
                if word1 not in G and word2 in G:
                    print("No '{}' in the graph!".format(word1))
                elif word1 in G and word2 not in G:
                    print("No '{}' in the graph!".format(word2))
                else:
                    print("No '{}' and '{}' in the graph!".format(word1, word2))
            else:
                bridge_words = query_bridge_words(G, word1, word2)
                if not bridge_words:
                    print("No bridge words from '{}' to '{}'!".format(word1, word2))
                else:
                    print("The bridge words from '{}' to '{}' is: {}".format(word1, word2, ", ".join(bridge_words)))
        elif choice == '2':
            input_text = input("请输入原始文本: ")
            new_text = generateNewText(input_text, G)
            print("新文本:", new_text)
        elif choice == '3':
            word1 = input("请输入起始单词: ")
            word2 = input("请输入目标单词: ")
            # 检查单词是否在图中
            if word1 not in G or word2 not in G:
                if word1 not in G and word2 in G:
                    print("No '{}' in the graph!".format(word1))
                elif word1 in G and word2 not in G:
                    print("No '{}' in the graph!".format(word2))
                else:
                    print("No '{}' and '{}' in the graph!".format(word1, word2))
            else:
                shortest_path, path_edges, length = find_shortest_path(G, word1, word2)
                if path_edges:
                    print("The shortest path is: " + " -> ".join(shortest_path))
                    print("The path length is: " + str(length))
                    draw_graph_with_highlighted_path(G, shortest_path, path_edges, length)
                else:
                    print("No path found between " + 'word1' + " and " + 'word2')
        elif choice == '4':
            visited_nodes = random_walk(G)
            print("Random walk nodes: " + " -> ".join(visited_nodes))
            with open("random_walk_output.txt", 'w') as f:
                f.write(" -> ".join(visited_nodes))
        elif choice.lower() == 'q':
            break
        else:
            print("无效选择，请重新输入。")


if __name__ == "__main__":
    main()
