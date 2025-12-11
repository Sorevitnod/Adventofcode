from collections import defaultdict

def read_graph():
    adj = defaultdict(list)
    with open('11_day.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            left, right = line.split(":", 1)
            node = left.strip()
            neighbors = right.strip().split()
            # Ensure node exists
            _ = adj[node]
            # Add neighbors
            for n in neighbors:
                adj[node].append(n)
                # Ensure neighbor key exists
                _ = adj[n]
    return adj

def topo_sort_from(start, adj):
    visited = set()
    order = []

    def dfs(u):
        visited.add(u)
        for v in adj[u]:
            if v not in visited:
                dfs(v)
        order.append(u)

    dfs(start)
    order.reverse()
    return order, visited

def count_paths_with_dac_fft(adj):
    if "svr" not in adj:
        raise ValueError("Graph does not contain 'svr' node.")
    if "out" not in adj:
        _ = adj["out"]

    topo, reachable = topo_sort_from("svr", adj)

    # dp[node][state] where state encodes which special nodes have been visited:
    #   0 = none visited
    #   1 = visited dac
    #   2 = visited fft
    #   3 = visited both dac and fft
    dp = {u: [0, 0, 0, 0] for u in reachable}
    dp["svr"][0] = 1  # Start at svr with no special nodes visited

    for u in topo:
        counts = dp[u]
        if sum(counts) == 0:
            continue
        for v in adj[u]:
            if v not in reachable:
                continue
            for state, cnt in enumerate(counts):
                if cnt == 0:
                    continue
                new_state = state
                if v == "dac":
                    new_state |= 1
                if v == "fft":
                    new_state |= 2
                dp[v][new_state] += cnt

    # Number of paths that end at 'out' having visited both dac and fft:
    return dp["out"][3]

adj = read_graph()
result = count_paths_with_dac_fft(adj)
print(result)