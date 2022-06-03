import sys
import uuid
from pathlib import Path

import orjson
import typer

from filedgr_ripple_cli.dto.network import NetworkChoices, all_networks
from filedgr_ripple_cli.ripple.connection import RippleConnection
from filedgr_ripple_cli.ripple.tx import TransactionBuilder
from filedgr_ripple_cli.ripple.wallet import RippleWallet, FileWalletLoader

default_path = f"{Path.home()}/.filedger-ripple-cli"
main = typer.Typer()


@main.command("init")
def init(path: str = default_path):
    from filedgr_ripple_cli.my_io.file_io import MyFileIO

    # Creating the directory if it does not exist
    MyFileIO.create_dir(path)

    # Creating the wallet directory
    MyFileIO.create_dir(f"{path}/wallets")

    # Write the default config
    networks = all_networks
    MyFileIO.write_to_file(f"{path}/networks", orjson.dumps(networks, default=lambda x: x.dict()).decode("utf-8"))


@main.command("create-wallet")
def create_wallet(name: str, dump: bool = True, path: str = default_path, network: NetworkChoices = "testnet") -> None:
    from filedgr_ripple_cli.ripple.connection import RippleConnection
    from filedgr_ripple_cli.ripple.wallet import RippleWallet
    from filedgr_ripple_cli.my_io.file_io import MyFileIO

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


@main.command("create-nft")
def create_nft(issuer: str,
               distributor: str,
               nft_id: str,
               path: str = default_path,
               network: NetworkChoices = "testnet"):

    issuer_wallet = FileWalletLoader(f"{path}/wallets/{issuer}")
    distributor_wallet = FileWalletLoader(f"{path}/wallets/{distributor}")


@main.command("create-t-token")
def create_t_token(name: str, path: str = default_path, network: NetworkChoices = "testnet"):
    from filedgr_ripple_cli.my_io.file_io import MyFileIO

    wallet_json = MyFileIO.read_from_file(f"{path}/wallets/{name}")
    wallet_dict = orjson.loads(wallet_json)

    ripple_wallet = RippleWallet(**wallet_dict)

    typer.echo(f"Created NFT from wallet: {wallet_json}, to wallet: ")


if __name__ == '__main__':
    sys.exit(main())
