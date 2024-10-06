from collections import OrderedDict

from .command import Command, CommandException
from ..util import Platform, DocSection

@Command.register()
class SetPronounCommand(Command):
    """
    Sets your pronouns to one of the valid options.
    """
    aliases = ("setpronouns", "setpronoun")
    supported_platforms = (Platform.DISCORD, Platform.TWITCH)
    usage = "setpronouns <pronouns>"
    section = DocSection.USER

    def execute(self, pronoun):
        # needs the same keys as PRONOUN_CHOICES in models/users.py
        pronoun_map = OrderedDict([
            ("he", ["him", "his", "he/him", "he/him/his"]),
            ("she", ["her", "hers", "she/her", "she/her/hers"]),
            ("they", ["theirs", "they/them", "they/them/theirs"]),
            ("he/they", ["ht"]),
            ("they/he", ["th"]),
            ("she/they", ["st"]),
            ("they/she", ["ts"]),
            ("it", ["its", "it/its"]),
            ("xe", ["xem", "xir", "xe/xem", "xe/xem/xir"]),
            ("any", ["any/all"]),
            ("ask", []),
            ("none", []),
        ])

        for key, aliases in pronoun_map.items():
            if pronoun == key or pronoun in aliases:
                if self.context.user.set_pronouns(key):
                    self.send_message("Your pronouns have been set to {np}!".format(
                        np=(self.context.user.get_pronouns_display() or "none").lower()
                    ))
                else:
                    raise CommandException("Error setting pronouns :(")
                return

        pronoun_list = ", ".join(pronoun_map.keys())
        raise CommandException(f"Invalid pronoun option. Choose one of: {pronoun_list}")

@Command.register()
class GetPronounCommand(Command):
    """
    Outputs the specified user's pronouns, or your own if no argument is
    provided.
    """
    aliases = ("pronouns", "pronoun", "getpronouns", "getpronoun")
    supported_platforms = (Platform.DISCORD, Platform.TWITCH)
    usage = "pronouns [username] (default username you)"
    section = DocSection.USER

    def execute(self, *username):
        username = username[0] if len(username) == 1 else self.context.args_string
        platform_user = (self.platform_user_from_username(username) if username
                         else self.context.platform_user)
        user = platform_user.user if platform_user else None

        username = self.context.display_name(user)
        pronouns = user.get_pronouns_display() or "not set"
        pronouns = pronouns.lower()
        self.send_message(f"{username}'s pronouns are {pronouns}")
