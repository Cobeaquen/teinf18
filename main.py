import asyncio
from threading import Thread
import discord
import datetime
from datetime import date
from datetime import timedelta
import schedule


def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.datetime.now().time()

    return check_time >= begin_time and check_time <= end_time


class Lektion:
    def __init__(self, name, weekday, start, end, call: str, help_call=''):
        self.name = name
        self.start = start
        self.end = end
        self.weekday = weekday
        self.call = call
        self.help_call = help_call

    def __str__(self):
        return self.name

    def is_going_on(self, time):
        return is_time_between(self.start, self.end, time)

    def get_duration(self, time):
        return 'från *{0}* till *{1}*'.format(self.start, self.end) # str(datetime.datetime.strptime(str(self.end), '%H:%M:%S') - datetime.datetime.strptime(str(time), '%H:%M:%S')))


mon1 = Lektion('Historia', 0, datetime.time(8), datetime.time(9, 10), 'https://meet.google.com/fmk-ikqy-nib', 'https://meet.google.com/epx-kdpa-wve')
mon2 = Lektion('Matematik', 0, datetime.time(9, 20), datetime.time(12), 'https://meet.google.com/pae-cixr-idt')
mon3 = Lektion('Webbutveckling', 0, datetime.time(13), datetime.time(15, 40), 'https://meet.google.com/gqa-hhdr-edx')

tue1 = Lektion('Svenska', 1, datetime.time(9, 20), datetime.time(12), 'Finns inget för tillfället')
tue2 = Lektion('Dator- och nätverksteknik', 1, datetime.time(13), datetime.time(15, 40), 'Microsoft Teams')

wed1 = Lektion('Webbutveckling', 2, datetime.time(9, 20), datetime.time(12), 'https://meet.google.com/gqa-hhdr-edx')
wed2 = Lektion('Programmering', 2, datetime.time(13), datetime.time(15, 40), 'Microsoft Teams')

thu1 = Lektion('Entreprenörskap', 3, datetime.time(9, 20), datetime.time(12), 'Finns inget för tillfället')
thu2 = Lektion('Mentors-/resurstid', 3, datetime.time(13), datetime.time(15), 'Microsoft Teams?')

fri1 = Lektion('Matematik', 4, datetime.time(8), datetime.time(9, 10), 'https://meet.google.com/pae-cixr-idt')
fri2 = Lektion('Fysik', 4, datetime.time(9, 20), datetime.time(12), 'https://meet.google.com/pqs-oqdp-xmb', 'https://meet.google.com/zgg-crru-ufr')
fri3 = Lektion('Engelska', 4, datetime.time(13), datetime.time(15, 40), 'https://meet.google.com/jmz-qytb-mma')

mon_lek = [mon1, mon2, mon3]
tue_lek = [tue1, tue2]
wed_lek = [wed1, wed2]
thu_lek = [thu1, thu2]
fri_lek = [fri1, fri2, fri3]

lektioner = [mon_lek, tue_lek, wed_lek, thu_lek, fri_lek]

weekdays = ("Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag")


def get_all_lektioner(weekday: int):
    return lektioner[weekday]


def get_lektion(weekday: int, time=None):
    today = get_all_lektioner(weekday)

    time = time or datetime.datetime.now().time()

    for l in today:
        if l.is_going_on(time):
            return l

    return None


async def remind():
    time = datetime.datetime.now().time()
    time2 = datetime.datetime.combine(date.today(), time) + datetime.timedelta(minutes=5)
    lektion = get_lektion(time2.weekday(), time2.time())

    embed = discord.Embed(title=str(lektion), description="**Börjar om 5 minuter**", color=0x00ff00)
    if lektion.call.startswith('http'):
        embed.url = lektion.call

    embed.add_field(name="Pågår", value='{0} - {1}'.format(lektion.start, lektion.end), inline=False)
    embed.add_field(name="Klassrum", value=lektion.call, inline=False)
    if lektion.help_call:
        embed.add_field(name="Hjälpklassrum", value=lektion.help_call, inline=False)

    await channel.send('@everyone', embed=embed)

    #print('Pågående: **{0}** {1}'.format(str(lektion), lektion.get_duration(time)))                                     # change time here
    #await channel.send('@everyone Startar om 5 minuter: **{0}** - {1}'.format(str(lektion), lektion.get_duration(time)))


def remind_callback():
    client.loop.create_task(remind())
    return schedule.CancelJob


def get_weekday(time: datetime.datetime):
    return time.strftime('%A')


def timedelta_to_time(timedelta: datetime.timedelta):
    seconds = timedelta.total_seconds()
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    return datetime.time(hours, minutes, seconds)


