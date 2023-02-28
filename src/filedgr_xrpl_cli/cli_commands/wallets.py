import uuid

import typer
from orjson import orjson
from rich import print

from filedgr_xrpl_cli.dto.network import all_networks, NetworkChoices
from filedgr_xrpl_cli.my_io.file_io import MyFileIO
from filedgr_xrpl_cli.my_xrpl.connection import XRPLConnection
from filedgr_xrpl_cli.my_xrpl.tx import TransactionBuilder
from filedgr_xrpl_cli.my_xrpl.wallet import XRPLWallet, FileWalletLoader
from filedgr_xrpl_cli.settings import default_path

wallet_app = typer.Typer()


@wallet_app.command()
def create(name: str,
           dump: bool = True,
           path: str = default_path,
           network: NetworkChoices = "testnet") -> str:
    conn = XRPLConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)
    if network == NetworkChoices.testnet:
        wallet = XRPLWallet.create_testnet_wallet(conn.get_client())
    else:
        wallet = XRPLWallet.create_wallet()

    wallet_json = orjson.dumps(wallet.get_wallet().__dict__).decode("utf8")
    if dump:
        MyFileIO.write_to_file(path=f"{path}/wallets/{name}", content=wallet_json)
    print(f"Created wallet: {wallet_json}")


@wallet_app.command()
def set_domain(
        name: str,
        domain: str = typer.Argument(...),
        path: str = default_path,
        network: NetworkChoices = "testnet") -> None:
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{name}")
    conn = XRPLConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)

    result = TransactionBuilder.set_issuer(
        conn=conn,
        wallet=issuer_wallet,
        domain=domain
    )
    print(result)


@wallet_app.command()
def set_trustline(issuer: str,
                  distributor: str,
                  code: str = uuid.uuid4(),
                  nft: bool = True,
                  path: str = default_path,
                  network: NetworkChoices = "testnet") -> None:
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    distributor_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{distributor}")
    conn = XRPLConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)

    result = TransactionBuilder.set_trustline(
        conn=conn,
        issuer=issuer_wallet,
        distributor=distributor_wallet,
        code=code,
        nft=nft
    )
    print(result)


@wallet_app.command()
def send_token(issuer: str,
               distributor: str,
               code: str,
               memo: str,
               format: str,
               path: str = default_path,
               network: NetworkChoices = "testnet"):
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    distributor_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{distributor}")
    conn = XRPLConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)

    result = TransactionBuilder.issue_transaction_token(
        conn=conn,
        issuer=issuer_wallet,
        distributor=distributor_wallet,
        code=code,
        memo=memo,
        format=format
    )
    print(result)
