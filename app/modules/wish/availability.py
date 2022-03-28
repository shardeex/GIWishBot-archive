import datetime
from typing import *

from app.schema import Player


# wish times. every day users will be available to wish exactly at this time.
# e.g. datetime.time(5) means 5:00AM, datetime.time(18) means 6:00AM.
WISH_TIMES = (datetime.time(9), datetime.time(21))  # 12 and 24 in UTC+3
MOON_WISH_TIMES = (datetime.time(3), datetime.time(15))  # 6 and 18 in UTC+3

FMT_TIME_WORD = {
    # sa - singular accusative, sg - singular genitive, pg - plural genitive
    'ru': lambda n, sa, sg, pg: (
        sa if n % 10 == 1 and n//10 % 10 != 1 else
        sg if n % 10 in (2, 3, 4) and n//10 % 10 != 1 else pg
    ),
    # s - singular, p - plural
    'en': lambda n, s, p: s if n == 1 else p
}

TIME_WORDS = {
    'ru': {
        'hour': ['час', 'часа', 'часов'],
        'minute': ['минуту', 'минуты', 'минут'],
        'second': ['секунду', 'секунды', 'секунд']
    },
    'en': {
        'hour': ['hour', 'hours'],
        'minute': ['minute', 'minutes'],
        'second': ['second', 'seconds']
    }
}

def format_time(lang: str, timedelta: datetime.timedelta) -> str:
    '''_summary_

    :param str lang: _description_
    :param datetime.timedelta timedelta: _description_
    :return str: _description_
    '''
    times = {}
    times['hour'], remainder = divmod(timedelta.seconds, 3600)
    times['minute'], times['second'] = divmod(remainder, 60)

    # hours and minutes if hours not 0, else minutes and seconds
    times.pop('hour') if times['hour'] == 0 else times.pop('second')

    format_tw = FMT_TIME_WORD[lang]
    tw = TIME_WORDS[lang]
    return ' '.join(f'{v} {format_tw(v, *tw[k])}' for k, v in times.items())

def wish_time(
    player: Player,
    check_datetime: datetime.datetime,
    moon=False
) -> Tuple[bool, datetime.timedelta]:
    '''_summary_

    :param Player player: _description_
    :param datetime.datetime check_datetime: _description_
    :param bool moon: _description_, defaults to False
    :return Tuple[bool, datetime.timedelta]: _description_
    '''
    if not moon:
        wish_times = WISH_TIMES
        last_wish = player.last_wish
    else:
        wish_times = MOON_WISH_TIMES
        last_wish = player.moon_last_wish

    # creates last yesterday, all today and first tomorrow times
    wish_datetimes = \
        [datetime.datetime.combine(
            check_datetime.date() + datetime.timedelta(days=-1),
            wish_times[-1])] + \
        [datetime.datetime.combine(
            check_datetime.date(),
            time) for time in wish_times] + \
        [datetime.datetime.combine(
            check_datetime.date() + datetime.timedelta(days=1),
            wish_times[0])]

    # finding closest datetime and checking if it's time to wish
    for i in range(len(wish_datetimes)):
        if check_datetime >= wish_datetimes[i] and check_datetime < wish_datetimes[i+1]:
            if last_wish > wish_datetimes[i]:
                return False, wish_datetimes[i+1] - check_datetime

    return True, datetime.timedelta(days=0)

def check(
    lang: str,
    player: Player,
    with_save: bool = True
) -> Tuple[bool, str]:
    '''_summary_

    :param Player player: _description_
    :param bool with_save: _description_, defaults to True
    :return Tuple[bool, datetime.timedelta]: _description_
    '''
    now = datetime.datetime.now()
    is_wish, timedelta = wish_time(player, now)

    if is_wish and with_save:
        player.last_wish = now  # save normal wish

    elif player.blessing_of_the_welkin_moon:
        is_wish, moon_timedelta = wish_time(player, now, moon=True)
        timedelta = min(timedelta, moon_timedelta)
        if is_wish and with_save:
            player.moon_last_wish = now  # save moon wish

    time_left = ''
    if timedelta:
        time_left = format_time(lang, timedelta)

    return is_wish, time_left
