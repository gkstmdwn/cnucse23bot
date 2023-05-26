import random

def pickrandom(List:list):
    output = random.choice(List)
    return output

def roll_dice() -> int:
    dice = random.randrange(1,7)
    return dice

def str_to_list(input:str) -> list:
    input = input.replace(", ", "")
    input = input.split(" ")
    input = input[1:]
    return input