from bot.database.models import Farm as FarmModel


class Farm:
    def __init__(self, farm_model: FarmModel):
        self.model = farm_model

    @classmethod
    async def load(cls, user_id: int):
        farm = await FarmModel.get(user_id)
        if farm is None:
            farm = await FarmModel.create(user_id=user_id)
        return Farm(farm_model=farm)
