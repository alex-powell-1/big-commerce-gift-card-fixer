import requests
import creds

"""
Big Commerce Gift Card Fixer
Author: Alex Powell
Written: January 3, 2024
Summary: Takes gift card code and changes gift card recipient email address. Helpful when users
accidentally enter the wrong email address for recipients
Changes: Version 2: 
-Added else statement for invalid gift cards
-Added recursion to run function again if try again is needed

Changes: Version 3:
-Added while loop to traverse pages for lists of gift cards over 250 in size.  
"""
client_id = creds.client_id
access_token = creds.access_token
store_hash = creds.store_hash


def get_gift_cards(page):
    url = f" https://api.bigcommerce.com/stores/{store_hash}/v2/gift_certificates?page={page}&limit=250"
    headers = {
        'X-Auth-Token': access_token,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)
    try:
        gift_cards = response.json()
    except requests.exceptions.JSONDecodeError:
        return
    else:
        return gift_cards


def find_specific_gift_card(gift_card_code):
    page = 1
    has_more_pages = True
    while has_more_pages:
        gift_cards = get_gift_cards(page)
        if gift_cards is not None:
            for x in gift_cards:
                if x['code'] == gift_card_code:
                    id = x['id']
                    to_name = x['to_name']
                    to_email = x['to_email']
                    from_name = x['from_name']
                    from_email = x['from_email']
                    amount = x['amount']
                    return id, to_name, to_email, from_name, from_email, amount
            page += 1
        else:
            has_more_pages = False


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
    gc_id = input("What is the code? ")
    index = 1
    gift_card_to_fix = find_specific_gift_card(gc_id)
    if gift_card_to_fix is not None:
        fixed_email = input("What is the correct email address? ")
        if not gift_card_to_fix == "No such gift card":
            old_email = gift_card_to_fix[2]
            fix_gift_card(gift_card_to_fix, fixed_email)
            return f"Done: {old_email} changed to {fixed_email} for gift card: {gc_id}"
    else:
        print("No such gift card. Try again.")
        return gift_card_fixer()


print(gift_card_fixer())
