from discord.ext import commands
from discord import User, Member

from utils import Embed

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from utils.stats import Stats

@commands.command()
async def profile(ctx: commands.Context, user: Union[User, Member] = commands.Author):
    stats: "Stats" = ctx.bot.stats

    p = await stats.get_stats(user.id)
    embed = Embed()
    embed.title = f"{user.display_name}'s profile:"
    embed.set_thumbnail(url=user.display_avatar)
    if p == None:
        embed.add_field(name="Gambling:", value="Haven't gambled yet, care to try your luck? 🤑")
    else:
        net = p['amnt_won'] - p['amnt_lost']
        if net < 0:
            net = f"-${abs(net):,}"
        else:
            net = f" ${net:,}"

        embed.add_field(
            name="Gambling:",
            value=f"Games played: {p['games_played']:,}\n" +
            f"`Won {(p['games_won']/p['games_played']*100)//1}%`\n\n" +

            f"Money gambled: ${p['amnt_played']:,}\n" +
            f"`Profit: ${p['amnt_won']:,}`\n`Loss:   ${p['amnt_lost']:,}`\n`Net:   {net}`"
            )
        
    await ctx.reply(embed=embed)

async def setup(bot: commands.Bot):
    bot.add_command(profile)