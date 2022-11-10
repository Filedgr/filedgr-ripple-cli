from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet, generate_faucet_wallet
from filedgr_xrpl_cli.my_io.file_io import MyFileIO


class WalletLoader(ABC):

    @abstractmethod
    def load_wallet(self) -> XRPLWallet:
        pass


class FileWalletLoader(WalletLoader):

    def load_wallet(self, path: str) -> XRPLWallet:
        from orjson import orjson
        wallet_json = MyFileIO.read_from_file(path)
        wallet = XRPLWallet(**orjson.loads(wallet_json))
        return wallet


class XRPLWallet:

    def __init__(self, **kwargs) -> None:
        self.__wallet = Wallet(seed=kwargs.get("seed"), sequence=kwargs.get("sequence"))
        pass

    @classmethod
    def create_wallet(cls: Type[XRPLWallet]) -> XRPLWallet:
        wallet = Wallet.create()
        return XRPLWallet(seed=wallet.seed,
                          sequence=wallet.sequence)

    @classmethod
    def create_testnet_wallet(cls: Type[XRPLWallet], client: JsonRpcClient) -> XRPLWallet:
        wallet = generate_faucet_wallet(client)
        return XRPLWallet(seed=wallet.seed,
                          sequence=wallet.sequence)

    def get_wallet(self):
        return self.__wallet
