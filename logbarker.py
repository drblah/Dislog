import discord
import subprocess
import select
import asyncio

class LogBarker(discord.Client):
    def __init__(self, files, channelid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channelid = int(channelid)
        self.files = files
        self.bg_task = self.loop.create_task(self.checkLog_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def checkLog_task(self):
        await self.wait_until_ready()
        
        print("Monitoring the following files: ", self.files)

        fd_list = []
        process_list = []

        for f in self.files:
            fd_list.append(
                subprocess.Popen(['tail','-n0','-f',f],\
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            )

            p = select.poll()
            p.register(fd_list[-1].stdout)
            process_list.append(
                p
            )

        channel = self.get_channel(self.channelid) # channel ID goes here
        while not self.is_closed():
            for fd, proc in zip(fd_list, process_list):
                if proc.poll(1):
                    await channel.send(fd.stdout.readline().decode("utf-8"))
            await asyncio.sleep(1) # task runs every n seconds
