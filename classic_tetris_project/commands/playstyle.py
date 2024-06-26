from .command import Command, CommandException

@Command.register("playstyle", usage="!playstyle [username]")
class GetPlaystyleCommand(Command):
    def execute(self, *username):
        username = username[0] if len(username) == 1 else self.context.args_string
        platform_user = (self.platform_user_from_username(username) if username
                         else self.context.platform_user)
        user = platform_user.user if platform_user else None

        if user and user.playstyle:
            self.send_message("{name}'s playstyle is {style}!".format(
                name=self.context.display_name(platform_user),
                style=user.get_playstyle_display()
            ))
        else:
            self.send_message("User has not set a playstyle.")

@Command.register("setplaystyle", "setstyle",
                  usage="setplaystyle <DAS|Hypertap|Hybrid|Roll>")
class SetPlaystyleCommand(Command):
    def execute(self, style):
        if self.context.user.set_playstyle(style):
            self.send_message(f"Your playstyle is now {self.context.user.get_playstyle_display()}!")
        else:
            raise CommandException("Invalid playstyle. Valid playstyles: DAS, Hypertap, Hybrid, Roll.")
