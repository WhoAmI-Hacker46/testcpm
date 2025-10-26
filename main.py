#!/usr/bin/python

import random
import requests
from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
import pystyle
from pystyle import Colors, Colorate

from noelcpm import CPMnoelcpm

__CHANNEL_USERNAME__ = "@Sai7Cpm"
__GROUP_USERNAME__   = "@Sai7Cpm"

def signal_handler(sig, frame):
    print("\n Bye Bye...")
    sys.exit(0)

def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ' ':
                color_index = int(((x / (width - 1 if width > 1 else 1)) + (y / (height - 1 if height > 1 else 1))) * 0.5 * (len(colors) - 1))
                color_index = min(max(color_index, 0), len(colors) - 1)  # Ensure the index is within bounds
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text

def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')
    brand_name =  "ATTENTION: TO USE THE TOOL YOU MUST ADD CREDITS WITH THE ADMIN NOEL VENDAS."
    colors = [
        "rgb(255,0,0)", "rgb(255,69,0)", "rgb(255,140,0)", "rgb(255,215,0)", "rgb(173,255,47)", 
        "rgb(0,255,0)", "rgb(0,255,255)", "rgb(0,191,255)", "rgb(0,0,255)", "rgb(139,0,255)",
        "rgb(255,0,255)"
    ]
    colorful_text = gradient_text(brand_name, colors)
    console.print(colorful_text)
    print(Colorate.Horizontal(Colors.rainbow, '=================================================================='))
    print(Colorate.Horizontal(Colors.rainbow, '\t         PLEASE LOG OUT OF CPM BEFORE USING THIS TOOL'))
    print(Colorate.Horizontal(Colors.rainbow, '    SHARING THE ACCESS KEY IS NOT ALLOWED AND WILL BE BLOCKED'))
    print(Colorate.Horizontal(Colors.rainbow, f' ‌           INSTAGRAM: @{__CHANNEL_USERNAME__} WHATSAPP @{__GROUP_USERNAME__}'))
    print(Colorate.Horizontal(Colors.rainbow, '=================================================================='))

def load_player_data(cpm):
    response = cpm.get_player_data()
    if response.get('ok'):
        data = response.get('data')
        if 'floats' in data and 'localID' in data and 'money' in data and 'coin' in data:
        
            print(Colorate.Horizontal(Colors.rainbow, '==========[ PLAYER INFORMATION ]=========='))
            
            print(Colorate.Horizontal(Colors.rainbow, f'NAME   : {(data.get("Name") if "Name" in data else "UNDEFINED")}.'))
                
            print(Colorate.Horizontal(Colors.rainbow, f'YOUR IN-GAME ID: {data.get("localID")}.'))
            
            print(Colorate.Horizontal(Colors.rainbow, f'MONEY  : {data.get("money")}.'))
            
            print(Colorate.Horizontal(Colors.rainbow, f'GOLDS  : {data.get("coin")}.'))
            
        else:
            print(Colorate.Horizontal(Colors.rainbow, '! ERROR: New accounts must be moved at least once !.'))
            exit(1)
    else:
        print(Colorate.Horizontal(Colors.rainbow, '! ERROR: Your login is not configured correctly !.'))
        exit(1)


def load_key_data(cpm):

    data = cpm.get_key_data()
    
    print(Colorate.Horizontal(Colors.rainbow, '========[ ACCESS KEY DETAILS ]========'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'ACCESS KEY      : {data.get("access_key")}.'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'TELEGRAM ID     : {data.get("telegram_id")}.'))
    
    print(Colorate.Horizontal(Colors.rainbow, f'YOUR BALANCE $  : {(data.get("coins") if not data.get("is_unlimited") else "unlimited")}.'))
        
    

def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            print(Colorate.Horizontal(Colors.rainbow, f'{tag} cannot be empty or just spaces. Please try again.'))
        else:
            return value
            
def load_client_details():
    response = requests.get("http://ip-api.com/json")
    data = response.json()
    print(Colorate.Horizontal(Colors.rainbow, '=============[ LOCATION ]============='))
    print(Colorate.Horizontal(Colors.rainbow, f'IP ADDRESS : {data.get("query")}.'))
    print(Colorate.Horizontal(Colors.rainbow, f'CITY       : {data.get("city")} {data.get("regionName")} {data.get("countryCode")}.'))
    print(Colorate.Horizontal(Colors.rainbow, f'COUNTRY    : {data.get("country")} {data.get("zip")}.'))
    print(Colorate.Horizontal(Colors.rainbow, '===============[ MENU ]==============='))

