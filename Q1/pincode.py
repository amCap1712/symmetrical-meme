import sys

import requests

from models import PostOfficeT, ResponseT

API_URL = "https://api.postalpincode.in/pincode"


def get_post_offices(pincode: str) -> list[PostOfficeT] | None:
    """ Query the postal pincode API for the given pincode.

        :arg pincode: the postal code to query post offices for
        :return the list of post offices associated with the given pincode
    """
    url = f"{API_URL}/{pincode}"
    response = requests.get(url)
    response.raise_for_status()
    data: ResponseT = response.json()[0]
    return data["PostOffice"]


def get_pincode(address: str) -> str | None:
    """ Extract and return the pincode from the given address. """
    # removes full-stop and commas from the address to improve chances of extracting the pincode
    address = address.replace(".", "")
    address = address.replace(",", "")

    # iterate from last to front and whenever a block of 6 digits is encountered, extract it as the pincode
    words = address.split()
    words.reverse()
    for word in words:
        if word.isdigit() and len(word) == 6:
            return word

    return None


def verify_address(address) -> bool:
    """ Verify whether the given address actually lies in the pincode it has.

    :param address: the address to check
    :return: the address is correct or not
    """
    address = address.lower()

    pincode = get_pincode(address)
    if pincode is None:
        return False

    post_offices = get_post_offices(pincode)
    for post_office in post_offices:
        if post_office["Name"].lower() in address:
            return True

    return False


def run_tests() -> int:
    testcases = [
        ("2nd Phase, 374/B, 80 Feet Rd, Bank Colony, Banashankari 3rd Stage, Srinivasa Nagar, Bengaluru, Karnataka 560050", True),
        ("374/B, 80 Feet Rd, State Bank Colony, Banashankari 3rd Stage, Srinivasa Nagar, Bangalore. 560050", True),
        ("374/B, 80 Feet Rd, State Bank Colony, Banashankari 3rd Stage, Srinivasa Nagar, Bangalore. 560050.", True),
        ("374/B, 80 Feet Rd, State Bank Colony, Banashankari 3rd Stage, Srinivasa Nagar, Bangalore. 560050. Karnataka", True),
        ("2nd Phase, 374/B, 80 Feet Rd, Mysore Bank Colony, Banashankari 3rd Stage, Srinivasa Nagar, Bengaluru, Karnataka 560095", False),
        ("Colony, Bengaluru, Karnataka 560050", False),
    ]

    failures = 0
    for address, expected in testcases:
        received = verify_address(address)
        if expected != received:
            print(f"Test Failed. Address: '{address}'. Expected: {expected}. Received: {received}.", file=sys.stderr)
            failures += 1
    return failures


if __name__ == '__main__':
    count = run_tests()
    if count:
        sys.exit(f"{count} test failure(s).")
