from enum import Enum
from pydantic import BaseModel


class Network(BaseModel):
    json_rpc_url: str
    ws_url: str


class NetworkChoices(Enum):
    mainnet = "mainnet"
    ripple1 = "ripple1"
    ripple2 = "ripple2"
    testnet = "testnet"
    devnet = "devnet"
    nft_devnet = "nft-devnet"


all_networks = {
    "mainnet": Network(
        json_rpc_url="https://xrplcluster.com/",
        ws_url="wss://xrpl.ws/"
    ),
    "ripple1": Network(
        json_rpc_url="https://s1.ripple.com:51234/",
        ws_url="wss://s1.ripple.com/"
    ),
    "ripple2": Network(
        json_rpc_url="https://s2.ripple.com:51234/",
        ws_url="wss://s2.ripple.com/"
    ),
    "testnet": Network(
        json_rpc_url="https://s.altnet.rippletest.net:51234/",
        ws_url="wss://s.altnet.rippletest.net/"
    ),
    "devnet": Network(
        json_rpc_url="https://s.devnet.rippletest.net:51234/",
        ws_url="wss://s.devnet.rippletest.net/"
    ),
    "nft-devnet": Network(
        json_rpc_url="http://xls20-sandbox.rippletest.net:51234",
        ws_url="wss://xls20-sandbox.rippletest.net:51233"
    )
}
