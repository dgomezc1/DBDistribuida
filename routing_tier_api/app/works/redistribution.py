from time import sleep
from typing import List
from threading import Thread

import requests

from app.node.node import NodeStatus
from app.core.config import settings, lock
from .tasks.calculate_distribution import validate_alive_nodes_number, split_capacity


class Redistribution(Thread):

    def __init__(self):
        super().__init__(name="REDISTRIBUTION-THREAD")

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
                        print(f"Node {node.host} is down :(")
                        dead_nodes.append(node)
                    elif _actual == NodeStatus.DEAD and node.status == NodeStatus.ALIVE:
                        print(f"Node {node.host} is up again :)")
                        revived_nodes.append(node)
        return dead_nodes, revived_nodes


    def get_values(self, host, key):
        response = requests.get(f'{host}/db/{key}')
        if response.status_code == 200:
            return {
                "key": key,
                "value": response.json()["value"]
            }
        return None

    def redistribution(self, dead_nodes):
        global settings
        with lock:
            for node in dead_nodes:
                node.set_keys_range(-1, -1)

            alive_nodes = validate_alive_nodes_number(settings.NODES)
            # print("===================NUEVAS CAPACIDADES========================")
            new_capacities = split_capacity(only_info=True, **alive_nodes)
            # print(new_capacities)
            # print("===================LLAVES DE NODOS===========================")
            keys_of_nodes = {
                node.host: [
                    _key
                    for _key in node.get_all_keys()["keys"]
                    if not (new_capacities[node.host][0] <= int(_key, 16) <= new_capacities[node.host][1])
                ]
                for node in alive_nodes["available_nodes"]
            }
            # print(keys_of_nodes)
            # print("===================NUEVAS CAPACIDADES=========================")
            for node in alive_nodes["available_nodes"]:
                keys_of_nodes[node.host] = list(
                    filter(lambda x: x,
                        map(lambda key: self.get_values(node.host, key), keys_of_nodes[node.host])
                    )
                )

                for obj in keys_of_nodes[node.host]:
                    key = obj["key"]
                    requests.delete(f'{node.host}/db/{key}')
                # print(f"{node.host}: ({node.min_key_value}, {node.max_key_value}) -> ({new_capacities[node.host][0]}, {new_capacities[node.host][1]})")
                node.set_keys_range(new_capacities[node.host][0], new_capacities[node.host][1])
            # print("===================LLAVES DE NODOS (UPDATE)===================")
            # print(keys_of_nodes)

            for node in alive_nodes["available_nodes"]:
                for obj in keys_of_nodes[node.host]:
                    # print(f"Llave {obj['key']} enviada a {node.host}")
                    requests.post(f'{node.host}/db/', json=obj)

    def run(self):
        global settings
        while True:
            dead_nodes, revived_nodes = self.check_status()
            if dead_nodes or revived_nodes:
                self.redistribution(dead_nodes)
            sleep(10)
