from dataclasses import dataclass


@dataclass
class Item:
    id: int
    rarity: int
    location: str
    name: dict[str, str]
    description: dict[str, str]

    def __post_init__(self):
        self.name_with_rarity: dict[str, str] = {
            l: f'{n} {"★"*self.rarity}' for l, n in self.name.items()}
        
    def get_name(self, locale: str) -> str:
        """Get localized item name

        Args:
            locale (str): name locale.

        Returns:
            str: localized item name, or 'en' name.
        """
        return self.name.get(locale, self.name['en'])
    
    def get_desc(self, locale: str) -> str:
        """Get localized item description

        Args:
            locale (str): description locale.

        Returns:
            str: localized item description, or 'en' description.
        """
        return self.description.get(locale, self.description['en'])
