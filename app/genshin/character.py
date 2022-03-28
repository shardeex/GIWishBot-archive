from dataclasses import dataclass

from .item import Item


@dataclass
class Character(Item):
    weapon: str
    vision: str
    
    def name_with_constellation(
        self, locale: str, number: int, extra: bool = False) -> str:
        """Get character name with constellation

        Args:
            locale (str): character name locale
            number (int): constellation number
            extra (bool, optional): add extra constellations or not.
            Defaults to False.

        Returns:
            str: name with constellation, e.g. "Lisa C4"
        """
        if not extra or number <= 7:  # no extra const
            return f'{self.name[locale]} C{number-1}'  # C0 means 1, C1 - 2..
        else:
            return f'{self.name[locale]} C6+{number-7}'