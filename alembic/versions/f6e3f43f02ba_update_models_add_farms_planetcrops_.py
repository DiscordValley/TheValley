"""Update models, Add Farms, PlanetCrops, Players, Profiles

Revision ID: f6e3f43f02ba
Revises: 81d196a1e6cc
Create Date: 2020-08-31 21:14:42.744836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f6e3f43f02ba"
down_revision = "81d196a1e6cc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "players",
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("user_id", sa.BIGINT(), nullable=True),
        sa.Column("guild_id", sa.BIGINT(), nullable=True),
        sa.Column("balance", sa.Integer(), nullable=True),
        sa.Column("xp", sa.Integer(), nullable=True),
        sa.Column("level", sa.Integer(), nullable=True),
        sa.Column("energy", sa.Integer(), nullable=True),
        sa.Column("last_visit", sa.DateTime(), nullable=True),
        sa.Column("allow_notification", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_players")),
        sa.UniqueConstraint("user_id", "guild_id", name="guild_user"),
    )
    op.create_table(
        "farms",
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("player_id", sa.BIGINT(), nullable=True),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("size", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["player_id"], ["players.id"], name=op.f("fk_farms_player_id_players")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_farms")),
    )
    op.create_table(
        "profiles",
        sa.Column("id", sa.BIGINT(), nullable=True),
        sa.Column("player_id", sa.BIGINT(), nullable=True),
        sa.Column("badge_id", sa.BIGINT(), nullable=True),
        sa.ForeignKeyConstraint(
            ["player_id"], ["players.id"], name=op.f("fk_profiles_player_id_players")
        ),
    )
    op.create_table(
        "planted_crops",
        sa.Column("id", sa.BIGINT(), nullable=False),
        sa.Column("farm_id", sa.BIGINT(), nullable=True),
        sa.Column("crop_id", sa.BIGINT(), nullable=True),
        sa.Column("planted_at", sa.DateTime(), nullable=True),
        sa.Column("coord_column", sa.Integer(), nullable=True),
        sa.Column("coord_row", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["farm_id"], ["farms.id"], name=op.f("fk_planted_crops_farm_id_farms")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_planted_crops")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("planted_crops")
    op.drop_table("profiles")
    op.drop_table("farms")
    op.drop_table("players")
    # ### end Alembic commands ###
