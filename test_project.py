import pytest
from project import searchCard

def main():
    test_sylveon()
    test_umbreon()

def test_sylveon():
    assert searchCard('Sylveon', '22') == ['Sylveon', '22', 'Shrouded Fable', 'https://images.pokemontcg.io/sv6pt5/22_hires.png']

def test_umbreon():
    assert searchCard('umbreon', 'TG23') == ['Umbreon VMAX', 'TG23', 'Brilliant Stars Trainer Gallery', 'https://images.pokemontcg.io/swsh9tg/TG23_hires.png']

if __name__ == '__main__':
    main()

