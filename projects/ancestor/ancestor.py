def earliest_ancestor(ancestors, starting_node):
    graph = {}
    
    for pair in ancestors:
        if pair[0] not in graph:
            graph[pair[0]] = set()

        if pair[1] in graph:
            graph[pair[1]].add(pair[0])
        else:
            graph[pair[1]] = {pair[0]}
    
    result = earliest_ancestor_helper(graph, starting_node, 0)[0]
    if result == starting_node:
        return -1
    else:
        return result

def earliest_ancestor_helper(ancestors_graph, current_node, current_distance):
    parents = ancestors_graph[current_node]
    if parents:
        true_result = ()
        for parent in parents:
            if true_result:
                current_result = earliest_ancestor_helper(ancestors_graph, parent, current_distance + 1)
                if current_result[1] > true_result[1]:
                    true_result = current_result
                elif current_result[1] == true_result[1]:
                    if current_result[0] < true_result[0]:
                        true_result = current_result
            else:
                true_result = earliest_ancestor_helper(ancestors_graph, parent, current_distance + 1)
        return true_result
    else:
        return current_node, current_distance