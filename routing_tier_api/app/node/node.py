from enum import Enum

import requests

from .status import health_check

class NodeStatus(Enum):
    ALIVE = 'alive'
    DEAD = 'dead'


class UnavailableNodeException(Exception):
    pass

class Node:

    def __init__(self, host):
        self.host = host
        self.failure_ping = 0
        self.status = None
        self.min_key_value = None
        self.max_key_value = None
        self.replication_node: Node = None
        self.replicated_node: Node = None
        if health_check(host):
            self.status = NodeStatus.ALIVE

    def set_keys_range(self, min_value, max_value):
        self.min_key_value = min_value
        self.max_key_value = max_value

    def check_status(self):
        if not health_check(self.host):
            self.failure_ping += 1
        else:
            self.failure_ping = 0
            self.status = NodeStatus.ALIVE

        if self.failure_ping >= 3:
            self.status = NodeStatus.DEAD

    def get_all_keys(self):
        if self.status != NodeStatus.ALIVE:
            raise UnavailableNodeException()

        try:
            response = requests.get(f"{self.host}/db/")
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.ConnectionError:
            if self.status != NodeStatus.DEAD:
                print(f"Node {self.host}: Error getting all keys")

        raise UnavailableNodeException()

    def is_alive(self):
        self.check_status()
        if self.status == NodeStatus.ALIVE:
            return True
        return False
