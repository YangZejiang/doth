# -*- coding: utf-8 -*-
'''
@File    :   sc_connector.py
@Time    :   2022-05-13 21:03:42
@Author  :   Zejiang Yang
'''

import json
from web3 import Web3, exceptions


MY_ADDRESS = '0x6595cd432df8693C6b9f4e318Ea4A452614C726B'
PRIVATE_KEY = '8654a13f94293c061c991439ea7612664287ec0a4ba62a563e0a15948bfabbe5'
INFURA_URL = "https://kovan.infura.io/v3/e3b3cf0628f04f2c9e54ccd14355ff57"
CHAIN_ID = 42  # kovan
DOTH_CONTRACT_ADDRESS = '0x80596450a684A8c43e57c1B246C690Cb85EA2138'

# load abi
with open('abi.json', 'r') as f:
    ABI = json.load(f)

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
doth = w3.eth.contract(address=DOTH_CONTRACT_ADDRESS, abi=ABI)


def get_latest_txn():
    return {
        'chainId': CHAIN_ID,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.getTransactionCount(MY_ADDRESS),
        'from': MY_ADDRESS,
    }


def sign_send_transaction(txn):
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    # 超时处理
    # try:
    #     tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash, timeout=120)
    # except exceptions.TimeExhausted as e:
    #     print(e)
    #     return False
    print('//' * 50)
    print(tx_receipt)
    print()
    return True


##
#   Write Contract
##
def addAllowedToken(token):
    if isTokenExisted(token):
        return False
    transaction = doth.functions.addAllowedToken(token).buildTransaction(
        get_latest_txn()
    )
    return sign_send_transaction(transaction)


def removeAllowedToken(token):
    if not isTokenExisted(token):
        return False
    transaction = doth.functions.removeAllowedToken(token).buildTransaction(
        get_latest_txn()
    )
    return sign_send_transaction(transaction)


def addManager(address):
    if isManager(address):
        return False
    transaction = doth.functions.addManager(address).buildTransaction(get_latest_txn())
    return sign_send_transaction(transaction)


def removeManager(address):
    if not isManager(address):
        return False
    transaction = doth.functions.removeManager(address).buildTransaction(
        get_latest_txn()
    )
    return sign_send_transaction(transaction)


def repayByUSD(user, amount):
    transaction = doth.functions.repayByUSD(user, amount).buildTransaction(
        get_latest_txn()
    )
    return sign_send_transaction(transaction)


def setAPY(apy):
    transaction = doth.functions.setAPY(apy).buildTransaction(get_latest_txn())
    return sign_send_transaction(transaction)


def setAPR(apr):
    transaction = doth.functions.setAPR(apr).buildTransaction(get_latest_txn())
    return sign_send_transaction(transaction)


def setInitialLTV(ltv):
    # FIXME: 合约这个方法名 英文拼写错了。。。
    transaction = doth.functions.setIntialLTV(ltv).buildTransaction(get_latest_txn())
    return sign_send_transaction(transaction)


def setMarginCallLTV(ltv):
    transaction = doth.functions.setMarginCallLTV(ltv).buildTransaction(
        get_latest_txn()
    )
    return sign_send_transaction(transaction)


def setLiquidationLTV(ltv):
    transaction = doth.functions.setLiquidationLTV(ltv).buildTransaction(
        get_latest_txn()
    )
    return sign_send_transaction(transaction)


def setPriceFeedContract(feed_address):
    transaction = doth.functions.setPriceFeedContract(feed_address).buildTransaction(
        get_latest_txn()
    )
    return sign_send_transaction(transaction)


def iWithdraw(to, token, amount):
    # to: user address
    # token: token address
    transaction = doth.functions.iWithdraw(to, token, amount).buildTransaction(
        get_latest_txn()
    )
    return sign_send_transaction(transaction)


##
#   Read Contract
##
def getAPR():
    return doth.functions.APR().call() / 1e8


def getAPY():
    return doth.functions.APY().call() / 1e8


