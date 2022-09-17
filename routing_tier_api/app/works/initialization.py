from app.node import Node
from app.core.config import NODES, settings

from .tasks.calculate_distribution import validate_alive_nodes_number, split_capacity


class Initialization:

    def __init__(self):
        pass

    def _nodes_registry(self):
        return [
            Node(node_host)
            for node_host in settings.NODE_HOSTS
        ]

    def run(self):
        NODES = self._nodes_registry()
        valid_nodes = validate_alive_nodes_number(NODES)
        split_capacity(**valid_nodes)
