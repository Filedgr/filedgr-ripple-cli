import wsgiref.validate

import orjson
import typer
from rich import print
from filedgr_nft_protobuf.serialize import serialize

from filedgr_xrpl_cli.dto.filedgr_nft_type import Xls24dNftType
from filedgr_xrpl_cli.dto.network import NetworkChoices, all_networks
from filedgr_xrpl_cli.my_xrpl.connection import XRPLConnection
from filedgr_xrpl_cli.my_xrpl.tx import TransactionBuilder
from filedgr_xrpl_cli.my_xrpl.wallet import FileWalletLoader
from filedgr_xrpl_cli.settings import default_path

nft_app = typer.Typer()


@nft_app.command()
def mint(issuer: str,
         # campaign_id: str,
         # nft_id: str,
         uri: str,
         path: str = default_path,
         network: NetworkChoices = "testnet"):
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    conn = XRPLConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)

    # nft_uri = serialize(
    #     nft_id=nft_id,
    #     campaign=campaign_id,
    #     uri=uri
    # )

    result = TransactionBuilder.issue_nft(
        conn=conn,
        issuer=issuer_wallet,
        uri=uri
    )
    print(result)


@nft_app.command()
def burn(
        issuer: str,
        token_id: str,
        path: str = default_path,
        network: NetworkChoices = "testnet"
):
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    conn = XRPLConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)
    result = TransactionBuilder.burn_nft(
        conn=conn,
        issuer=issuer_wallet,
        token_id=token_id
    )
    print(result)


@nft_app.command()
def send(
        source: str,
        destination: str,
        token_id: str,
        path: str = default_path,
        network: NetworkChoices = "testnet"
):
    source_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{source}")
    conn = XRPLConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)
    result = TransactionBuilder.send_nft(
        conn=conn,
        source=source_wallet,
        destination=destination,
        token_id=token_id
    )
    print(result)


@nft_app.command()
def generate_meta(
        path: str,
        name: str,
        description: str,
        image: str,
        file: str
):
    nft_type = Xls24dNftType(
        name=name,
        description=description,
        image=image,
        file=file
    )

    nft_type.add_attribute(
        trait_type="smartNft.url",
        value="https://github.com/XRPLF/XRPL-Standards/discussions/69",
        description="The URL to the smart NFT"
    )

    file = None
    try:
        meta_json = nft_type.json(by_alias=True)
        file = open(path, "w")
        file.write(meta_json)
    finally:
        if file:
            file.close()