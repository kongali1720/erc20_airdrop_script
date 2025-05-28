from web3 import Web3
import json
import time

# Config Infura / Alchemy RPC URL
RPC_URL = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
PRIVATE_KEY = "YOUR_PRIVATE_KEY"  # Private key wallet pengirim token
TOKEN_ADDRESS = "0xYourERC20TokenAddress"  # Contract ERC20 Token

# Baca alamat penerima dari file
def read_recipients(filename="recipients.txt"):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not web3.isConnected():
        print("❌ Gagal terhubung ke blockchain.")
        return

    account = web3.eth.account.from_key(PRIVATE_KEY)
    sender_address = account.address

    # ABI minimal untuk ERC20 transfer
    erc20_abi = json.loads('[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"type":"function"}]')

    token_contract = web3.eth.contract(address=web3.toChecksumAddress(TOKEN_ADDRESS), abi=erc20_abi)

    recipients = read_recipients()

    print(f"🚀 Memulai airdrop ke {len(recipients)} alamat...")

    nonce = web3.eth.get_transaction_count(sender_address)

    for i, recipient in enumerate(recipients, start=1):
        try:
            # Atur jumlah token yang akan dikirim (misal 10 token, dengan 18 desimal)
            amount = web3.toWei(10, 'ether')  # sesuaikan dengan decimals token

            tx = token_contract.functions.transfer(
                web3.toChecksumAddress(recipient),
                amount
            ).buildTransaction({
                'chainId': 1,
                'gas': 70000,
                'gasPrice': web3.toWei('50', 'gwei'),
                'nonce': nonce,
            })

            signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"[{i}/{len(recipients)}] ✅ Token berhasil dikirim ke {recipient} | TxHash: {web3.toHex(tx_hash)}")

            nonce += 1
            time.sleep(1)  # delay agar tidak spam node
        except Exception as e:
            print(f"[{i}/{len(recipients)}] ❌ Gagal kirim token ke {recipient}: {e}")

if __name__ == "__main__":
    main()
