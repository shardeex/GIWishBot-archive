from dataclasses import dataclass

from .item import Item


@dataclass(repr=False)
class Character(Item):
    weapon: str
    vision: str

    category = 'characters'

    def name_with_number(
        self, locale: str, number: int, extra: bool = False) -> str:
        return self.name_with_constellation(locale, number, extra)

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
            return f'{self.name[locale]} C{number-1 if number <= 7 else 6}'  # C0 means 1, C1 - 2..
        else:
            return f'{self.name[locale]} C6+{number-7}'