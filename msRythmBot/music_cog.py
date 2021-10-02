import asyncio
import inspect
import discord
import pprint
from discord.ext import commands

from youtube_dl import YoutubeDL


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ms = ''

        self.is_playing = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

    def search_youtube(self, item):
        # 'with' means we use it and at the end, we throw away
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %
                                        item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            music_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            music_url = self.music_queue[0][0]['source']
            if self.vc == "" or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
            # else:
            #     self.vc = await self.bot.move_to(self.music_queue[0][1])
            self.ms = ''
            self.ms += (self.music_queue[0][0]['title'])
            # print(type(self.music_queue[0][0]['title']))
            self.music_queue.pop(0)
            # self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command()
    async def p(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send("Connected")
        else:
            song = self.search_youtube(query)
            if type(song) == type(True):
                await ctx.send("Wrong Song,  Need Another")
            else:
                self.music_queue.append([song, voice_channel])
                await ctx.send("Song Added : %s" % song['title'])

                if self.is_playing == False:
                    await self.play_music()

    @commands.command()
    async def q(self, ctx):
        print(self.ms)
        if self.ms == '':
            retval = ""
        else:
            retval = "[Now Playing]: " + self.ms +" \n"
            self.ms=''

        for i in range(0, len(self.music_queue)):
            retval += '['+str(i)+'] : '
            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Not Music in Queue")

    @commands.command()
    async def skip(self, ctx):
        if self.vc != "":
            self.vc.stop()
            await self.play_music()
        # else:

    @commands.command()
    async def bothelp(self, ctx):
        await ctx.send("사용법 \n음악 재생 !p 음악 이름 + 가수; (주의사항: 똥 프로그램이라 음악이름을 상세하게 적어주세요)\n음악 리스트 !q \n음악 넘기기 !skip\n")
