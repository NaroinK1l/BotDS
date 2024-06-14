import asyncio
from database import exp

class AutoSave:
    def __init__(self, client):
        self.client = client

    async def start(self):
        while True:
            await self.autosave_data()
            await asyncio.sleep(10800)  # 3 hours

    async def autosave_data(self):
        for user_id in self.client.exp.keys():
            exp.update_user_exp(user_id, self.client.exp[user_id])
            exp.update_user_level(user_id, self.client.levels[user_id])
        print("Data has been autosaved.")

async def main(client):
    autosave = AutoSave(client)
    await autosave.start()
