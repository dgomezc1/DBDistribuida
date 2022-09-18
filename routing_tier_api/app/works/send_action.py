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

        if selected_node and selected_node.is_alive():
            return True, selected_node
        return False, None

    def run(self, key, method, value=None, *args, **kwargs):
        target = key_encryption(key)
        with lock:
            can_send, node = self._identify_node(target["n"])
            if can_send:
                request_data = {"url": f"{node.host}/db/{target['key']}"}
                if method in 'post':
                    request_data["url"] = f"{node.host}/db/"

                if method in ['post', 'put']:
                    request_data["json"] = {
                        "key": target['key'],
                        "value": value
                    }

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
