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

from Sai7Cpm import Sai7Cpm  # renamed module/class

__CHANNEL_USERNAME__ = "Sai7Cpm"
__GROUP_USERNAME__   = "Sai7Cpm"

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
                color_index = min(max(color_index, 0), len(colors) - 1)
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text

def banner(console):
    os.system('cls' if os.name == 'nt' else 'clear')
    brand_name = "ATTENTION: TO USE THIS TOOL, YOU MUST ADD CREDITS WITH ADMIN SAI7CPM."
    colors = [
        "rgb(255,0,0)", "rgb(255,69,0)", "rgb(255,140,0)", "rgb(255,215,0)", "rgb(173,255,47)", 
        "rgb(0,255,0)", "rgb(0,255,255)", "rgb(0,191,255)", "rgb(0,0,255)", "rgb(139,0,255)",
        "rgb(255,0,255)"
    ]
    colorful_text = gradient_text(brand_name, colors)
    console.print(colorful_text)
    print(Colorate.Horizontal(Colors.rainbow, '=================================================================='))
    print(Colorate.Horizontal(Colors.rainbow, '\t         LOG OUT OF CPM BEFORE USING THIS TOOL'))
    print(Colorate.Horizontal(Colors.rainbow, '    SHARING YOUR ACCESS KEY IS NOT ALLOWED AND WILL RESULT IN BLOCKING'))
    print(Colorate.Horizontal(Colors.rainbow, f' ‌           INSTAGRAM: @{__CHANNEL_USERNAME__} WHATSAPP @{__GROUP_USERNAME__}'))
    print(Colorate.Horizontal(Colors.rainbow, '=================================================================='))

def load_player_data(cpm):
    response = cpm.get_player_data()
    if response.get('ok'):
        data = response.get('data')
        if 'floats' in data and 'localID' in data and 'money' in data and 'coin' in data:
            print(Colorate.Horizontal(Colors.rainbow, '==========[ PLAYER INFORMATION ]=========='))
            print(Colorate.Horizontal(Colors.rainbow, f'NAME       : {(data.get("Name") if "Name" in data else "UNDEFINED")}.'))
            print(Colorate.Horizontal(Colors.rainbow, f'GAME ID    : {data.get("localID")}.'))
            print(Colorate.Horizontal(Colors.rainbow, f'MONEY      : {data.get("money")}.'))
            print(Colorate.Horizontal(Colors.rainbow, f'COINS      : {data.get("coin")}.'))
        else:
            print(Colorate.Horizontal(Colors.rainbow, '! ERROR: New accounts must log in at least once!'))
            exit(1)
    else:
        print(Colorate.Horizontal(Colors.rainbow, '! ERROR: Your login is not properly set!'))
        exit(1)

def load_key_data(cpm):
    data = cpm.get_key_data()
    print(Colorate.Horizontal(Colors.rainbow, '========[ ACCESS KEY DETAILS ]========'))
    print(Colorate.Horizontal(Colors.rainbow, f'ACCESS KEY : {data.get("access_key")}.'))
    print(Colorate.Horizontal(Colors.rainbow, f'TELEGRAM ID: {data.get("telegram_id")}.'))
    print(Colorate.Horizontal(Colors.rainbow, f'BALANCE $  : {(data.get("coins") if not data.get("is_unlimited") else "unlimited")}.'))

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

