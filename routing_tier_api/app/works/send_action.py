import requests
from fastapi import HTTPException, status

from app.node import Node
from app.node.node import NodeStatus
from app.core.config import settings, lock
from .tasks.key_identifier import key_encryption

class SendDBAction:

    def _identify_node(self, n: int):
        selected_node: Node = None
        for node in settings.NODES:
            if node.min_key_value <= n <= node.max_key_value:
                selected_node = node
                break

        if selected_node:
            if selected_node.is_alive():
                return True, selected_node
            return True, selected_node, selected_node.replication_node
        return False, None

    def run(self, key, method, value=None, *args, **kwargs):
        target = key_encryption(key)
        with lock:
            identify_result = self._identify_node(target["n"])

            can_send = identify_result[0]
            node = identify_result[1]
            use_replication = len(identify_result) == 3
            if use_replication:
                node: Node = identify_result[2]


            if can_send:

                request_data = {
                    "url": f"{node.host}/db/{target['key']}",
                }

                if method != "get":
                    request_data["json"] = {
                        "replication_url": node.replication_node.host,
                        "is_restore": False,
                        "node_url": "",
                        "insert_type": 0
                    }

                if method in 'post':
                    request_data["url"] = f"{node.host}/db/"

                if method in ['post', 'put']:
                    request_data["json"]["key"] = target['key']
                    request_data["json"]["value"] = value


                if use_replication:
                    request_data["url"] = request_data["url"].replace("/db/", "/db/replication/")
                    if "json" in request_data:
                        request_data["json"]["insert_type"] = 1

                if not request_data["url"].endswith("/"):
                    request_data["url"] += "/"

                _method = getattr(requests, method)
                try:
                    response: requests.Response = _method(**request_data)

                    if 200 <= response.status_code < 300:
                        return response

                    raise HTTPException(
                        status_code=response.status_code,
                        detail=response.text
                    )
                except requests.exceptions.ConnectionError:
                    node.status = NodeStatus.DEAD

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The node in charge of making the request is not available, try again in a few seconds while the redistribution is done"
        )
