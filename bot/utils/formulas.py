import ujson
import random
import math

from bot.game.player import PlayerModel


with open("levels.json", "r") as f:
    LEVELS = ujson.load(f)


def level_energy_usage(level: int):
    return 1 / 10 * pow((1 + 1 / 50), level + 40) + 10


def energy_increase(player_level: int):
    if player_level == 1:
        # Prevent issues with nullification and log(1)
        player_level = 2

    return abs(
        level_energy_usage(player_level) * ((player_level / 2) * math.log(player_level))
    )


def plant_tier_formula(tier: int, modifier: float):
    return 10 * pow(1.1, tier + 10 - modifier) - abs(2 * math.log(tier * 2) + 15)


def plant_stage_formula(stage: int, modifier: float):
    return 5 * pow(1.1, stage + 10 - modifier) + 8


def xp_formula(player_db: PlayerModel, modifier: float):
    if player_db.level > 4:
        xp = player_db.xp + abs(
            int(
                (
                    (
                        (
                            1
                            * random.randint(1, 10)
                            * abs(player_db.level - (player_db.level * 0.4))
                        )
                        / (5 * 1)
                    )
                    * (
                        (
                            pow(
                                (
                                    (2 * abs(player_db.level - (player_db.level * 0.4)))
                                    + 10
                                ),
                                2.5,
                            )
                            / pow(
                                (
                                    abs(player_db.level - (player_db.level * 0.4))
                                    + player_db.level
                                    + 10
                                ),
                                2.5,
                            )
                        )
                        + 1
                    )
                    * modifier
                )
            )
        )
    else:
        xp = player_db.xp + abs(random.randint(1, 5))
    return xp
