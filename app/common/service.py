from cosmpy.aerial.wallet import LocalWallet
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.client.bank import create_bank_send_msg
from cosmpy.aerial.client.utils import (
    prepare_and_broadcast_basic_transaction,
)
from config import ACCOUNT_MNENONIC, GRPC_URL

NETWORK_CONFIG = NetworkConfig(
    chain_id="pion-1",
    url=GRPC_URL,
    fee_minimum_gas_price=1,
    fee_denomination="untrn",
    staking_denomination="untrn",
)

def send_rewards(address):
    client = LedgerClient(NETWORK_CONFIG)
    sender_wallet = LocalWallet.from_mnemonic(ACCOUNT_MNENONIC, prefix="neutron")

    tx = Transaction()
    tx.add_message(
        create_bank_send_msg(sender_wallet.address(), address, 200000, "untrn")
    )
    tx.add_message(
        create_bank_send_msg(sender_wallet.address(), address, 100000000, "factory/neutron1heydp9f3977kq7c4fecrkra9etdqlu9al954cs/uboom")
    )
    transaction_result = prepare_and_broadcast_basic_transaction(
        client, tx, sender_wallet, gas_limit=350_000, memo="Test msg"
    )
    transaction_result.wait_to_complete()
    return transaction_result._response.code == 0
