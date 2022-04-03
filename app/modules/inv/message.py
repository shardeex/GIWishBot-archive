from app import genshin, symbols
from app.loader import i18n
from app.schema import Player


_ = i18n.lazy_gettext


def get(
    player: Player,
    username: str,
    names: list,
    numbers: list,
    category: str = 'all'
    ) -> str:
    mention = f'<a href="tg://user?id={player.id}">{username}</a>'
    sections = []

    match category:
        case 'all':
            sections.append(
                _('{mention}, here is your inventory:').format(
                    mention=mention))
        case 'characters':
            sections.append(
                _('{mention}, here is your characters:').format(
                    mention=mention))
        case 'weapons':
            sections.append(
                _('{mention}, here is your weapons:').format(
                    mention=mention))
        case _:
            raise ValueError(category)

    sections.append('')

    if sum(numbers[1:]) == 0:
        sections.append(
            _('<i>There is no spoon.</i>').value)
        return '\n'.join(sections)
    
    for rarity in range(5, 0, -1):  # [5..1]
        if numbers[rarity] != 0:
            sections.append(
                _('{stars} ({number}):').format(
                    stars=symbols.stars(rarity), number=numbers[rarity]))
            sections.append(', '.join(names[rarity]))
            sections.append('')

    return '\n'.join(sections[:-1])
