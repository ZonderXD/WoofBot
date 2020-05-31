import discord
import asyncio
import datetime
import random as r
import random
import io
import os
import wikipedia
import nekos
import sqlite3
import json
import requests
import time
import sys
import traceback
from mod import *
from discord.ext import commands
from discord.utils import get
from Cybernator import Paginator

bot = commands.Bot(command_prefix='h!')
bot.remove_command('help')

conn = sqlite3.connect("database.sqlite")
cursor = conn.cursor()

@bot.event
async def on_ready():
    print(f'          [Hotel]')
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game('Префикс: h!'))
    print(f"[Hotel] Bot successfully launched!;")
    print(f"[Hotel] Name: [{bot.user}];")
    print(f'[Hotel] ID: [{bot.user.id}]')
    print('[------------------------------]')
    print(f'          [Other]')

@bot.event
async def is_owner(ctx):
    return ctx.author.id == 668325441224048641 or  ctx.author.id == 369499654909591555 # Айди создателя бота

@bot.command()
@commands.check(is_owner)
async def opros(ctx, *, arg):
	await ctx.message.delete()
	embed = discord.Embed(title=f"Опрос:", color = 0x00ffff)
	embed.add_field(name=f'**Вопрос:**', value=f"**{arg}**\n", inline=False)  # Создает строку
	embed.add_field(name=f'**Решение:**', value="**-=-=- Да - 👍 -=-=-\n -=-=- Нет - 👎 -=-=-**\n\n", inline=False)  # Создает строку
	embed.add_field(name=f'**Инфо:**', value="**Голосование будет длиться 1 минуту!**", inline=False)  # Создает строку
	opros = await ctx.send(embed=embed)
	
	await opros.add_reaction("👍")
	await opros.add_reaction("👎")

def random_meme():
    with open('memes_data.txt', 'r') as file:
        memes = file.read().split(',')
    picked_meme = random.choice(memes)
    return picked_meme

@bot.command()
async def cat(ctx):
    meow = random.randint(1, 100000)
    embed = discord.Embed(title='**Вот тебе кот:**' ,colour=0x00ffff)
    embed.set_image(url = f'https://cataas.com/cat?{meow}')
    await ctx.send(embed=embed)

@bot.command()
@commands.check(is_owner)
@commands.cooldown(1, 10, commands.BucketType.user)
async def giveaway( ctx, seconds: int, *, text ):
    def time_end_form( seconds ):
        h = seconds//3600
        m = (seconds - h*3600)//60
        s = seconds%60
        if h < 10:
            h = f"0{h}"
        if m < 10:
            m = f"0{m}"
        if s < 10:
            s = f"0{s}"
        time_reward = f"{h} : {m} : {s}"
        return time_reward

    author = ctx.message.author
    time_end = time_end_form(seconds)
    await ctx.message.delete()
    message = await ctx.send(embed = discord.Embed(
        description = f"**Разыгрывается : `{text}`\nЗавершится через: `{time_end}` \n\nОрганизатор: {author.mention} \nДля участия нажмите на реакцию ниже.**",
        colour = 0x75218f).set_footer(
        text = '𝙀𝙍𝙍𝙊𝙍 ツ#6666 © | Все права защищены',
        icon_url = ctx.message.author.avatar_url))
    await message.add_reaction("🎉")
    while seconds > -1:
        time_end = time_end_form(seconds)
        text_message = discord.Embed(
            description = f"**Разыгрывается: `{text}`\nЗавершится через: `{time_end}` \n\nОрганизатор: {author.mention} \nДля участия нажмите на реакцию ниже.**",
            colour = 0x75218f).set_footer(
            text = '𝙀𝙍𝙍𝙊𝙍 ツ#6666 © | Все права защищены',
            icon_url = ctx.message.author.avatar_url)
        await message.edit(embed = text_message)
        await asyncio.sleep(1)
        seconds -= 1
        if seconds < -1:
            break
    channel = message.channel
    message_id = message.id
    message = await channel.fetch_message(message_id)
    reaction = message.reactions[ 0 ]

    users = await reaction.users().flatten()

    def winners():
        global win

        user_win = random.choice(users)

        if reaction.count == 1:
            win = discord.Embed(
                description = f'**В этом розыгрыше нет победителя!**',
                colour = 0x75218f).set_footer(
                text = '𝙀𝙍𝙍𝙊𝙍 ツ#6666 © | Все права защищены',
                icon_url = ctx.message.author.avatar_url)
        elif str(user_win.id) == str(bot.user.id):
            winners()
        else:
            win = discord.Embed(
                description = f'**Победитель розыгрыша: {user_win.mention}!\nНапишите организатору {author.mention}, чтобы получить награду.**',
                colour = 0x75218f).set_footer(
                text = '𝙀𝙍𝙍𝙊𝙍 ツ#6666 © | Все права защищены',
                icon_url = ctx.message.author.avatar_url)

    winners()
    global win
    await message.edit(embed = win)
    await author.send(embed = discord.Embed(description = f'**Ваш розыгрыш закончился.**',
                                            colour = 0x75218f).set_footer(
        text = '𝙀𝙍𝙍𝙊𝙍 ツ#6666 © | Все права защищены',
        icon_url = ctx.message.author.avatar_url))

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 714560313697239044: # ID Сообщения
        guild = bot.get_guild(payload.guild_id)
        role = None

        if str(payload.emoji) == '✅': # Emoji для реакций
            role = guild.get_role(713846336595689552) # ID Ролей для выдачи

        if role:
            member = guild.get_member(payload.user_id)
            if member:
                await member.add_roles(role)

