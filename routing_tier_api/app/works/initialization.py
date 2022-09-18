from app.node import Node
from app.core.config import settings

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
        return nodes
