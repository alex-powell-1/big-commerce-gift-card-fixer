import requests
import creds

"""
Big Commerce Gift Card Fixer
Author: Alex Powell
Written: January 3, 2024
Summary: Takes gift card code and changes gift card recipient email address. Helpful when users
accidentally enter the wrong email address for recipients 
"""
client_id = creds.client_id
access_token = creds.access_token
store_hash = creds.store_hash

def get_gift_cards():
    url = f" https://api.bigcommerce.com/stores/{store_hash}/v2/gift_certificates"
    headers = {
        'X-Auth-Token': access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)
    gift_cards = response.json()
    return gift_cards

def find_specific_gift_card(gift_cards, gift_card_code):
    for x in gift_cards:
        if x['code'] == gift_card_code:
            id = x['id']
            to_name = x['to_name']
            to_email = x['to_email']
            from_name = x['from_name']
            from_email = x['from_email']
            amount = x['amount']
            return id, to_name, to_email, from_name, from_email, amount
    return "No such gift card"


def fix_gift_card(gift_card, email):
    fix_id = gift_card[0]
    url = f"https://api.bigcommerce.com/stores/{store_hash}/v2/gift_certificates/{fix_id}"
    headers = {
        'X-Auth-Token': access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    payload = {
        "to_name": gift_card[1],
        "to_email": email,
        "from_name": gift_card[3],
        "from_email": gift_card[4],
        "amount": gift_card[5]
    }
    # return payload
    response = requests.put(url, headers=headers, json=payload)
    result = response.text
    return result


def gift_card_fixer():
    id = input("What is the code? ")
    fixed_email = input("What is the correct email address? ")
    gift_card_to_fix = find_specific_gift_card(get_gift_cards(), id)
    if not gift_card_to_fix == "No such gift card":
        old_email = gift_card_to_fix[2]
        fix_gift_card(gift_card_to_fix, fixed_email)
        return f"Done: {old_email} changed to {fixed_email} for gift card: {id}"
    else:
        print("No such gift card. Try again.")
        gift_card_fixer()


print(gift_card_fixer())