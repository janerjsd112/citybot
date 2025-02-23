import discord
import json
from discord.ext import commands

# 봇 토큰 입력
TOKEN = 'MTMzMDk0NzU3OTg1NjU1MjExNA.Gkk0fh.pMJ1mD7IDQU3UCvi9gFNqLMov-RsOfJC8in7yo'  # Replace this with your bot's token

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # This intent is necessary to fetch the list of members

# 봇 설정: 접두사를 '!'로 설정
bot = commands.Bot(command_prefix='!', intents=intents)

# 단어 저장 파일
WORDS_FILE = "words.json"

# 단어 파일이 존재하지 않으면 생성
def load_words():
    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_words(words):
    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=4)

# 단어 저장
words = load_words()

# 봇이 준비되었을 때
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="부원서버 참여 "))

# 단어를 가르치는 명령어
@bot.command(name="단어")
async def add_word(ctx, word: str, *, definition: str):
    words[word] = definition
    save_words(words)  # 단어 저장
    await ctx.send(f"단어 `{word}` 가 성공적으로 추가되었습니다! 뜻: {definition}")

# 단어를 설명하는 명령어
@bot.event
async def on_message(message):
    # 봇이 자신의 메시지에 반응하지 않도록
    if message.author == bot.user:
        return

    # "시티야" 뒤에 공백 없이 단어를 찾을 수 있도록 수정
    if message.content.startswith("시티야"):
        word = message.content[3:].strip()  # "시티야" 뒤의 단어를 가져옵니다.
        
        if word in words:
            await message.channel.send(words[word])  # 뜻만 출력
        else:
            await message.channel.send(f"단어 `{word}`는 아직 가르쳐지지 않았습니다. 먼저 `!단어 [단어] [뜻]`으로 가르쳐주세요!")

    # 명령어 처리 (중복 실행 방지)
    await bot.process_commands(message)

# 서버 가이드 명령어
@bot.command(name='가이드')
async def send_server_info(ctx):
    embed = discord.Embed(
        title=f"{ctx.guild.name} 서버 정보",
        description="서버의 기본 정보를 아래에서 확인하세요!",
        color=discord.Color.blue()
    )
    embed.add_field(name="🌐 서버 이름", value=ctx.guild.name, inline=False)
    embed.add_field(name="🌸 서버 아이디", value=ctx.guild.id, inline=False)
    embed.add_field(name="💬 서버 멤버 수", value=ctx.guild.member_count, inline=False)
    embed.add_field(name="📝 서버 설명", value="다양한 친구들을 만나 친목도모 및 단체 이벤트 참여를 하여 서버를 즐겨보시길 바랍니다!", inline=False)
    embed.add_field(name="🦺 서버 문의", value="<@1190259610569936896> / <@1223239237210472458> / <@1271733682247438390> / <@1150740247756414986> / <@868372755261849600> 디엠으로 해주시거나 정해진 채널에 문의하시길 바랍니다", inline=False)
    
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    else:
        embed.add_field(name="⚠️ 서버 아이콘 없음", value="이 서버에는 아이콘이 설정되지 않았습니다.", inline=False)
    
    channel_info = ""
    channel_info += f"https://discordapp.com/channels/1173200911686975608/1267420408643190824 - 본 채널은 주 대화가 이루어지는 공간입니다.\n"
    channel_info += f"https://discordapp.com/channels/1173200911686975608/1248710781873426433 - 중요사항과 가장 많은 공지가 올라오는 곳입니다.\n"
    channel_info += f"https://discordapp.com/channels/1173200911686975608/1267401818447675414 - 관리진의 처벌에 불만이 있을시 재판을 요구할 수 있습니다.\n"
    
    embed.add_field(name="📌 대표 채널", value=channel_info, inline=False)

    try:
        await ctx.author.send(embed=embed)
        await ctx.send(f"{ctx.author.mention}님, 서버 정보를 DM으로 보냈습니다!")
    except discord.errors.Forbidden:
        await ctx.send(f"{ctx.author.mention}님, DM을 받을 수 없습니다. DM 설정을 확인해주세요.")

# 모두에게 DM 보내기 (관리자 권한만)
@bot.command(name='모두에게DM')
@commands.has_permissions(administrator=True)  # 관리자 권한만 허용
async def send_dm_to_all(ctx, *, message: str):
    sent_count = 0
    failed_count = 0

    for member in ctx.guild.members:
        if member.bot:  # 봇에게는 메시지를 보내지 않음
            continue
        try:
            await member.send(message)
            sent_count += 1
        except discord.errors.Forbidden:
            failed_count += 1
    
    await ctx.send(f"{sent_count}명의 사용자에게 DM을 성공적으로 보냈습니다. {failed_count}명에게는 DM을 보낼 수 없습니다.")

# 관리자 권한이 없는 경우 알림 추가
@send_dm_to_all.error
async def send_dm_to_all_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{ctx.author.mention}님, 이 명령어는 관리자 권한이 필요합니다!")

# 봇 실행
bot.run(TOKEN)











