from app.node.node import Node
from app.core.config import settings

def validate_alive_nodes_number(nodes):
    available_nodes = [_node for _node in nodes if _node.is_alive()]
    return {
        "available_nodes": available_nodes,
        "n_nodes": len(available_nodes)
    }

def split_capacity(available_nodes, n_nodes, only_info = False):
    keys_for_node = settings.MAX_KEYS // n_nodes
    info = {}
    for i in range(n_nodes):
        _node: Node = available_nodes[i]

        _min = keys_for_node * i
        if i > 0:
            _min += 1

        _max = keys_for_node * (i+1)
        if i == n_nodes - 1:
            _max = settings.MAX_KEYS

        info[_node.host] = (_min, _max)
        if not only_info:
            _node.set_keys_range(_min, _max)
    if only_info:
        return info

