from typing import List

import typer

from filedgr_xrpl_cli.dto.memo import MyMemos, MyMemo
from filedgr_xrpl_cli.dto.network import NetworkChoices, all_networks
from filedgr_xrpl_cli.my_xrpl.connection import XRPLConnection
from filedgr_xrpl_cli.my_xrpl.tx import TransactionBuilder
from filedgr_xrpl_cli.my_xrpl.wallet import FileWalletLoader
from filedgr_xrpl_cli.settings import default_path

payment_app = typer.Typer()


@payment_app.command()
def send_token(issuer: str,
               distributor: str,
               code: str,
               memo: str = '',
               memo_format: str = '',
               memos: str = '',
               path: str = default_path,
               network: NetworkChoices = "testnet"):
    issuer_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{issuer}")
    distributor_wallet = FileWalletLoader().load_wallet(f"{path}/wallets/{distributor}")
    conn = XRPLConnection(json_rpc_url=all_networks.get(network.value).json_rpc_url)

    # TODO: need to return to the typer help loop
    c_memos: List[MyMemo] = None
    if memo != '' and memo_format != '':
        c_memos = [MyMemo(
            memo=memo,
            memo_format=memo_format
        )]
    elif memos != '':
        # load the memos file
        my_memos = MyMemos.parse_file(memos)
        c_memos = my_memos.__root__
        pass

    result = TransactionBuilder.issue_transaction_token(
        conn=conn,
        issuer=issuer_wallet,
        distributor=distributor_wallet,
        code=code,
        memos=c_memos
    )
    print(result)
