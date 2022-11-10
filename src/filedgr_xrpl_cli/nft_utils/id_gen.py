from random import randint


# TODO: In the cloud system check for uniqueness
def generate_nft_or_campaign_id() -> str:
    """
    Method to generate an 8 character long base58 nft id.
    :return: 8 character long id
    """
    base_58_characters = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    result = ''
    for i in range(0,8):
         result += base_58_characters[randint(0, len(base_58_characters)-1)]
    return result