@bot.event
async def on_voice_state_update(member,before,after):
    if after.channel != None and after.channel.id == 712629884119416944:
        for guild in bot.guilds:
            if guild.id == 696322642747064380:
                mainCategory = discord.utils.get(guild.categories, id=712629625049579561)
                channel2 = await guild.create_voice_channel(name=f"🌄╎{member.display_name}",category=mainCategory, user_limit=1)
                await member.move_to(channel2)
                def check(a,b,c):
                    return len(channel2.members) == 0
                await bot.wait_for('voice_state_update', check=check)
                await channel2.delete()

@bot.command()
async def neko(ctx):
    number = random.randint(1,3)
    if (number == 1): 
        embed = discord.Embed(description = f"{ctx.author.mention} вот тебе аниме гирл:", colour = 0xff0000)
        embed.set_image(url=nekos.img('neko'))
    if (number == 2):
        embed = discord.Embed(description = f"{ctx.author.mention} Вот тебе лисичка:", colour = 0xff0000)
        embed.set_image(url=nekos.img('fox_girl'))
    if (number == 3):
        embed = discord.Embed(description = f"{ctx.author.mention} Вот тебе класик:", colour = 0xff0000)
        embed.set_image(url=nekos.img('avatar'))
    await ctx.send(embed = embed)

@bot.command()
async def meme(ctx):
    emb = discord.Embed(description = f"**Вот тебе мем:**", color = 0xda4a)
    emb.set_image(url= random_meme())
    await ctx.send(embed=emb)

@bot.event
async def on_member_join( member ):
    emb = discord.Embed( description = f"**Приветствую тебя {member.mention}. Ты попал на сервер `{member.guild.name}`. Удачи тебе на сервере! 😜**", color = 0xda4a )
    role = discord.utils.get( member.guild.roles, id = 713034231743381587 ) # Айди роли которая будет выдаватся когда человек зашёл на сервер

    await member.add_roles( role )
    channel = bot.get_channel( 713793981095477248 ) # Айди канала куда будет писатся сообщение
    await channel.send( embed = emb )

