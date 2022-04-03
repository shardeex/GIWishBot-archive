import json

import sqlalchemy

from .main import metadata


# four lists with char and wepn ids in showcase
showcase_default: list[list[str]] = [list() for n in range(4)]

# item ids as keys, numbers as values
invnetory_default: dict[str, int] = {}

# pity data for 4* and 5*
pities_default = {
    str(n): {"pity": 0, "isweapon": None, "twice": False} for n in (4, 5)}

table = sqlalchemy.Table('players', metadata,
    # id: telegram user id.
    sqlalchemy.Column(
        'id', sqlalchemy.BigInteger, primary_key=True),
    # showcase: player profile character showcase
    sqlalchemy.Column(
        'showcase', sqlalchemy.JSON, server_default=json.dumps(showcase_default)),
    # inventory: player characters and weapons
    sqlalchemy.Column(
        'inventory', sqlalchemy.JSON, server_default=json.dumps(invnetory_default)),
    # pities: player's data about pities
    sqlalchemy.Column(
        'pities', sqlalchemy.JSON, server_default=json.dumps(pities_default)),
    sqlalchemy.Column(
        'wishes', sqlalchemy.Integer, server_default='0'),
    # blessing_of_the_welkin_moon: does player have purchased moon or not
    sqlalchemy.Column(
        'blessing_of_the_welkin_moon', sqlalchemy.Boolean, server_default='false'),
    # last_wish: last normal wish time
    sqlalchemy.Column(
        'last_wish', sqlalchemy.DateTime, server_default='-infinity'),
    # moon_last_wish: last moon wish time
    sqlalchemy.Column(
        'moon_last_wish', sqlalchemy.DateTime, server_default='-infinity'),
    sqlalchemy.Column(
        'masterless_stardust', sqlalchemy.Integer, server_default='0'),
    sqlalchemy.Column(
        'masterless_starglitter', sqlalchemy.Integer, server_default='0'),
    sqlalchemy.Column(
        'genesis_crystals', sqlalchemy.Integer, server_default='0'),
    )
