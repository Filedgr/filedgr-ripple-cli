from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet, generate_faucet_wallet
from filedgr_xrpl_cli.my_io.file_io import MyFileIO


class WalletLoader(ABC):

    @abstractmethod
    def load_wallet(self) -> RippleWallet:
        pass


class FileWalletLoader(WalletLoader):

    def load_wallet(self, path: str) -> RippleWallet:
        from orjson import orjson
        wallet_json = MyFileIO.read_from_file(path)
        wallet = RippleWallet(**orjson.loads(wallet_json))
        return wallet



class RippleWallet:

    def __init__(self, **kwargs) -> None:
        self.__wallet = Wallet(seed=kwargs.get("seed"), sequence=kwargs.get("sequence"))
        pass

    @classmethod
    def create_wallet(cls: Type[RippleWallet]) -> RippleWallet:
        wallet = Wallet.create()
        return RippleWallet(seed=wallet.seed,
                            sequence=wallet.sequence)

    @classmethod
    def create_testnet_wallet(cls: Type[RippleWallet], client: JsonRpcClient) -> RippleWallet:
        wallet = generate_faucet_wallet(client)
        return RippleWallet(seed=wallet.seed,
                            sequence=wallet.sequence)

    def get_wallet(self):
        return self.__wallet
