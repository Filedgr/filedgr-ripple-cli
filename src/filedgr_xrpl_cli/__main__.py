import sys
import orjson
import typer

from filedgr_xrpl_cli.cli_commands.nfts import nft_app
from filedgr_xrpl_cli.cli_commands.payment import payment_app
from filedgr_xrpl_cli.cli_commands.wallets import wallet_app
from filedgr_xrpl_cli.dto.network import all_networks
from filedgr_xrpl_cli.nft_utils.id_gen import generate_nft_or_campaign_id
from filedgr_xrpl_cli.settings import default_path

app = typer.Typer()
app.add_typer(typer_instance=wallet_app, name="wallet")
app.add_typer(typer_instance=payment_app, name="payment")
app.add_typer(typer_instance=nft_app, name="nft")


@app.command("init")
def init(path: str = default_path):
    from .my_io.file_io import MyFileIO

    # Creating the directory if it does not exist
    MyFileIO.create_dir(path)

    # Creating the wallet directory
    MyFileIO.create_dir(f"{path}/wallets")

    # Write the default config
    networks = all_networks
    MyFileIO.write_to_file(f"{path}/networks", orjson.dumps(networks, default=lambda x: x.dict()).decode("utf-8"))


@app.command("generate-id")
def generate_id():
    nft_result = generate_nft_or_campaign_id()
    campaign_result = generate_nft_or_campaign_id()
    typer.echo(f"The NFT ID: {nft_result}; The campaign ID: {campaign_result}")


if __name__ == '__main__':
    sys.exit(app())
