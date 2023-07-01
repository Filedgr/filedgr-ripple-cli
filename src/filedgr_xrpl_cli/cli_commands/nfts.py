import wsgiref.validate
from typing import Optional

import orjson
import typer
import xrpl
from rich import print
from filedgr_nft_protobuf.serialize import serialize

from filedgr_xrpl_cli.dto.filedgr_nft_type import FiledgrArtV0NftType, FiledgrArtV0NftTypeAttributeTraitEnum, \
    FiledgrArtV0NftTypeCollection
from filedgr_xrpl_cli.dto.network import NetworkChoices, all_networks
from filedgr_xrpl_cli.my_xrpl.connection import XRPLConnection
from filedgr_xrpl_cli.my_xrpl.tx import TransactionBuilder
from filedgr_xrpl_cli.my_xrpl.wallet import FileWalletLoader
from filedgr_xrpl_cli.settings import default_path

nft_app = typer.Typer()


@nft_app.command()
def mint(issuer: str,
         uri: str,
         path: str = default_path,
         network: NetworkChoices = "testnet"):
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    conn = XRPLConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)

    result = TransactionBuilder.issue_nft(
        conn=conn,
        issuer=issuer_wallet,
        uri=uri,
    )
    print(result)


@nft_app.command()
def get_id(issuer: str,
         path: str = default_path,
         network: NetworkChoices = "testnet") -> str:

    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    conn = XRPLConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)
    # Predict NFT ID
    account_root = xrpl.account.get_account_root(address=issuer_wallet.get_wallet().classic_address,
                                                 client=conn.get_client())
    account_id = account_root.get("Account")
    minted_tokens = account_root.get("MintedNFTokens")

    # Fees
    fees = 0
    hex_fees = hex(fees).replace("0x", "").upper()
    while len(hex_fees) < 4:
        hex_fees = f"0{hex_fees}"

    hex_sequence = hex(minted_tokens).replace("0x", "").upper()
    while len(hex_sequence) < 8:
        hex_sequence = f"0{hex_sequence}"

    taxon = (1 ^ (384160001 * minted_tokens + 2459)) % 4294967296
    taxon_hex = hex(taxon).replace("0x", "").upper()
    while len(taxon_hex) < 8:
        taxon_hex = f"0{taxon_hex}"
    # return (taxon ^ (384160001 * token_seq + 2459)) % 4294967296

    account_be = xrpl.core.addresscodec.decode_classic_address(account_id)

    token_id = f"000B{hex_fees}{account_be.hex().upper()}{taxon_hex}{hex_sequence}"
    print(token_id)
    return token_id



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
        file: Optional[str] = ''
):
    nft_type = FiledgrArtV0NftType(
        name=name,
        description=description,
        image=image,
        file=file,
        collection=FiledgrArtV0NftTypeCollection(
            name="Filedgr Carbonauten FuckCO2 Hoodies",
            family="Version 0.0.1-BETA"
        )
    )
    nft_type.add_attribute(
        trait_type=FiledgrArtV0NftTypeAttributeTraitEnum.SMART_NFT_URI,
        value="https://github.com/XRPLF/XRPL-Standards/discussions/69",
        description="The URL to the smart NFT"
    )
    nft_type.add_attribute(
        trait_type=FiledgrArtV0NftTypeAttributeTraitEnum.TX_TOKEN,
        value="t_asdada_adad",
        description="The token on XRPL updating data of the NFT"
    )
    nft_type.add_attribute(
        trait_type=FiledgrArtV0NftTypeAttributeTraitEnum.TX_RECEIVER,
        value="rereadadad",
        description="The wallet receiving the transactions updating the NFT."
    )

    file = None
    try:
        meta_json = nft_type.json(by_alias=True)
        file = open(path, "w")
        file.write(meta_json)
    finally:
        if file:
            file.close()
