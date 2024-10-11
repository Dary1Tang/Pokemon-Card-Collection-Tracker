# libraries
from pokemontcgsdk import Card
from pokemontcgsdk import Set
import sys
from tabulate import tabulate
import csv

# imports api key
from pokemontcgsdk import RestClient
RestClient.configure()

# main controls the flow of the program
def main():
    output = ""
    # makes sure that the name of the output file is typed
    if len(sys.argv) < 2:
        sys.exit("Please enter output name")
    elif sys.argv[1].endswith(".csv"):
        output = sys.argv[1].replace(".csv", "").strip()
    else:
        output = sys.argv[1].strip()

    # keeps prompting until the user quits
    running = True
    # cards are stored in a list
    collection = []
    # header for the table and csv file
    fields = ["Name", "Card Number", "Set", "Image Preview"]

    while running:
        # prompts the user for the name of the card, if user hits q, the program will export the list into a csv file with the name stated above and exit via sys.exit()
        pokemon_name = input("What card do you wanna search for (q to save and quit)? ").lower().strip()
        if pokemon_name == "q":
                export(fields, collection, output)
                sys.exit()
        # prompts the user for an optional card number
        pokemon_id = input("Please input the card id (optional): ")
        if pokemon_id == "":
            # if user only inputs a name, it will search all the cards with the given name
            collection.append(searchAll(pokemon_name))
        # validates whether the card exists using the name and number
        elif Card.where(q=f"name:{pokemon_name} number:{pokemon_id}") == []:
            print("Invalid Card")
            continue
        else:
            # if user inputs name and number, it will search for the exact card
            collection.append(searchCard(pokemon_name, pokemon_id))
        # checks for duplicate values and removes them
        collection = removeDuplicates(collection)
        # creates a table in the terminal window with the data given
        createTable(collection , fields)

# searches the exact card with given inputs and using the api, returns a list containing the card info
def searchCard(pokemon, id):
    cards = Card.where(q=f"name:{pokemon} number:{id}")
    for card in cards:
        card = [card.name, card.number, card.set.name, card.images.large]
        printCard(card)
        return card


# prints information of what is going to be returned
def printCard(card):
    print()
    print("Name:", card[0])
    print("ID:", card[1])
    print("Set:", card[2])
    print("Image URL:", card[3])
    print()


# searches for all the cards with the given name and then displays the available cards, prompts the user for the right number and runs the searchCard() function
def searchAll(pokemon):
    run = True
    cards = Card.where(q=f"name:{pokemon}")
    for card in cards:
        card = [card.name, card.number, card.set.name, card.images.large]
        printCard(card)
    while run:
        id = input("Please input the id of the card you want to add: ")
        if Card.where(q=f"name:{pokemon} number:{id}") == []:
                print("Invalid Card")
        else:
            break
    return searchCard(pokemon, id)

# creates a table from the list and headers
def createTable(collection, fields):
    table = tabulate(collection, headers=fields, tablefmt="grid")
    print(table)

# exports data into csv file
def export(fields, collection, output):
    output = output + ".csv"
    with open(output, "w") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(collection)

# removes duplicates by creating a new list and filtering out duplicates, returns the updated list
def removeDuplicates(collection):
    updated = []
    for card in collection:
        if card not in updated:
            updated.append(card)
    return updated

if __name__ == "__main__":
    main()

