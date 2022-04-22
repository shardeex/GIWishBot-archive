from types import SimpleNamespace

from app import symbols
from app.loader import i18n, assets_path
from app.schema import Player
from app.database.players import showcase_default


_ = i18n.lazy_gettext

links = SimpleNamespace(
    edit_profile='https://t.me/GIWishBot?start=edit_profile')

def get(
    player: Player,
    username: str,
    showcase: list
    ) -> str:
    mention = f'<a href="tg://user?id={player.id}">{username}</a>'
    # default for now
    preview = f'<a href="{assets_path}/images/namecards/default.png">\u2060</a>'
    strings = []

    strings.append(_(
        '<b>{mention}</b>\' profile:'
        ).format(mention=mention))
    strings.append('')

    strings.append(_(
        '<b>Wish Counter:</b>'
        ).value)
    strings.append(_(
        '<b>[{number}]</b> Lifetime wishes'
        ).format(number=player.wishes))
    strings.append(_(
        '<b>[{number}]</b> 5{star} Pity <i>(guaranteed at 90)</i>'
        ).format(number=player.pities['5']['pity'], star=symbols.stars(1)))
    strings.append(_(
        '<b>[{number}]</b> 4{star} Pity <i>(guaranteed at 10)</i>'
        ).format(number=player.pities['4']['pity'], star=symbols.stars(1)))
    strings.append('')

    strings.append(_(
        '<b>Precious items <u>(not spendable yet)</u>:</b>'
        ).value)
    strings.append(_(
        '<b>[{number}]</b> Masterless Stardust'
        ).format(number=symbols.masterless_stardust(
            player.masterless_stardust)))
    strings.append(_(
        '<b>[{number}]</b> Masterless Starglitter'
        ).format(number=symbols.masterless_starglitter(
            player.masterless_starglitter)))
    strings.append(_(
        '<b>[{number}]</b> Genesis Crystals'
        ).format(number=symbols.genesis_crystals(player.genesis_crystals)))
    strings.append('')

    strings.append(_(
        '<b>Character showcase:</b>'
        ).value)
    if player.showcase == showcase_default:
        strings.append(_(
            '<b><a href="{links.edit_profile}">Tap here</a></b> '
            'to edit your character showcase.'
        ).format(links=links))
    else:
        for i in range(len(showcase)):
            slot = showcase[i]
            if slot is None:
                strings.append(_(
                    '[{position}] No character in slot.'
                ).format(position=i+1))
            else:
                strings.append(_(
                    '[{position}] {character} & {weapon}'
                ).format(position=i+1, character=slot[0], weapon=slot[1]))

    return preview + '\n'.join(strings)
