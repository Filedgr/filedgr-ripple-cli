import sys
import uuid
from pathlib import Path

import orjson
import typer
from filedgr_nft_protobuf.serialize import serialize

from .dto.network import NetworkChoices, all_networks
from .ripple.connection import RippleConnection
from .ripple.tx import TransactionBuilder
from .ripple.wallet import FileWalletLoader

default_path = f"{Path.home()}/.filedger-ripple-cli"
main = typer.Typer()


@main.command("init")
def init(path: str = default_path):
    from .my_io.file_io import MyFileIO

    # Creating the directory if it does not exist
    MyFileIO.create_dir(path)

    # Creating the wallet directory
    MyFileIO.create_dir(f"{path}/wallets")

    # Write the default config
    networks = all_networks
    MyFileIO.write_to_file(f"{path}/networks", orjson.dumps(networks, default=lambda x: x.dict()).decode("utf-8"))


@main.command("create-wallet")
def create_wallet(name: str, dump: bool = True, path: str = default_path, network: NetworkChoices = "testnet") -> None:
    from .ripple.connection import RippleConnection
    from .ripple.wallet import RippleWallet
    from .my_io.file_io import MyFileIO

    conn = RippleConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)
    if network == NetworkChoices.testnet:
        wallet = RippleWallet.create_testnet_wallet(conn.get_client())
    else:
        wallet = RippleWallet.create_wallet()

    wallet_json = orjson.dumps(wallet.get_wallet().__dict__).decode("utf8")
    if dump:
        MyFileIO.write_to_file(path=f"{path}/wallets/{name}", content=wallet_json)
    typer.echo(f"Created wallet: {wallet_json}")


@main.command("set-issuer")
def set_issuer(issuer: str,
               domain: str = typer.Argument(...),
               path: str = default_path,
               network: NetworkChoices = "testnet") -> None:
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    conn = RippleConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)

    result = TransactionBuilder.set_issuer(
        conn=conn,
        wallet=issuer_wallet,
        domain=domain
    )
    typer.echo(result)


@main.command("set-distributor")
def set_distributor(issuer: str,
                    domain: str = typer.Argument(None),
                    path: str = default_path,
                    network: NetworkChoices = "testnet") -> None:
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    conn = RippleConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)

    result = TransactionBuilder.set_issuer(
        conn=conn,
        wallet=issuer_wallet,
        domain=domain
    )
    typer.echo(result)


@main.command("set-trustline")
def set_trustline(issuer: str,
                  distributor: str,
                  code: str = uuid.uuid4(),
                  nft: bool = True,
                  path: str = default_path,
                  network: NetworkChoices = "testnet") -> None:
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{distributor}")
    distributor_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    conn = RippleConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)

    result = TransactionBuilder.set_trustline(
        conn=conn,
        issuer=issuer_wallet,
        distributor=distributor_wallet,
        code=code,
        nft=nft
    )
    typer.echo(result)


@main.command("issue-nft")
def issue_nft(issuer: str,
              id: str,
              campaign: str,
              uri: str,
              path: str = default_path,
              network: NetworkChoices = "testnet"):
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    conn = RippleConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)

    nft_uri = serialize(
        nft_id=id,
        campaign=campaign,
        uri=uri
    )

    result = TransactionBuilder.issue_nft(
        conn=conn,
        issuer=issuer_wallet,
        uri=nft_uri.decode("utf8")
    )
    typer.echo(result)


@main.command("create-t-token")
def create_t_token(issuer: str,
                   distributor: str,
                   code: str,
                   memo: str,
                   format: str,
                   path: str = default_path,
                   network: NetworkChoices = "testnet"):
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{distributor}")
    distributor_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    conn = RippleConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)

    result = TransactionBuilder.issue_transaction_token(
        conn=conn,
        issuer=issuer_wallet,
        distributor=distributor_wallet,
        code=code,
        memo=memo,
        format=format
    )
    typer.echo(result)


if __name__ == '__main__':
    sys.exit(main())