def getAllowedTokens():
    return doth.functions.allowedTokens().call()


def getDepositors():
    return doth.functions.getDepositors().call()


def getBorrowers():
    return doth.functions.getBorrowers().call()


def getLTV(user):
    return doth.functions.getLTV(user).call() / 1e4


def getTokenValue(token):
    price, decimal = doth.functions.getTokenValue(token).call()
    return price / 10**decimal


def getTotalTokens():
    tokens, amounts = doth.functions.getTotalTokens().call()
    new_amounts = [i / 1e18 for i in amounts]
    return tokens, new_amounts


def getUserLoanValue(user):
    return doth.functions.getUserLoanValue(user).call() / 1e2


def getUserSingleTokenAmount(user, token):
    return doth.functions.getUserSingleTokenAmount(user, token).call() / 1e18


def getUserSingleTokenValue(user, token):
    return doth.functions.getUserSingleTokenValue(user, token).call() / 1e2


def getUserTotalValue(user):
    return doth.functions.getUserTotalValue(user).call() / 1e2


def getInitialLTV():
    return doth.functions.initialLTV().call() / 1e4


def getMargincallLTV():
    return doth.functions.marginCallLTV().call() / 1e4


def getLiquidationLTV():
    return doth.functions.liquidationLTV().call() / 1e4


def isTokenExisted(token):
    return doth.functions.isTokenExisted(token).call()


def isManager(address):
    return doth.functions.isManager(address).call()


def getTokenPriceFeedAddress(token):
    return doth.functions.tokenPriceFeedMapping(token).call()


# if __name__ == '__main__':
# test
# addAllowedToken('0x0000000000000000000000000000000000000000')
# print(isTokenExisted('0x0000000000000000000000000000000000000000'))
# removeAllowedToken('0x0000000000000000000000000000000000000000')
# print(isTokenExisted('0x0000000000000000000000000000000000000000'))

# addManager('0x0000000000000000000000000000000000000000')
# print(isManager('0x0000000000000000000000000000000000000000'))
# removeManager('0x0000000000000000000000000000000000000000')
# print(isManager('0x0000000000000000000000000000000000000000'))

# print(getUserLoanValue('0x6595cd432df8693C6b9f4e318Ea4A452614C726B'))
# repayByUSD('0x6595cd432df8693C6b9f4e318Ea4A452614C726B', 100)
# print(getUserLoanValue('0x6595cd432df8693C6b9f4e318Ea4A452614C726B'))

# setAPY(4000000)
# print(getAPY())
# setAPY(3000000)
# print(getAPY())

# setAPR(10000000)
# print(getAPR())
# setAPR(9000000)
# print(getAPR())

# setInitialLTV(6600)
# print(getInitialLTV())
# setInitialLTV(6500)
# print(getInitialLTV())

# setMarginCallLTV(7600)
# print(getMargincallLTV())
# setMarginCallLTV(7500)
# print(getMargincallLTV())

# setLiquidationLTV(8400)
# print(getLiquidationLTV())
# setLiquidationLTV(8300)
# print(getLiquidationLTV())

# print(getDepositors())
# print(getBorrowers())
# print(getLTV('0x6595cd432df8693C6b9f4e318Ea4A452614C726B'))
# print(getTokenValue('0xd0A1E359811322d97991E03f863a0C30C2cF029C'))
# print(getTotalTokens())

# print(getUserSingleTokenAmount('0x6595cd432df8693C6b9f4e318Ea4A452614C726B', '0xd0A1E359811322d97991E03f863a0C30C2cF029C'))
# print(getUserSingleTokenValue('0x6595cd432df8693C6b9f4e318Ea4A452614C726B', '0xd0A1E359811322d97991E03f863a0C30C2cF029C'))
# print(getUserTotalValue('0x6595cd432df8693C6b9f4e318Ea4A452614C726B'))
# print(getTokenPriceFeedAddress('0xd0A1E359811322d97991E03f863a0C30C2cF029C'))
