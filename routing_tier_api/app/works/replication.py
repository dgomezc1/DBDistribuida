import logging
from time import sleep
from typing import List
from threading import Thread
from datetime import datetime

import requests

from app.node.node import Node, NodeStatus
from app.core.config import settings, lock, ROOT_DIR
from .tasks.calculate_distribution import validate_alive_nodes_number, split_capacity

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    filename=str(ROOT_DIR.joinpath(f"code/logs/{datetime.now().strftime('%Y%m%d%H%M%S')}.log").resolve())
)


class Replication(Thread):

    def __init__(self):
        super().__init__(name="REPLICATION-THREAD")

    def check_status(self):
        global settings
        dead_nodes = []
        revived_nodes = []
        with lock:
            for node in settings.NODES:
                _actual = node.status
                node.check_status()
                if _actual != node.status:
                    if node.status == NodeStatus.DEAD:
                        logging.error(f"Node {node.host} is down")
                        dead_nodes.append(node)
                    elif _actual == NodeStatus.DEAD and node.status == NodeStatus.ALIVE:
                        logging.info(f"Node {node.host} is up again")
                        revived_nodes.append(node)
        return dead_nodes, revived_nodes

    def restore(self, revived_nodes: List[Node]):
        global settings
        with lock:
            for node in revived_nodes:
                response = requests.post(
                    f"{node.replication_node.host}/db/replication/restore/",
                    json={
                        "replication_url": "",
                        "is_restore": True,
                        "node_url": node.host,
                        "insert_type": 0
                    }
                )
                if response.status_code != 200:
                    logging.error(f"Node {node.replication_node.host} cannot restore data into {node.host} ")

    def run(self):
        global settings
        while True:
            _, revived_nodes = self.check_status()
            if revived_nodes:
                self.restore(revived_nodes)
            sleep(10)
