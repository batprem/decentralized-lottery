from .helpful_script import get_account, get_contract
from brownie import Lottery, network, config


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


def main():
    deploy_lottery()