def rainbow_gradient_string(player_name):
    modified_string = ""
    num_chars = len(player_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(player_name):
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
        cpm = Sai7Cpm(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)

        if login_response != 0:
            if login_response == 100:
                print(Colorate.Horizontal(Colors.rainbow, 'THIS ACCOUNT DOES NOT EXIST.'))
            elif login_response == 101:
                print(Colorate.Horizontal(Colors.rainbow, 'INVALID PASSWORD.'))
            elif login_response == 103:
                print(Colorate.Horizontal(Colors.rainbow, 'INVALID ACCESS KEY.'))
            else:
                print(Colorate.Horizontal(Colors.rainbow, 'PLEASE TRY AGAIN. DATABASE FULL, CONTACT SUPPORT.'))
            sleep(2)
            continue
        else:
            print(Colorate.Horizontal(Colors.rainbow, 'LOGIN SUCCESSFUL.'))
            sleep(2)

        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()

            choices = [str(i) for i in range(27)]
            print(Colorate.Horizontal(Colors.rainbow, '{01}: ADD MONEY            1,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{02}: ADD COINS            3,500K'))
            print(Colorate.Horizontal(Colors.rainbow, '{03}: SET KING RANK        4,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{04}: CHANGE ID            3,500K'))
            print(Colorate.Horizontal(Colors.rainbow, '{05}: CHANGE NAME          100'))
            print(Colorate.Horizontal(Colors.rainbow, '{06}: CHANGE NAME (RGB)    100'))
            print(Colorate.Horizontal(Colors.rainbow, '{07}: NUMBER PLATES        2,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{08}: DELETE ACCOUNT       FREE'))
            print(Colorate.Horizontal(Colors.rainbow, '{09}: REGISTER ACCOUNT     FREE'))
            print(Colorate.Horizontal(Colors.rainbow, '{10}: DELETE FRIENDS       500'))
            print(Colorate.Horizontal(Colors.rainbow, '{11}: UNLOCK PAID CARS     4,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{12}: UNLOCK ALL CARS      3,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{13}: ADD SIREN TO ALL CARS 2,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{14}: UNLOCK W16 ENGINE     3,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{15}: UNLOCK ALL HORNS      3,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{16}: DISABLE ENGINE DAMAGE 2,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{17}: UNLIMITED FUEL       2,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{18}: UNLOCK HOUSE 3       3,500K'))
            print(Colorate.Horizontal(Colors.rainbow, '{19}: UNLOCK SMOKE EFFECT  2,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{20}: UNLOCK ANIMATIONS    2,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{21}: UNLOCK WHEELS        4,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{22}: UNLOCK MALE CLOTHES  3,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{23}: UNLOCK FEMALE CLOTHES 3,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{24}: CHANGE RACES WON     1,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{25}: CHANGE RACES LOST    1,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{26}: CLONE ACCOUNT        5,000K'))
            print(Colorate.Horizontal(Colors.rainbow, '{0} : EXIT'))

            service = IntPrompt.ask(f"[bold][?] SELECT A SERVICE [1-{choices[-1]} or 0][/bold]", choices=choices, show_choices=False)

            if service == 0:
                print(Colorate.Horizontal(Colors.rainbow, f'COME BACK SOON....: @{__CHANNEL_USERNAME__}.'))
                break

            # Loop through each service and call corresponding cpm methods
            if service == 1:
                amount = IntPrompt.ask("[?] ENTER THE AMOUNT OF MONEY TO ADD")
                if amount > 0:
                    if cpm.set_player_money(amount):
                        print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'INVALID AMOUNT'))

            elif service == 2:
                amount = IntPrompt.ask("[?] ENTER THE NUMBER OF COINS TO ADD")
                if amount > 0:
                    if cpm.set_player_coins(amount):
                        print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                    else:
                        print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 3:
                if cpm.set_king_rank():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 4:
                new_id = Prompt.ask("[?] ENTER NEW ID")
                if cpm.change_id(new_id):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 5:
                new_name = Prompt.ask("[?] ENTER NEW NAME")
                if cpm.change_name(new_name):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 6:
                new_name = Prompt.ask("[?] ENTER NEW NAME (RAINBOW)")
                rainbow_name = rainbow_gradient_string(new_name)
                if cpm.change_name(rainbow_name):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 7:
                plates = Prompt.ask("[?] ENTER NUMBER PLATES TO SET")
                if cpm.set_number_plates(plates):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 8:
                if cpm.delete_account():
                    print(Colorate.Horizontal(Colors.rainbow, 'ACCOUNT DELETED'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 9:
                if cpm.register_account():
                    print(Colorate.Horizontal(Colors.rainbow, 'ACCOUNT REGISTERED'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 10:
                if cpm.delete_friends():
                    print(Colorate.Horizontal(Colors.rainbow, 'FRIENDS DELETED'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 11:
                if cpm.unlock_paid_cars():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 12:
                if cpm.unlock_all_cars():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 13:
                if cpm.add_siren_to_all_cars():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 14:
                if cpm.unlock_w16_engine():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 15:
                if cpm.unlock_all_horns():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 16:
                if cpm.disable_engine_damage():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 17:
                if cpm.unlimited_fuel():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 18:
                if cpm.unlock_house_3():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 19:
                if cpm.unlock_smoke_effect():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 20:
                if cpm.unlock_animations():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 21:
                if cpm.unlock_wheels():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 22:
                if cpm.unlock_male_clothes():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 23:
                if cpm.unlock_female_clothes():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 24:
                amount = IntPrompt.ask("[?] ENTER RACES WON")
                if cpm.change_races_won(amount):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 25:
                amount = IntPrompt.ask("[?] ENTER RACES LOST")
                if cpm.change_races_lost(amount):
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            elif service == 26:
                if cpm.clone_account():
                    print(Colorate.Horizontal(Colors.rainbow, 'SUCCESS'))
                else:
                    print(Colorate.Horizontal(Colors.rainbow, 'FAILED'))

            sleep(2)
