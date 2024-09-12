from django.conf import settings
from web3 import Web3


def connect_to_web3(rpc_url):
    """
    Connects to a web3 provider.
    """
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise Exception("Failed to connect to web3 provider")
    return web3


def send_ether(web3, source_wallet, source_private_key, recipient, amount):
    """
    Sends ether from a source wallet to a recipient.
    """
    nonce = web3.eth.get_transaction_count(source_wallet)
    tx = {
        "nonce": nonce,
        "to": recipient,
        "value": web3.to_wei(amount, "ether"),
        "gas": 2000000,
        "gasPrice": web3.to_wei("50", "gwei"),
        "chainId": settings.ETH_TESTNET_CHIND_ID
    }
    signed_tx = web3.eth.account.sign_transaction(tx, source_private_key)
    return web3.to_hex(web3.eth.send_raw_transaction(signed_tx.raw_transaction))
