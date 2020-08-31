from bot.database.models import Player as PlayerModel
from dataclasses import dataclass


@dataclass
class Player:
    id: int
    balance: int
    xp: int
    level: int
    energy: int

    @classmethod
    async def load(cls, user_id: int, guild_id: int):
        player = (
            await PlayerModel.query.where(PlayerModel.user_id == user_id)
            .where(PlayerModel.guild_id == guild_id)
            .gino.first()
        )
        if player is None:
            player = await PlayerModel.create(user_id=user_id, guild_id=guild_id)
        return Player(
            id=player.id,
            balance=player.balance,
            xp=player.xp,
            level=player.level,
            energy=player.energy,
        )
