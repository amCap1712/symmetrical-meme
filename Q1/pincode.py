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


def get_pincode(address: str):
    """ Extract and return the pincode from the given address.

        Assumes the last number (6 digits) of the address are always the pincode.
    """
    return address[-6:]


def verify_address(address) -> bool:
    """ Verify whether the given address actually lies in the pincode it has.

    :param address: the address to check
    :return: the address is correct or not
    """
    pincode = get_pincode(address)
    post_offices = get_post_offices(pincode)
    for post_office in post_offices:
        if post_office["Name"] in address:
            return True
    return False


if __name__ == '__main__':
    addr = input("Enter address: ")
    print(verify_address(addr))
