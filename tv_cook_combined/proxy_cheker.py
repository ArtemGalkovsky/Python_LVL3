from grequests import get as gget, map as gmap
from datetime import datetime

PROXY_CHECKER_TIMEOUT_SECONDS = 10
PROXY_CHECKER_SIZE = 5000

def check(proxies: list[str]) -> list[str]:
    print(f"[proxy_checker](check) Start checking proxies... Amount of proxies is {len(proxies)}")
    proxies_requests = [gget(f"http://steamcommunity.com/market", proxies={"http": proxy},
                             timeout=PROXY_CHECKER_TIMEOUT_SECONDS) for proxy in proxies]
    proxies_responses = gmap(proxies_requests, size=PROXY_CHECKER_SIZE)
    print("[proxy_checker](check) End checking proxies!")

    good_proxies = []
    for response, proxy in zip(proxies_responses, proxies):
        if response:
            good_proxies.append(proxy)

    print("[proxy_checker](check) Amount of good proxies is:", len(good_proxies))

    return good_proxies


def check_with_printing(proxies: list[str]) -> list[str]:
    start_time = datetime.now()
    print(f"[proxy_checker](check_with_printing) Start checking proxies... Amount of proxies is {len(proxies)}")

    good_proxies = []
    for i in range(0, len(proxies), PROXY_CHECKER_SIZE):
        current_proxies = proxies[i:i + PROXY_CHECKER_SIZE]
        print(f"[proxy_checker](check_with_printing) Checking proxies starting from #{i} "
              f"{len(current_proxies)} proxies!")

        proxies_requests = [gget(f"http://steamcommunity.com/market", proxies={"http": proxy},
                                 timeout=PROXY_CHECKER_TIMEOUT_SECONDS) for proxy in current_proxies]
        proxies_response = gmap(proxies_requests, size=PROXY_CHECKER_SIZE)

        for proxy_response, proxy in zip(proxies_response, current_proxies):
            if proxy_response:
                good_proxies.append(proxy)
                print("[proxy_checker](check_with_printing) Found good proxy:", proxy, proxy_response)

        print("[proxy_checker](check_with_printing) Current Result in summary is", len(good_proxies), "good proxies!")

    end_time = datetime.now()
    print(f"[proxy_checker](check_with_printing) End checking proxies in "
          f"{round((end_time - start_time).total_seconds(), 2)}s!")
    print("[proxy_checker](check_with_printing) Amount of good proxies is:", len(good_proxies))

    return good_proxies


if __name__ == '__main__':
    with open("proxies.txt") as fl:
        proxies = fl.read().splitlines()

    print(check(proxies))
