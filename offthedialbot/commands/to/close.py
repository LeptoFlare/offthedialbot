"""$to close"""
import discord

from offthedialbot import utils
from .attendees import export


@utils.deco.to_only
@utils.deco.tourney(True)
async def main(ctx):
    """Close registration for the tournament."""
    ui: utils.CommandUI = await utils.CommandUI(ctx, discord.Embed(title="Closing registration for the tournament...", color=utils.colors.Roles.COMPETING))

    # Steps
    utils.dbh.set_tourney_reg(False)
    await export.export_profiles(ui, {"meta.competing": True})