@bot.command(aliases=['bot'])
async def botinfo(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Информация о боте **Отель Альтон#2307**.\n Бот был написан специально для проекта **`Отель Альтон`**,\n Подробнее о командах: **h!help`**", color = 0x00ffff)
    embed.add_field(name=f'**Меня создал:**', value="`𝙀𝙍𝙍𝙊𝙍 ツ#6666`(<@668325441224048641>)", inline=False)  # Создает строку
    embed.add_field(name=f'**Лицензия:**', value="LD-v7", inline=False)  # Создает строку
    embed.add_field(name=f'**Я написан на:**', value="Discord.py", inline=False)  # Создает строку
    embed.add_field(name=f'**Версия:**', value="V.3.0.1", inline=False)  # Создает строку
    embed.add_field(name=f'**Патч:**', value="10", inline=False)  # Создает строку
    embed.set_thumbnail( url = bot.user.avatar_url)
    embed.set_footer(text=f"𝙀𝙍𝙍𝙊𝙍 ツ#6666 © | Все права защищены", icon_url='https://cdn.discordapp.com/avatars/668325441224048641/a_57993892db606d5adfacf36b67144222.gif?size=1024') # создаение футера
    await ctx.send(embed=embed)

@bot.command()
@commands.check(is_owner)
async def edit(ctx, message_id: int = None, new_content: str = None):
        message = await ctx.message.channel.fetch_message(message_id)
        
        await message.edit(content = new_content)
        await ctx.message.add_reaction('✅')

@bot.command()
@commands.check(is_owner)
async def emoji(ctx,id:int,reaction:str):
		await ctx.message.delete()
		message = await ctx.message.channel.fetch_message(id)
		await message.add_reaction(reaction)

@bot.command() # Декоратор команды
async def ran_avatar(ctx): # Название команды
    emb = discord.Embed(description= 'Вот подобраная Вам аватарка.', color=0x6fdb9e) # Переменная ембеда и его описание
    emb.set_image(url=nekos.img('avatar')) # Тут мы с помощью новой библиотеки ищем картинку на тему аватар и ставим её в ембед
    await ctx.send(embed=emb)  # Отпрвака ембеда

@bot.command() # Декоратор команды
async def slap(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете ударить сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас ударил(-а) {ctx.message.author.mention}.', color=0x6fdb9e) # Переменная ембеда и описание
        emb.set_image(url=nekos.img('slap')) # Ищем картинку и ставим её в ембед
 
        await ctx.send(embed=emb) # Отпрвака ембед

@bot.command() # Декоратор команды
async def goose(ctx): # Название команды и аргумент
        emb = discord.Embed(description= f'**Вот твой гусь:**', color=0x6fdb9e) # Переменная ембеда и описание
        emb.set_image(url=nekos.img('goose')) # Ищем картинку и ставим её в ембед
 
        await ctx.send(embed=emb) # Отпрвака ембед

@bot.command() # Декоратор команды
async def dog(ctx): # Название команды и аргумент
        emb = discord.Embed(description= f'**Вот твоя собака:**', color=0x6fdb9e) # Переменная ембеда и описание
        emb.set_image(url=nekos.img('woof')) # Ищем картинку и ставим её в ембед
 
        await ctx.send(embed=emb) # Отпрвака ембед

@bot.command() # Декоратор команды
async def hug(ctx, member : discord.Member): # Название команды и аргумент
    if member == ctx.message.author: # Проверка кого упомянули
        await ctx.send('Вы не можете обнять сами себя.')
    else:
        emb = discord.Embed(description= f'{member.mention}, Вас обнял(-а) {ctx.message.author.mention}.', color=0x6fdb9e) # Переменная ембеда и описание
        emb.set_image(url=nekos.img('hug')) # Ищем картинку и ставим её в ембед
 
        await ctx.send(embed=emb) # Отпрвака ембед

@bot.command()
async def kill(ctx, member : discord.Member = None):
	if member == None:
		emb = discord.Embed(description= f'{ctx.message.author.mention} Прыгает с крыши.', color=0x6fdb9e) # Переменная ембеда и описание
		emb.set_image(url='https://pa1.narvii.com/7081/7f5f49cf4e6c0a06614d7cda9bd5954b257a2151r1-500-296_hq.gif')
		
		await ctx.send(embed=emb)
	else:
		emb = discord.Embed(description= f'{member.mention}, Вас убил(-а) {ctx.message.author.mention}.', color=0x6fdb9e) # Переменная ембеда и описание
		emb.set_image(url='https://cdn.discordapp.com/attachments/693515715646324796/707582757144100894/tenor.gif') # Ищем картинку и ставим её в ембед
 	
		await ctx.send(embed=emb) # Отпрвака ембед

@bot.command()
async def password(ctx, lenght: int = None, number: int = None):

    if not lenght or not number:
        await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите длину пароля и количество символов в нем.', color=0x0c0c0c)) 

    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for x in range(number):
        password = ''

        for i in range( lenght ):
            password += random.choice(chars)

        await ctx.author.send(embed = discord.Embed(description = f'**Сгенерированный пароль:\n{password}**', color=0x0c0c0c)) 
        await ctx.send(embed = discord.Embed(description = f'**Пароль успешно отправлен!**', color=0x0c0c0c))
        return

@bot.command()
async def help(ctx):
    embed1 = discord.Embed(title = '⚙ Навигация по командам:\n ❗ Обязательные параметры: `()`\n ❓ Необязательные параметры: `[]`', color=0x6fdb9e )
    embed2 = discord.Embed(title ='💎 Базовые:', description='**``h!user [@user]`` - Узнать информацию о пользователе 🎭\n ``h!server`` - Узнать информацию о сервере 🧿\n `h!bot` - Информация о боте 🤖\n`h!avatar [@user]` - Аватар пользователя 🖼\n `h!suggest (text)` - Предложить идею ✉\n `h!wiki (text)` - Википедия 📖**', color=0x6fdb9e )
    embed3 = discord.Embed(title ='🎉 Весёлости:', description='**``h!ran_color`` - Рандомный цвет в формате HEX 🩸\n ``h!coin`` - Бросить монетку 🌈\n ``h!math (2*2/2+2-2)`` - Решить пример :infinity:\n `h!8ball (question)` - Волшебный шар 🔮\n `h!password (10 10)` - Рандомный пароль 🎩\n `h!meme` - Рандомный мем 🤣**', color=0x6fdb9e)
    embed4 = discord.Embed(title ='💋 Некос:', description='**`h!hug (@user)` - Обнять 😜\n `h!slap (@user)` - Ударить 😡\n `h!ran_avatar` - Рандом. аватар 🤯\n `h!kill [@user]` - Убить 🔪\n `h!dog` - Собака :dog:\n `h!goose` - Гусь :duck:\n `h!cat` - Кот 🐱\n `h!neko` - Рандомная аватарка в стиле аниме ✨**', color=0x6fdb9e)
    embeds = [embed1, embed2, embed3, embed4]
    message = await ctx.send(embed=embed1)
    page = Paginator(bot, message, only=ctx.author, use_more=False, embeds=embeds)
    await page.start()

@bot.command()
async def wiki(ctx, *, text):
    wikipedia.set_lang("ru")
    new_page = wikipedia.page(text)
    summ = wikipedia.summary(text)
    emb = discord.Embed(
        title= new_page.title,
        description= summ,
        color = 0x00ffff
    )
    emb.set_author(name= 'Больше информации тут! Кликай!', url= new_page.url, icon_url= 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png')

    await ctx.send(embed=emb)

@bot.command()
async def user(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.'.format(Member.name), description=f"Участник зашёл на сервер: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
                                                                                      f"**🧬 Имя: `{Member.name}`**\n\n"
                                                                                      f"**⚔ Никнейм: `{Member.nick}`**\n\n"
                                                                                      f"**🌵 Статус: `{Member.status}`**\n\n"
                                                                                      f"**🔑 ID: `{Member.id}`**\n\n"
                                                                                      f"**🌋 Высшая роль: `{Member.top_role}`**\n\n"
                                                                                      f"**🌟 Аккаунт создан: `{Member.created_at.strftime('%A %b %#d, %Y')}`**", 
                                                                                      color=0xff0000, timestamp=ctx.message.created_at)

    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Команда вызвана: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

@bot.command()
async def avatar(ctx, member : discord.Member = None):

    user = ctx.message.author if (member == None) else member

    embed = discord.Embed(title=f'** Аватар `{user}`**', color= 0x0c0c0c)

    embed.set_image(url=user.avatar_url)

    await ctx.send(embed=embed)

@bot.command()
async def coin( ctx ):
    coins = [ 'орел', 'решка' ]
    coins_r = random.choice( coins )
    coin_win = 'орел'

    if coins_r == coin_win:
        await ctx.send(embed = discord.Embed(description= f''':tada: { ctx.message.author.name }, выиграл! 
            Тебе повезло у тебя: ``{ coins_r }``''', color = 0x0c0c0c))

    if coins_r != coin_win:
        await ctx.send(embed = discord.Embed(description= f''':thumbsdown:  { ctx.message.author.name }, проиграл! 
            Тебе не повезло у тебя: ``{ coins_r }``''', color = 0x0c0c0c))

@bot.command()
async def ran_color(ctx):
    clr = (random.randint(0,16777215))
    emb = discord.Embed(
        description= f'Сгенерированый цвет : ``#{hex(clr)[2:]}``',
        colour= clr
    )

    await ctx.send(embed=emb)

@bot.command(name = "8ball")
async def ball(ctx, *, arg):

    message = ['Нет 😑','Да 😎','Возможно 😪','Опредленно нет '] 
    s = random.choice( message )
    await ctx.send(embed = discord.Embed(description = f'**:crystal_ball: Знаки говорят:** {s}', color=0x0c0c0c))
    return

# Работа с ошибками шара

@ball.error 
async def ball_error(ctx, error):

    if isinstance( error, commands.MissingRequiredArgument ): 
        await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите вопрос.', color=0x0c0c0c)) 

@bot.command(aliases = ['count', 'calc', 'вычисли', 'math'])
async def __count(ctx, *, args = None):
    text = ctx.message.content

    if args == None:
        await ctx.send(embed = discord.Embed(description = 'Пожалуйста, укажите выражение для оценки.', color = 0x39d0d6))
    else:
        result = eval(args)
        await ctx.send(embed = discord.Embed(description = f'Результат примера: `{args}`: \n`{result}`', color = 0x39d0d6))

@bot.command()
async def server(ctx):
    members = ctx.guild.members
    online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
    offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
    idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
    dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
    allchannels = len(ctx.guild.channels)
    allvoice = len(ctx.guild.voice_channels)
    alltext = len(ctx.guild.text_channels)
    allroles = len(ctx.guild.roles)
    embed = discord.Embed(title=f"Сервер: `{ctx.guild.name}`", color=0xff0000, timestamp=ctx.message.created_at)
    embed.description=(
        f":timer: **Сервер создали: `{ctx.guild.created_at.strftime('%A, %b %#d %Y')}`**\n\n"
        f":flag_white: **Регион: `{ctx.guild.region}`**\n\n"
        f":cowboy:  **Глава сервера: `{ctx.guild.owner}`**\n\n"
        f":tools: **Ботов на сервере: `{len([m for m in members if m.bot])}`**\n\n"
        f":green_circle: **Онлайн: `{online}`**\n\n"
        f":black_circle: **Оффлайн: `{offline}`**\n\n"
        f":yellow_circle: **Отошли: `{idle}`**\n\n"
        f":red_circle: **Не трогать: `{dnd}`**\n\n"
        f":shield: **Уровень верификации: `{ctx.guild.verification_level}`**\n\n"
        f":musical_keyboard: **Всего каналов: `{allchannels}`**\n\n"
        f":loud_sound: **Голосовых каналов: `{allvoice}`**\n\n"
        f":keyboard: **Текстовых каналов: `{alltext}`**\n\n"
        f":briefcase: **Всего ролей: `{allroles}`**\n\n"
        f":slight_smile: **Людей на сервере: `{ctx.guild.member_count}`**\n\n"
    )

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Информация о сервере: {ctx.guild.name}")
    await ctx.send(embed=embed)

@bot.command()
@commands.check(is_owner)
async def say(ctx, *, arg):
    await ctx.message.delete()
    await ctx.send(embed = discord.Embed(description = f'{arg}', color=0xda4a))

@bot.command()
@commands.check(is_owner)
async def leave(ctx, server_id: int):
    to_leave = bot.get_guild(server_id)

    await ctx.send(embed = discord.Embed(description = f'**Я успешно прекратил обслуживание данного сервера.**', color=0x0c0c0c))
    await to_leave.leave()

@bot.command()
@commands.check(is_owner)
async def servers(ctx):
    description = ' '
    counter = 0
    for guild in bot.guilds:
        counter += 1
        description += f'{counter}) **`{guild.name}`** - **`{len(guild.members)}`** участников. ID: **`{guild.id}`** \n'
        await ctx.send(embed = discord.Embed(title = 'Сервера, на которых я нахожусь', description = description, color = 0x00ffff))

token = os.environ.get("BotToken")
bot.run(str(token))
