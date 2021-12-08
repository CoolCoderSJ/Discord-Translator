import keep_alive
import discord
import os
import time
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
from easypydb import DB
import requests, json
from googletrans import Translator
translator = Translator()
translator.raise_Exception = True

db = DB("database", os.environ['DB_TOKEN'])
db.autosave = True
db.autoload = True

client = discord.Client()

client = commands.Bot(command_prefix = '>')

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese-s',
    'zh-tw': 'chinese-t',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'
}

@client.event
async def on_ready():
    print("bot online") 


@client.event
async def on_message(message):
	await client.process_commands(message)
	for key in db.data.keys():
		if str(message.channel.id) in key and message.author.name != "LangSupport":
			print("REE")
			data = db[key]
			print(data, message.channel.id)
			dests = []

			for eachchannel in data['info']:
				print(eachchannel, message.channel.id)
				if str(message.channel.id) == str(eachchannel):
					source = data['info'][eachchannel]
					del data['info'][eachchannel]
					break
			print("INFO" + str(data['info']))
			for eachchannel in data['info']:
				channel = client.get_channel(int(eachchannel))
				dest = data['info'][eachchannel]

				# url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source}&tl={dest}&dt=t&q={message.content}"
				# response = requests.get(url)
				# print(response.text)
				# translated_text = ""
				# for text in json.loads(response.text)[0]:
				# 	translated_text += text[0]
				content = message.content
				if "```" in message.content:
					clist = content.split("```")
					alist = {}
					x = 1
					y = 1
					for item in clist:
						if x//2:
							alist[item] = y
							clist.remove(item)
						x += 1
						y += 1
					print(clist)
					print(alist)
					for item in alist:
						print(f"```{item}```")
						content = content.replace(f"```{item}```", f"__{alist[item]}__")
					print(content)
					print("\n\n")
					text = translator.translate(content, src=source, dest=dest)
					text = text.text
					print(text)
					for item in alist:
						text = text.replace(f"__{alist[item]}__", f"```{item}```")
				


				else:
					try:
						text = translator.translate(content, src=source, dest=dest)
						text = text.text
					except Exception as err:
						text = f"ERROR OCCURED, {err}"
				await channel.send(f"` {str(message.author)} ` - {text}")

	

@client.command()
async def support(ctx, *, langs):
	if ctx.author.id != 744921397582888991:
		return "This server has been restricted to owner only to help prevent spam."
	if len(langs.split(" ")) > 50:
		await ctx.send("You have provided more than 50 languages. Some of these languages will not be used because of Discord Limitations.")
	langstuff = {}
	x = 1
	for lang in langs.split(" "):
		if x > 49:
			break
		print(lang)
		for language in LANGUAGES:
			if LANGUAGES[language] == lang:
				orig1 = lang
				lang1 = language
				langstuff[lang1] = orig1
				break
		if lang not in LANGUAGES.values():
			await ctx.send("A Language provided was not a recognized language")
			return
		x += 1
	
	guild = client.get_guild(ctx.guild.id)
	count = len(db.data) + 1
	category = await guild.create_category(f'SUPPORT ID {count}')
	chnls = []
	for lang in langstuff:
		chnl = await category.create_text_channel(langstuff[lang])
		chnls.append(chnl.id)
	
	querystring = ""
	for id in chnls:
		querystring += str(id)
		if chnls[chnls.index(id)] != chnls[-1]:
			querystring += " "

	langstring = ""
	for lang in langstuff:
		langstring += lang + " "

	langlist = []
	for lang in langstuff:
		langlist.append(lang)

	info = {}
	for id in chnls:
		info[id] = langlist[chnls.index(id)]

	db[querystring] = {
		"catid": category.id,
		"info": info
	}

	chnlstuff = ""
	for id in chnls:
		chnlstuff += f"<#{id}>"
		
	await ctx.send(f"Support Service Started, {chnlstuff}")

@client.command()
async def stop(ctx, catid=None):
	if catid:
		category = ctx.guild.get_channel(int(catid))
		for channel in category.channels:
			chnl = client.get_channel(channel.id)
			await chnl.delete()
		await category.delete()

	for key in db.data.keys():
		if str(ctx.channel.id) in key:
				category = ctx.guild.get_channel(db[key]['catid'])
				for channel in category.channels:
					chnl = client.get_channel(channel.id)
					await chnl.delete()
				await category.delete()
				del db[key]
				break

@client.command()
async def langs(ctx):
	desc = ""
	for lang in LANGUAGES.values():
		desc += lang + "\n"
	embed = discord.Embed(title="SUPPORTED LANGUAGES", description=desc)
	await ctx.send(embed=embed)

@client.command()
async def cease_all_support(ctx):
	if ctx.author.id == 744921397582888991:
		db.data = {}
		await ctx.send("DB Nuked.")

@client.command()
async def detect(ctx, *, message):
	text = translator.detect(message)
	lang = text.lang
	for key in LANGUAGES.keys():
		if lang == key:
			lang = str(LANGUAGES[key]).title()	
	confidence = text.confidence
	await ctx.send(embed=discord.Embed(title=lang, description=f"CONFIDENCE LEVEL: {confidence}"))
	

keep_alive.keep_alive()
client.run(os.getenv("TOKEN"))