def setup_schedule():
    for m in lektioner[0]:  # Lektioner på måndag
        time = datetime.datetime.combine(date.today(), m.start) - datetime.datetime.combine(date.today(), datetime.time(minute=5))
        schedule.every().monday.at(str(timedelta_to_time(time))).do(remind_callback)
    for t in lektioner[1]:  # Lektioner på tisdag
        time = datetime.datetime.combine(date.today(), t.start) - datetime.datetime.combine(date.today(), datetime.time(minute=5))
        schedule.every().monday.at(str(timedelta_to_time(time))).do(remind_callback)
    for o in lektioner[2]:  # Lektioner på onsdag
        time = datetime.datetime.combine(date.today(), o.start) - datetime.datetime.combine(date.today(), datetime.time(minute=5))
        schedule.every().wednesday.at(str(timedelta_to_time(time))).do(remind_callback)
    for to in lektioner[3]:  # Lektioner på torsdag
        time = datetime.datetime.combine(date.today(), to.start) - datetime.datetime.combine(date.today(), datetime.time(minute=5))
        schedule.every().thursday.at(str(timedelta_to_time(time))).do(remind_callback)
    for f in lektioner[4]:  # Lektioner på fredag
        time = datetime.datetime.combine(date.today(), f.start) - datetime.datetime.combine(date.today(), datetime.time(minute=5))
        schedule.every().friday.at(str(timedelta_to_time(time))).do(remind_callback)


class Teinf(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user.name)

        global guild
        guild = self.get_guild(426375993356451851)
        global channel
        channel = self.get_channel(485170507377803266) # TEINF18A official server                                       #635883291840348161)

        lektion = lektioner[0][0]

    async def on_message(self, message):
        if message.author == client.user or message.channel != channel:
            return

        time = datetime.datetime.now()

        if message.content.startswith('lektion'):
            lektion = get_lektion(time.weekday(), time.time())
            if lektion is None:                                                                                         # få nästa lektion
                for i in lektioner[time.weekday()]:
                    if time.time() < i.start:
                        lektion = i
                        break
                if lektion is not None:
                    await channel.send('Nästa lektion är **{0}** - pågår {1}'.format(str(lektion), lektion.get_duration(time.time())))
                    return
                else:
                    await channel.send('**Inga fler lektioner idag**')
                    return

            await channel.send('Pågående: **{0}** - {1}'.format(str(lektion), lektion.get_duration(time.time())))

        elif message.content.startswith('schema'):

            parts = message.content.split()

            msg = ''

            if len(parts) > 1:
                day = parts[1].lower()
                if day == 'måndag':
                    msg = '**{0}**:\n'.format(weekdays[0])
                    for lek in lektioner[0]:
                        msg += '**{0}** {1}\n'.format(str(lek), lek.get_duration(time.time()))
                elif day == 'tisdag':
                    msg = '**{0}**:\n'.format(weekdays[1])
                    for lek in lektioner[1]:
                        msg += '**{0}** {1}\n'.format(str(lek), lek.get_duration(time.time()))
                elif day == 'onsdag':
                    msg = '**{0}**:\n'.format(weekdays[2])
                    for lek in lektioner[2]:
                        msg += '**{0}** {1}\n'.format(str(lek), lek.get_duration(time.time()))
                elif day == 'torsdag':
                    msg = '**{0}**:\n'.format(weekdays[3])
                    for lek in lektioner[3]:
                        msg += '**{0}** {1}\n'.format(str(lek), lek.get_duration(time.time()))
                elif day == 'fredag':
                    msg = '**{0}**:\n'.format(weekdays[4])
                    for lek in lektioner[4]:
                        msg += '**{0}** {1}\n'.format(str(lek), lek.get_duration(time.time()))

                if msg:
                    await channel.send(msg)
                else:
                    await channel.send('INGEN DAG SOM HETER SÅ DUMHUVUD :man_facepalming: ')
                return

            snd = '---------------------------------------------------------\n'
            for day in lektioner:
                snd += '**{0}**:\n'.format(weekdays[day[0].weekday])
                for lek in day:
                    snd += '**{0}** {1}\n'.format(str(lek), lek.get_duration(time.time()))
                snd += '---------------------------------------------------------\n'

            print(snd)
            await channel.send(snd)

        elif message.content.startswith('-hjälp'):
            await message.channel.send('**lektion** - få pågående lektion. Om ingen, nästa under samma dag\n'
                                       '**schema** *dag (valfri)* - visar schemat för en viss dag (om inte dag anges visas hela veckans schema). Exempel: **schema tisdag**')

setup_schedule()
client = Teinf()
schedule.run_continuously()
print(schedule.next_run())

client.run('NjkwNTU1MTA4NDkyMzEyNjc4.XnTHmQ.O8g1b3KQfxtOQC95tw4w9N-2yoE')