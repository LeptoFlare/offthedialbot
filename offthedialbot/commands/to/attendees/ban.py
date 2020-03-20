"""$to attendees ban"""
import discord

from offthedialbot import utils
from . import check_valid_attendee, remove


@utils.deco.require_role("Organiser")
async def main(ctx):
    """Ban an attendee from the tournament."""
    ui: utils.CommandUI = await utils.CommandUI(ctx,
        discord.Embed(
            title="Ban attendees.",
            description="Mention each attendee you want to ban.",
            color=utils.Alert.Style.DANGER))
    reply = await ui.get_valid_message(lambda m: len(m.mentions) == 1,
        {"title": "Invalid Mention", "description": "Make sure to send a **mention** of the attendee."})

    for attendee in reply.mentions:

        # Check to make sure the attendee is valid
        if not (profile := await check_valid_attendee(ctx, attendee, competing=False)):
            continue

        until = await set_ban_length(ui, profile)
        await remove_smashgg(ui, attendee)
        await remove.from_competing(ctx, attendee, profile,
            reason=f"attendee manually banned by {ctx.author.display_name}.")

        # Complete ban
        await utils.Alert(ctx, utils.Alert.Style.SUCCESS,
            title="Ban attendee complete",
            description=f"`{attendee.display_name}` is now banned {f'until `{until} UTC`' if until != True else 'forever'}.")

    await ui.end(None)


async def remove_smashgg(ui, attendee):
    """Remove attendee from smash.gg if applicable."""
    try:
        await remove.from_smashgg(ui, attendee)
    except TypeError:
        pass


async def set_ban_length(ui: utils.CommandUI, profile):
    """Get ban length and set it inside of the profile."""
    ui.embed.description = f"Specify the length of the ban. or enter 'forever' for a permanent ban."
    ui.embed.add_field(name="Supported symbols:", value=utils.time.User.symbols)

    parse = lambda m: utils.time.User.parse(m.content) if m.content != "forever" else True
    reply = await ui.get_valid_message(parse,
        {"title": "Invalid Length", "description": "Please check the `Supported symbols` and make sure your input is correct."})
    until = parse(reply)
    profile.set_banned(until)

    ui.embed.remove_field(0)
    return until
