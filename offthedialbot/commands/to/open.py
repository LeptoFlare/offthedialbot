"""$to open"""
import discord

from offthedialbot import utils


@utils.deco.require_role("Organiser")
@utils.deco.tourney(None)
async def main(ctx):
    """Open registration for a new tournament!"""
    ui: utils.CommandUI = await utils.CommandUI(ctx,
        discord.Embed(title="Opening registration for a new tournament...", color=utils.colors.COMPETING))

    # Steps
    link = await get_tourney_link(ui)
    rules = await get_rules_link(ui)
    utils.dbh.new_tourney(link, rules)

    await ui.end(True)


async def get_tourney_link(ui):
    """Set the smash.gg link for the next tournament."""
    ui.embed.description = "Enter the new link to the tournament. (https://smash.gg/slug)"
    reply = await ui.get_reply()
    return reply.content


async def get_rules_link(ui):
    """Set the rules for the next tournament."""
    ui.embed.description = "Enter the link of the rules to the tournament. (https://docs.google.com/document/d/rules/edit?usp=sharing)"
    reply = await ui.get_reply()
    return reply.content
