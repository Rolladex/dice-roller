# -*- coding: utf-8 -*-
"""
┏┓┏━┏┓┏━━┓┏┓┏┓┏┓
┣┓┗┓ ┫┗┓ ┃┣ ┣┓┏┛
┗┛┗┛┗┛┗┛ ╹┗┛┗┛┗━
▄▄▄        ▄▄▌  ▄▄▌   ▄▄▄· ·▄▄▄▄  ▄▄▄ .▐▄• ▄ 
▀▄ █·▪     ██•  ██•  ▐█ ▀█ ██▪ ██ ▀▄.▀· █▌█▌▪
▐▀▀▄  ▄█▀▄ ██▪  ██▪  ▄█▀▀█ ▐█· ▐█▌▐▀▀▪▄ ·██· 
▐█•█▌▐█▌.▐▌▐█▌▐▌▐█▌▐▌▐█ ▪▐▌██. ██ ▐█▄▄▌▪▐█·█▌
.▀  ▀ ▀█▄▀▪.▀▀▀ .▀▀▀  ▀  ▀ ▀▀▀▀▀•  ▀▀▀ •▀▀ ▀▀                   
"""
import random
import re

class Dice:
    def __init__(self, type, number=1):
        self.type = type
        self.number = number

    def roll(self):
        if self.type == "d100":
            return self.roll_percentile()
        else:
            return random.randint(1, self.type)

    def roll_percentile(self):
        tens = random.randint(0, 9)
        ones = random.randint(0, 9)
        if tens == 0 and ones == 0:
            return 100
        return tens * 10 + ones

class Roller:
    def __init__(self):
        self.available_dice = {
            "d20": 20,
            "d12": 12,
            "d10": 10,
            "d8": 8,
            "d6": 6,
            "d4": 4,
            "d100": "percentile"
        }

    def parse_input(self, dice_input):
        components = self._extract_components(dice_input)
        
        rolls = []
        for component in components:
            value = self._evaluate_component(component)
            rolls.append(value)
            
        return rolls

    def _extract_components(self, dice_input):
        pattern = re.compile(r'([+-]?)(?:(\d*)d(\d+)|(\d+))')
        return pattern.findall(dice_input)

    def _evaluate_component(self, component):
        sign, num, dice_type, static_value = component
        
        if static_value:  # handles static bonuses/penalties
            value = int(static_value)
        else:
            value = self._roll_dice(num, dice_type)
        
        # Apply the sign
        value = -value if sign == '-' else value
        return value
    
    def _roll_dice(self, num, dice_type):
        num = 1 if not num else int(num)
        dice_key = f"d{dice_type}"
        if dice_key not in self.available_dice:
            raise ValueError(f"Invalid dice type: {dice_type}. Available dice are: {', '.join(self.available_dice.keys())}")
            
        dice = Dice(self.available_dice[dice_key])
        return sum(dice.roll() for _ in range(num))

    def add_custom_dice(self):
        dice_name = input("Enter the name of the dice (e.g., d7): ").lower()
        while not re.match(r'd\d+', dice_name):
            print("Invalid dice name format. It should start with 'd' followed by a number.")
            dice_name = input("Enter the name of the dice (e.g., d7): ").lower()

        try:
            dice_sides = int(input(f"Enter the number of sides for {dice_name}: "))
        except ValueError:
            print("Invalid number of sides.")
            return

        if dice_name in self.available_dice:
            confirm = input(f"{dice_name} already exists with {self.available_dice[dice_name]} sides. Overwrite? (y/n) ").lower()
            if confirm != 'y':
                return

        self.available_dice[dice_name] = dice_sides
        print(f"{dice_name} with {dice_sides} sides has been added!")

    def prompt_and_roll(self):
        """Interactive prompt for dice rolling."""
        while True:
            print("\nOptions: roll, add, exit")
            choice = input("Choose an option: ").lower()
            
            if choice == 'exit':
                break
            elif choice == 'add':
                self.add_custom_dice()
            elif choice == 'roll':
                dice_input = input("\nEnter dice to roll (e.g., '2d20+1d6-1d8+5') or 'back' to go back: ").lower()
            
                if dice_input == 'back':
                    continue
            
                rolls = self.parse_input(dice_input)  # <-- Fixed this line
                if rolls:
                    total = sum(rolls)
                    print(f"Rolled {dice_input}: {rolls} (Total: {total})")
            else:
                print("Invalid option.")

def main():
    roller = Roller()
    roller.prompt_and_roll()

if __name__ == "__main__":
    main()