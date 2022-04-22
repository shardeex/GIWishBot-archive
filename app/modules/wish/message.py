from app import genshin
from app.loader import i18n, assets_path
from app.schema import Player


_ = i18n.lazy_gettext

def get_now(
    lang: str,
    player: Player,
    username: str,
    item: genshin.Character | genshin.Weapon,
    info: str
    ) -> str:
    '''_summary_

    :param str lang: _description_
    :param Player player: _description_
    :param str name: _description_
    :param genshin.Character | genshin.Weapon item: _description_
    :param str info: _description_
    :return str: _description_
    '''
    preview = f'<a href="{assets_path}/images/wishes/{lang}/{item.id}.png">\u2060</a>'
    mention = f'<a href="tg://user?id={player.id}">{username}</a>'
    name = item.get_name(lang, rarity=True)
    desc = item.get_desc(lang)
    strings = (
        _('{preview}{desc}\n').format(preview=preview, desc=desc),
        _('{mention}, you received <b>{name}</b>! {info}').format(
            mention=mention, name=name, info=info))
    return preview + '\n'.join(strings)

def get_later(player: Player, name: str, time_left: str):
    '''_summary_

    :param Player player: _description_
    :param str name: _description_
    :param str time_left: _description_
    :return _type_: _description_
    '''
    mention = f'<a href="tg://user?id={player.id}">{name}</a>'
    return _('{mention}, you can wish again in {time_left}.').format(
        mention=mention, time_left=time_left)

def get_cashback_alert():
    '''_summary_

    :return _type_: _description_
    '''
    return _(
        'You can wish in group chat to get ' +
        '<b>Masterless Stardust</b> and <b>Masterless Starglitter</b>.')
