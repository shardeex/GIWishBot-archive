from dataclasses import dataclass

from .item import Item


@dataclass(repr=False)
class Weapon(Item):
    type: str

    category = 'weapons'

    def name_with_number(
        self, locale: str, number: int, extra: bool = False) -> str:
        return self.name_with_replica(locale, number, extra)
    
    def name_with_replica(
        self, locale: str, number: int, extra: bool = False) -> str:
        """Get weapon name like "Rust R4"

        Args:
            locale (str): weapon name locale
            number (int): replica number
            extra (bool, optional): add extra replicas or not.
            Defaults to False.

        Returns:
            str: name with replica, e.g. "Rust R4"
        """
        if not extra or number <= 5:  # no extra replica
            return f'{self.name[locale]} R{number if number <= 5 else 5}'
        else:
            return f'{self.name[locale]} R5+{number-5}'
