from xrpl.clients import JsonRpcClient


class XRPLConnection:

    def __init__(self,  json_rpc_url: str):
        self.__json_rpc_url = json_rpc_url
        try:
            self.__client = JsonRpcClient(self.__json_rpc_url)
        except Exception as ex:
            print(f"An exception occurred: {ex}")

    def get_client(self) -> JsonRpcClient:
        return self.__client
