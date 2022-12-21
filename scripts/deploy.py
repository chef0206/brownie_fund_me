from brownie import network, config, FundMe, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fundMe():
    account = get_account()
    # Pass price feed address to out FundMe contract

    # if we are on a persistent network like goerli, use the associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    # Deploy our own price feed contract i.e. mocking
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # publish_source is set to true to verify the transaction on a chain
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    print("Deploying the FundMe contract\n")
    deploy_fundMe()
