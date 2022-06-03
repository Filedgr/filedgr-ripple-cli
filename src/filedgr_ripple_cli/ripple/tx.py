from __future__ import annotations
from typing import Type

from filedgr_ripple_cli.ripple.connection import RippleConnection
from filedgr_ripple_cli.ripple.wallet import RippleWallet

import xrpl


class TransactionBuilder:

    @classmethod
    def set_issuer(cls: Type[TransactionBuilder],
                   conn: RippleConnection,
                   wallet: RippleWallet,
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
                      conn: RippleConnection,
                      wallet: RippleWallet,
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
                      conn: RippleConnection,
                      issuer: RippleWallet,
                      distributor: RippleWallet,
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
