import os

import requests
from time import sleep

import keyboard

def is_webhook_valid(url: str) -> bool:
    if not "http://" in url and not "https://" in url:
        return False
    
    test_req_response = requests.get(url)
    test_req_response_string = str(test_req_response.content)
    print(f"\nWEBHOOK INFO: {test_req_response_string} [For debuging]")
    
    if test_req_response.status_code == 200 or test_req_response.status_code == 204:
        if "token" in test_req_response_string and "url" in test_req_response_string and "channel_id" in test_req_response_string and "guild_id" in test_req_response_string:
            return True
    else:
        return False
    
def force_quit():
    print("Force quiting..")
    os._exit(0)
    
keyboard.add_hotkey("ctrl+q", force_quit)

print("------------ Matrix's Basic Webhook Spammer V4 ------------")

print("\nWebhook URL:")
WEBHOOK_URL: str = input(">>> ")

print("\nText to spam:")
TEXT: str = input(">>> ")

print("\nAmount (Amounts up to 500 is recommended):")
AMOUNT: int = int(input(">>> "))

print("\nMessage cooldown (So the webhook wont get rate limited all the time) (0.1 for instant but will hit rate limits alot)")
COOLDOWN: float = float(input(">>> "))

print("\nRate limit cooldown (For how many seconds the webhook spammer will wait if the webhook gets rate limited) (3 recomended)")
RATE_LIMIT_COOLDOWN: float = float(input(">>> "))

def main() -> None:
    if is_webhook_valid(WEBHOOK_URL) == True:
        print("\nWebhook is valid. Attempt to spam webhook starts in 3 seconds. Press ctrl+q to quit at any time.")
        sleep(3)
        print("Attempt to spam started.")
        
        for _ in range(AMOUNT):
            response = requests.post(url=WEBHOOK_URL, json={"content": TEXT})
            
            if response.status_code == 429 or response.status_code == "429":
                print(f"Webhook failed to send message with status code 429 (Too many requests)")
                sleep(1)
                print(f"Continuing in {RATE_LIMIT_COOLDOWN} seconds.")
                sleep(RATE_LIMIT_COOLDOWN)
                
            elif response.status_code == 404 or response.status_code == "404":
                print("An error has accured trying to send a message thru the webhook. (404 - not found/webhook doesnt exist.)")
                sleep(2)
                print("Automatically aborting in 5 seconds")
                sleep(5)
                quit()
                
            elif response.status_code == 400 or response.status_code == "400":
                print("Failed to reach webhook with status code 400 (bad request - unknown error)")
                sleep(2)
                print("Automatically aborting in 5 seconds")
                sleep(5)
                quit()
                
            else:
                print(f"\nSuccessfully reached {WEBHOOK_URL} with status code {response.status_code}\n")
                
            sleep(COOLDOWN)
        
        sleep(2)      
        print(f"Successfully spammed the webhook {AMOUNT} times with text \"{TEXT}\" (Webhook URL: {WEBHOOK_URL}). Automatically quiting in 5 seconds.")
        
    else:
        print("\nWebhook URL is invalid or an error has accured. Automatically quiting in 5 seconds")
        sleep(5)
        quit()
        
if __name__ == "__main__":
    main()
