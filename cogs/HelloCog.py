from discord.ext import commands
from discord.ext.commands import Context


class HelloCog(commands.Cog):
    """
    An Example Cog.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def hello(self, ctx: Context):
        """
        Basic Hello command.
        Usage: [p]hello
        """

        # check if subcommand was invoked before executing this command
        if ctx.invoked_subcommand is None:
            sender = ctx.author
            await ctx.send(f"Hello {sender.display_name}")

    @hello.command()
    async def world(self, ctx: Context):
        """
        Basic Hello World subcommand example.
        Usage: [p]hello world
        """
        sender = ctx.author
        await ctx.send(f"Hello World {sender.display_name}")


def setup(bot):
    # registers this cog to the bot
    bot.add_cog(HelloCog(bot))
