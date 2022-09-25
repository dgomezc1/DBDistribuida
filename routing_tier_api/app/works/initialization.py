from app.node import Node
from app.core.config import settings

from .tasks.create_replications import associate_nodes_to_replication
from .tasks.calculate_distribution import validate_alive_nodes_number, split_capacity


class Initialization:

    def __init__(self):
        pass

    def _nodes_registry(self):
        return [
            Node(node_host)
            for node_host in settings.LIST_OF_NODE_HOSTS
        ]

    def run(self):
        nodes = self._nodes_registry()
        valid_nodes = validate_alive_nodes_number(nodes)
        split_capacity(**valid_nodes)
        associate_nodes_to_replication(valid_nodes["available_nodes"])
        for node in valid_nodes["available_nodes"]:
            print(f"{node.host} -> {node.replication_node_url}")
        return nodes
