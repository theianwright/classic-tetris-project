from .. import discord

from .command import Command, CommandException
from ..countries import countries

@Command.register_discord("profile",
                  usage="profile [username] (default username you)")
class ProfileCommand(Command):
    def execute(self, *username):
        username = username[0] if len(username) == 1 else self.context.args_string
        if username and not self.platform_user_from_username(username):
            raise CommandException("Specified user has no profile.")

        user = (self.platform_user_from_username(username).user if username
                         else self.context.platform_user.user)

        if not user:
            raise CommandException("Invalid specified user.")

        if user.preferred_name:
            name = user.preferred_name
        else:
            name = discord.get_guild().get_member(int(user.discord_user.discord_id)).display_name

        ntsc_pb = user.ntsc_pb or "Not set"
        pal_pb = user.pal_pb or "Not set"
        country = countries[user.country] if user.country else "Not set"

        if hasattr(user, "twitch_user"):
            twitch_channel = f"https://www.twitch.tv/{user.twitch_user.username}"
        else:
            twitch_channel = "Not set"


        self.send_message(
            ("**{name}'s profile:**\n\n"
             "    **Personal bests:**\n"
             "        NTSC: {ntsc_pb}\n"
             "        PAL: {pal_pb}\n"
             "    **Country:** {country}\n"
             "    **Twitch:** {twitch_channel}"
             ).format(
                 name=name,
                 ntsc_pb=ntsc_pb,
                 pal_pb=pal_pb,
                 country=country,
                 twitch_channel=twitch_channel
            )
        )
