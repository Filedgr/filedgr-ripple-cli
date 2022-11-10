from __future__ import annotations
from typing import Type

from xrpl.models import Memo, NFTokenMintFlag

from .connection import XRPLConnection
from .wallet import XRPLWallet

import xrpl


class TransactionBuilder:

    @classmethod
    def set_issuer(cls: Type[TransactionBuilder],
                   conn: XRPLConnection,
                   wallet: XRPLWallet,
                   domain: str = None) -> str:
        enc_domain = None
        if domain:
            enc_domain = bytes.hex(domain.encode("ASCII"))

        issuer_settings_tx = xrpl.models.transactions.AccountSet(
            account=wallet.get_wallet().classic_address,
            transfer_rate=0,
            tick_size=5,
            domain=enc_domain,
            set_flag=xrpl.models.transactions.AccountSetFlag.ASF_DEFAULT_RIPPLE,
        )
        cst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
            transaction=issuer_settings_tx,
            wallet=wallet.get_wallet(),
            client=conn.get_client(),
        )

        response = xrpl.transaction.send_reliable_submission(cst_prepared, conn.get_client())
        return response

    @classmethod
    def set_distrutor(cls: Type[TransactionBuilder],
                      conn: XRPLConnection,
                      wallet: XRPLWallet,
                      domain: str = None):
        enc_domain = None
        if domain:
            enc_domain = bytes.hex(domain.encode("ASCII"))

        hot_settings_tx = xrpl.models.transactions.AccountSet(
            account=wallet.get_wallet().classic_address,
            set_flag=xrpl.models.transactions.AccountSetFlag.ASF_REQUIRE_AUTH,
            domain=enc_domain
        )
        hst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
            transaction=hot_settings_tx,
            wallet=wallet.get_wallet(),
            client=conn.get_client(),
        )
        response = xrpl.transaction.send_reliable_submission(hst_prepared, conn.get_client())
        return response

    @classmethod
    def set_trustline(cls: Type[TransactionBuilder],
                      conn: XRPLConnection,
                      issuer: XRPLWallet,
                      distributor: XRPLWallet,
                      code: str,
                      nft: bool) -> str:

        enc_code = bytes.hex(code.encode("utf-8")).upper()
        while len(enc_code) < 40:
            enc_code += "0"

        trust_set_tx = xrpl.models.transactions.TrustSet(
            account=distributor.get_wallet().classic_address,
            limit_amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
                currency=enc_code,
                issuer=issuer.get_wallet().classic_address,
                value="0.000001" if nft else "1"
            )
        )
        ts_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
            transaction=trust_set_tx,
            wallet=distributor.get_wallet(),
            client=conn.get_client(),
        )
        response = xrpl.transaction.send_reliable_submission(ts_prepared, conn.get_client())
        return response

    @classmethod
    def issue_nft(cls: Type[TransactionBuilder],
                  conn: XRPLConnection,
                  issuer: XRPLWallet,
                  uri: str) -> str:
        mint_nft_tx = xrpl.models.transactions.NFTokenMint(
            nftoken_taxon=0,
            account=issuer.get_wallet().classic_address,
            uri=uri.encode(
                'utf-8').hex().upper(),
            flags=[NFTokenMintFlag.TF_BURNABLE, NFTokenMintFlag.TF_TRANSFERABLE]
        )
        mint_nft_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
            transaction=mint_nft_tx,
            wallet=issuer.get_wallet(),
            client=conn.get_client(),
        )
        response = xrpl.transaction.send_reliable_submission(mint_nft_prepared, conn.get_client())
        return response

    @classmethod
    def issue_transaction_token(cls: Type[TransactionBuilder],
                                conn: XRPLConnection,
                                issuer: XRPLWallet,
                                distributor: XRPLWallet,
                                code: str,
                                memo: str,
                                format: str) -> str:

        enc_code = bytes.hex(code.encode("utf-8")).upper()
        while len(enc_code) < 40:
            enc_code += "0"

        quantity = "0.000001"
        memo = Memo(
            memo_data=memo.encode(
                'utf-8').hex().upper(),
            memo_format=format.encode('utf-8').hex().upper()
        )
        send_token_tx = xrpl.models.transactions.Payment(
            account=issuer.get_wallet().classic_address,
            destination=distributor.get_wallet().classic_address,
            amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
                currency=enc_code,
                issuer=issuer.get_wallet().classic_address,
                value=quantity
            ),
            memos=[memo]
        )

        pay_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
            transaction=send_token_tx,
            wallet=issuer.get_wallet(),
            client=conn.get_client(),
        )
        response = xrpl.transaction.send_reliable_submission(pay_prepared, conn.get_client())
        return response