def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb))
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)

def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f'[{interpolated_color}]{char}'
    return modified_string

if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value("[bold][?] ENTER YOUR EMAIL[/bold]", "Email", password=False)
        acc_password = prompt_valid_value("[bold][?] ENTER YOUR PASSWORD[/bold]", "Password", password=False)
        acc_access_key = prompt_valid_value("[bold][?] ENTER YOUR ACCESS KEY[/bold]", "Access Key", password=False)
        console.print("[bold cyan][%] Trying to Login[/bold cyan]: ", end=None)
        cpm = CPMnoelcpm(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                print(Colorate.Horizontal(Colors.rainbow, 'THIS ACCOUNT DOES NOT EXIST.'))
                sleep(2)
                continue
            elif login_response == 101:
                print(Colorate.Horizontal(Colors.rainbow, 'INVALID PASSWORD.'))
                sleep(2)
                continue
            elif login_response == 103:
                print(Colorate.Horizontal(Colors.rainbow, 'INVALID ACCESS KEY.'))
                sleep(2)
                continue
            else:
                print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                print(Colorate.Horizontal(Colors.rainbow, '! NOTICE: DATABASE FULL, CONTACT SUPPORT !.'))
                sleep(2)
                continue
        else:
            print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS.'))
            sleep(2)
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()
            choices = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26"]
           
            print(Colorate.Horizontal(Colors.rainbow, '{03}: INSERT KING RANK  4.000K'))
    
            print(Colorate.Horizontal(Colors.rainbow, '{0} : EXIT'))
            
            print(Colorate.Horizontal(Colors.rainbow, '===============[  CPM☆ ]==============='))
            
            service = IntPrompt.ask(f"[bold][?] SELECT A SERVICE [red][1-{choices[-1]} or 0][/red][/bold]", choices=choices, show_choices=False)
            
            print(Colorate.Horizontal(Colors.rainbow, '===============[  CPM☆ ]==============='))
            
            if service == 0: # Exit
                print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
            elif service == 1: # Increase Money
                print(Colorate.Horizontal(Colors.rainbow, '[?] ENTER THE AMOUNT OF MONEY YOU WANT TO ADD .'))
                amount = IntPrompt.ask("[?] AMOUNT")
                console.print("[%] SAVING DATA: ", end=None)
                if amount > 0 and amount <= 999999999:
                    if cpm.set_player_money(amount):
                        print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ", choices=["y", "n"], default="n")
                        if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f' THANK YOU : @{__CHANNEL_USERNAME__}.'))
                        else: continue
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                        print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED .'))
                    print(Colorate.Horizontal(Colors.rainbow, 'USE VALID VALUES.'))
                    sleep(2)
                    continue
            elif service == 2: # Increase Coins
                print(Colorate.Horizontal(Colors.rainbow, '[?] ENTER THE NUMBER OF GOLDS YOU WANT TO ADD.'))
                amount = IntPrompt.ask("[?] AMOUNT")
                console.print("[%] SAVING DATA: ", end=None)
                if amount > 0 and amount <= 999999999:
                    if cpm.set_player_coins(amount):
                        print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ", choices=["y", "n"], default="n")
                        if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f' THANK YOU : @{__CHANNEL_USERNAME__}.'))
                        else: continue
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                        print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'USE VALID VALUES.'))
                    sleep(2)
                    continue
            elif service == 3: # King Rank
                console.print("[bold red][!] ATTENTION:[/bold red]: IF KING DOES NOT APPEAR, EXIT AND OPEN THE GAME A FEW TIMES.", end=None)
                console.print("[bold red][!] ATTENTION:[/bold red]: IF STILL NOT APPEARING, EXIT AND ENTER UNTIL IT DOES, IF NECESSARY DO TWICE.", end=None)
                sleep(2)
                console.print("[%] ADDING KING TO YOUR ACCOUNT: ", end=None)
                if cpm.set_player_rank():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 4: # Change ID
                print(Colorate.Horizontal(Colors.rainbow, '[?] ENTER YOUR NEW ID.'))
                new_id = Prompt.ask("[?] ID")
                console.print("[%] SAVING DATA: ", end=None)
                if len(new_id) >= 0 and len(new_id) <= 999999999 and (' ' in new_id) == False:
                    if cpm.set_player_localid(new_id.upper()):
                        print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ", choices=["y", "n"], default="n")
                        if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f' THANK YOU : @{__CHANNEL_USERNAME__}.'))
                        else: continue
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                        print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'THIS ID IS ALREADY IN USE, TRY ANOTHER.'))
                    sleep(2)
                    continue
            elif service == 5: # Change Name
                print(Colorate.Horizontal(Colors.rainbow, '[?] ENTER YOUR NEW NAME.'))
                new_name = Prompt.ask("[?] NAME")
                console.print("[%] SAVING DATA: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(new_name):
                        print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ", choices=["y", "n"], default="n")
                        if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f' THANK YOU : @{__CHANNEL_USERNAME__}.'))
                        else: continue
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                        print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'USE VALID VALUES.'))
                    sleep(2)
                    continue
            elif service == 6: # Change Name Rainbow
                print(Colorate.Horizontal(Colors.rainbow, '[?] ENTER YOUR NEW NAME ( RGB ).'))
                new_name = Prompt.ask("[?] NAME")
                console.print("[%] SAVING DATA: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(rainbow_gradient_string(new_name)):
                        print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ", choices=["y", "n"], default="n")
                        if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f' THANK YOU : @{__CHANNEL_USERNAME__}.'))
                        else: continue
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                        print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'USE VALID VALUES.'))
                    sleep(2)
                    continue
            elif service == 7: # Number Plates
                console.print("[%] ADDING NUMBER TO PLATES: ", end=None)
                if cpm.set_player_plates():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 8: # Account Delete
                print(Colorate.Horizontal(Colors.rainbow, '[!] AFTER DELETING THE ACCOUNT THERE IS NO GOING BACK!!.'))
                answ = Prompt.ask("[?] DO YOU REALLY WANT TO DELETE THE ACCOUNT (use y for yes and n for no) ?", choices=["y", "n"], default="n")
                if answ == "y":
                    cpm.delete()
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                else: continue
            elif service == 9: # Account Register
                print(Colorate.Horizontal(Colors.rainbow, '[!] LET\'S REGISTER YOUR NEW ACCOUNT.'))
                acc2_email = prompt_valid_value("[?] ENTER AN EMAIL", "Email", password=False)
                acc2_password = prompt_valid_value("[?] ENTER A PASSWORD", "Password", password=False)
                console.print("[%] CREATING YOUR NEW ACCOUNT: ", end=None)
                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    print(Colorate.Horizontal(Colors.rainbow, 'INFO: NOW YOU CAN MODIFY THIS ACCOUNT.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'LOG INTO THE GAME AT LEAST ONCE USING THIS ACCOUNT BEFORE ADDING ANY SERVICE.'))
                    sleep(7)
                    continue
                elif status == 105:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'THIS EMAIL ALREADY EXISTS, TRY A NEW EMAIL THAT IS NOT IN USE !.'))
                    sleep(3)
                    continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 10: # Delete Friends
                console.print("[%] DELETING YOUR FRIEND LIST: ", end=None)
                if cpm.delete_player_friends():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 11: # Unlock All Paid Cars
                console.print("[!] ATTENTION: THIS FUNCTION MAY TAKE A WHILE TO COMPLETE DO NOT CANCEL.", end=None)
                console.print("[%] UNLOCKING ALL PAID CARS: ", end=None)
                if cpm.unlock_paid_cars():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN .'))
                    sleep(2)
                    continue
            elif service == 12: # Unlock All Cars
                console.print("[%] UNLOCKING ALL CARS: ", end=None)
                if cpm.unlock_all_cars():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 13: # Unlock All Cars Siren
                console.print("[%] ADDING SIREN TO ALL ACCOUNT CARS: ", end=None)
                if cpm.unlock_all_cars_siren():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 14: # Unlock w16 Engine
                console.print("[%] UNLOCKING W16 ENGINE: ", end=None)
                if cpm.unlock_w16():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 15: # Unlock All Horns
                console.print("[%] UNLOCKING ALL HORNS: ", end=None)
                if cpm.unlock_horns():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 16: # Disable Engine Damage
                console.print("[%] DISABLING ENGINE DAMAGE: ", end=None)
                if cpm.disable_engine_damage():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 17: # Unlimited Fuel
                console.print("[%] UNLOCKING UNLIMITED FUEL: ", end=None)
                if cpm.unlimited_fuel():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 18: # Unlock House 3
                console.print("[%] UNLOCKING HOUSE 3: ", end=None)
                if cpm.unlock_houses():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 19: # Unlock Smoke
                console.print("[%] UNLOCKING SMOKE: ", end=None)
                if cpm.unlock_smoke():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 20: # Unlock Animations
                console.print("[%] UNLOCKING ANIMATIONS: ", end=None)
                if cpm.unlock_animations():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 21: # Unlock Wheels
                console.print("[%] UNLOCKING WHEELS: ", end=None)
                if cpm.unlock_wheels():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 22: # Unlock Male Clothes
                console.print("[%] UNLOCKING MALE CLOTHES: ", end=None)
                if cpm.unlock_equipments_male():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 23: # Unlock Female Clothes
                console.print("[%] UNLOCKING FEMALE CLOTHES: ", end=None)
                if cpm.unlock_equipments_female():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, 'TRY AGAIN.'))
                    sleep(2)
                    continue
            elif service == 24: # Change Races Wins
                print(Colorate.Horizontal(Colors.rainbow, '[!] ENTER THE NUMBER OF RACES WON .'))
                amount = IntPrompt.ask("[?] ENTER HERE")
                console.print("[%] SAVING DATA: ", end=None)
                if amount > 0 and amount <= 999999999999999999999999999:
                    if cpm.set_player_wins(amount):
                        print(Colorate.Horizontal(Colors.rainbow, 'DONE'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE ( Y ) FOR YES AND ( N ) FOR NO?", choices=["y", "n"], default="n")
                        if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU: @{__CHANNEL_USERNAME__}.'))
                        else: continue
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                        print(Colorate.Horizontal(Colors.rainbow, '[!] USE VALID VALUES.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, '[!] USE VALID VALUES.'))
                    sleep(2)
                    continue
            elif service == 25: # Change Races Loses
                print(Colorate.Horizontal(Colors.rainbow, '[!] ENTER THE NUMBER OF RACES LOST.'))
                amount = IntPrompt.ask("[?] ENTER HERE")
                console.print("[%] SAVING DATA: ", end=None)
                if amount > 0 and amount <= 999999999999999999999:
                    if cpm.set_player_loses(amount):
                        print(Colorate.Horizontal(Colors.rainbow, 'DONE'))
                        print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                        answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE ( Y ) FOR YES AND ( N ) FOR NO ", choices=["y", "n"], default="n")
                        if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                        else: continue
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                        print(Colorate.Horizontal(Colors.rainbow, '[!] PROVIDE THE CORRECT VALUES.'))
                        sleep(2)
                        continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, '[!] PROVIDE THE CORRECT VALUES.'))
                    sleep(2)
                    continue
            elif service == 26: # Clone Account
                print(Colorate.Horizontal(Colors.rainbow, '[!] ENTER THE EMAIL TO CLONE THE ACCOUNT INTO ( NOTE: MUST LOG OUT OF ACCOUNTS FIRST!).'))
                to_email = prompt_valid_value("[?] EMAIL OF ACCOUNT", "Email", password=False)
                to_password = prompt_valid_value("[?] PASSWORD OF ACCOUNT", "Password", password=False)
                console.print("[%] CLONING YOUR ACCOUNT: ", end=None)
                if cpm.account_clone(to_email, to_password):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    print(Colorate.Horizontal(Colors.rainbow, '======================================'))
                    answ = Prompt.ask("[?] DO YOU WANT TO EXIT? USE Y FOR YES AND N FOR NO ?", choices=["y", "n"], default="n")
                    if answ == "y": print(Colorate.Horizontal(Colors.rainbow, f'THANK YOU....: @{__CHANNEL_USERNAME__}.'))
                    else: continue
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED.'))
                    print(Colorate.Horizontal(Colors.rainbow, '[!] USE THE CORRECT VALUES.'))
                    sleep(2)
                    continue
            else: continue
            break
        break
