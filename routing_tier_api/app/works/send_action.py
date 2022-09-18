import requests
from fastapi import HTTPException, status

from app.core.config import settings
from app.node import Node
from .tasks.key_identifier import key_encryption

class SendDBAction:

    def _identify_node(self, n: int):
        selected_node: Node = None
        for node in settings.NODES:
            print(node.host)
            print(node.min_key_value)
            print(n)
            print(node.max_key_value)
            if node.min_key_value <= n <= node.max_key_value:
                selected_node = node
                break

        if selected_node and selected_node.is_alive():
            return True, selected_node
        return False, None

    def run(self, key, method, value=None, *args, **kwargs):
        # TODO: Resolver race condition
        target = key_encryption(key)
        print(target)
        can_send, node = self._identify_node(target["n"])
        if can_send:
            print(node.host)
            request_data = {"url": f"{node.host}/db/{target['key']}"}
            if method in 'post':
                request_data["url"] = f"{node.host}/db/"

            if method in ['post', 'put']:
                request_data["json"] = {
                    "key": target['key'],
                    "value": value
                }

            _method = getattr(requests, method)
            response: requests.Response = _method(**request_data)
            if 200 <= response.status_code < 300:
                return response

            raise HTTPException(
                status_code=response.status_code,
                detail=response.text
            )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The node in charge of making the request is not available, try again in a few seconds while the redistribution is done"
        )
