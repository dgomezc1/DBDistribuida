from typing import List
from app.node import Node

def associate_nodes_to_replication(nodes: List[Node]):
    _range = list(range(len(nodes))) + [0]
    if len(_range) > 2:
        for mn, rn in zip(_range, _range[1:]):
            nodes[mn].replication_node = nodes[rn]
            nodes[rn].replicated_node = nodes[mn]
