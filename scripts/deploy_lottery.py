from .helpful_script import get_account, get_contract, fund_contract_with_link
from brownie import Lottery, network, config
import time


def deploy_lottery():
    account = get_account()
    fee = config["networks"][network.show_active()]["fee"]
    fee = eval(fee)
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        fee,
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(lottery)
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)

    print("The lottery is started")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    recieve = lottery.getEntranceFee()
    value = recieve + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # fund contract
    tx = fund_contract_with_link(lottery.address)
    # tx.wait(1)
    # then end contract
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(180)
    print(f"{lottery.recentWinner()} is the new winner!")
    # tx =


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
