import discord
from discord.ext import commands


FARMLAND_NOT_FOUND = discord.Embed(
    description="The farmland specified was not recognized. Please try again."
)


class Farming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{type(self).__name__} Cog ready.')

    @commands.command()
    async def harvest(self, ctx, *args):
        """
        *Harvest your crops.*
        Example:
            {prefix}harvest <crops>
        <crops> is optional, and can also be multiple arguments.
        Rows are enumerated starting at '1'.
        Columns are labeled starting at 'a'.
        Example with 0's instead of farmland:
           a   b   c
        1  0   0   0
        2  0   0   0
        3  0   0   0
        <crops> can be a row, column or a specific crop.
        Specific crop is specified by row number followed by column label.
        (for example a1 for the top left crop.)
        If <crops> is not specified, all crops will be harvested.
        """
        plot_template = [[0, 0, 0], [0, 0, 0], [0, 0, 0],
                         [0, 0, 0], [0, 0, 0], [0, 0, 0],
                         [0, 0, 0], [0, 0, 0], [0, 0, 0],
                         [0, 0, 0], [0, 0, 0]]
        if args:
            for arg in args:
                if len(arg) == 1:
                    try:
                        uni_value = ord(arg.lower())
                    except TypeError:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                        return
                    if uni_value != 0:
                        if 48 < uni_value < 58:
                            for i in range(0, len(plot_template[int(arg)-1])):
                                plot_template[int(arg) - 1][i] = 1
                        elif 96 < uni_value < 123:
                            column_num = uni_value - 97
                            for row in plot_template:
                                row[column_num] = 1
                        else:
                            await ctx.send(embed=FARMLAND_NOT_FOUND)
                            return
                elif len(arg) == 2:
                    try:
                        uni_value1 = ord(arg[0].lower())
                        uni_value2 = ord(arg[1].lower())
                    except TypeError:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                        return
                    if (48 < uni_value1 < 58) or (96 < uni_value1 < 123):
                        if (48 < uni_value2 < 58) or (96 < uni_value2 < 123):
                            n = True if 48 < uni_value1 < 58 else False
                            m = True if 48 < uni_value2 < 58 else False
                            if n is not m:
                                if n:
                                    plot_template[uni_value1 - 49][uni_value2 - 97] = 1
                                else:
                                    plot_template[uni_value1 - 97][uni_value2 - 49] = 1
                            elif n and m:
                                for i in range(0, len(plot_template[int(arg) - 1])):
                                    plot_template[int(arg) - 1][i] = 1
                            else:
                                await ctx.send(embed=FARMLAND_NOT_FOUND)
                                return
                        else:
                            await ctx.send(embed=FARMLAND_NOT_FOUND)
                            return
                    else:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                        return
                elif len(arg) == 3:
                    uni_value1 = 0
                    uni_value2 = 0
                    uni_value3 = 0
                    try:
                        uni_value1 = ord(arg[0].lower())
                        uni_value2 = ord(arg[1].lower())
                        uni_value3 = ord(arg[2].lower())
                    except TypeError:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                    if (48 < uni_value1 < 58) and (48 < uni_value2 < 58) and (96 < uni_value3 < 123):
                        plot_template[int(arg[:2])-1][uni_value3 - 97] = 1
                    elif (96 < uni_value1 < 123) and (48 < uni_value2 < 58) and (48 < uni_value3 < 58):
                        plot_template[int(arg[1:3])-1][uni_value1 - 97] = 1
                    else:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                else:
                    await ctx.send(embed=FARMLAND_NOT_FOUND)
                    return
        else:
            for row in plot_template:
                for i in range(0, len(row)):
                    row[i] = 1             # Should be function which harvests a single farmland.
        for row in plot_template:
            print(row)

    @commands.command()
    async def water(self, ctx, *args):
        """
        *Water your crops.*
        Example:
            {prefix}water <crops>
        <crops> is optional, and can also be multiple arguments.
        Rows are enumerated starting at '1'.
        Columns are labeled starting at 'a'.
        Example with 0's instead of farmland:
           a   b   c
        1  0   0   0
        2  0   0   0
        3  0   0   0
        <crops> can be a row, column or a specific crop.
        Specific crop is specified by row number followed by column label.
        (for example a1 for the top left crop.)
        If <crops> is not specified, all crops will be watered.
        """

        plot_template = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                         [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        if args:
            for arg in args:
                if len(arg) == 1:
                    try:
                        uni_value = ord(arg.lower())
                    except TypeError:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                        return
                    if uni_value != 0:
                        if 48 < uni_value < 58:
                            for i in range(0, len(plot_template[int(arg) - 1])):
                                plot_template[int(arg) - 1][i] = 1
                        elif 96 < uni_value < 123:
                            column_num = uni_value - 97
                            for row in plot_template:
                                row[column_num] = 1
                        else:
                            await ctx.send(embed=FARMLAND_NOT_FOUND)
                            return
                elif len(arg) == 2:
                    try:
                        uni_value1 = ord(arg[0].lower())
                        uni_value2 = ord(arg[1].lower())
                    except TypeError:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                        return
                    if (48 < uni_value1 < 58) or (96 < uni_value1 < 123):
                        if (48 < uni_value2 < 58) or (96 < uni_value2 < 123):
                            n = True if 48 < uni_value1 < 58 else False
                            m = True if 48 < uni_value2 < 58 else False
                            if n is not m:
                                if n:
                                    plot_template[uni_value1 - 49][uni_value2 - 97] = 1
                                else:
                                    plot_template[uni_value1 - 97][uni_value2 - 49] = 1
                            elif n and m:
                                for i in range(0, len(plot_template[int(arg) - 1])):
                                    plot_template[int(arg) - 1][i] = 1
                            else:
                                await ctx.send(embed=FARMLAND_NOT_FOUND)
                                return
                        else:
                            await ctx.send(embed=FARMLAND_NOT_FOUND)
                            return
                    else:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                        return
                elif len(arg) == 3:
                    uni_value1 = 0
                    uni_value2 = 0
                    uni_value3 = 0
                    try:
                        uni_value1 = ord(arg[0].lower())
                        uni_value2 = ord(arg[1].lower())
                        uni_value3 = ord(arg[2].lower())
                    except TypeError:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                    if (48 < uni_value1 < 58) and (48 < uni_value2 < 58) and (96 < uni_value3 < 123):
                        plot_template[int(arg[:2]) - 1][uni_value3 - 97] = 1
                    elif (96 < uni_value1 < 123) and (48 < uni_value2 < 58) and (48 < uni_value3 < 58):
                        plot_template[int(arg[1:3]) - 1][uni_value1 - 97] = 1
                    else:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                else:
                    await ctx.send(embed=FARMLAND_NOT_FOUND)
                    return
        else:
            for row in plot_template:
                for i in range(0, len(row)):
                    row[i] = 1  # Should be function which waters a single farmland.
        for row in plot_template:
            print(row)

    @commands.command()
    async def plant(self, ctx, *args):
        """
        *Plant your crops.*
        Example:
            {prefix}plant <crops>
        <crops> is optional, and can also be multiple arguments.
        Rows are enumerated starting at '1'.
        Columns are labeled starting at 'a'.
        Example with 0's instead of farmland:
           a   b   c
        1  0   0   0
        2  0   0   0
        3  0   0   0
        <crops> can be a row, column or a specific crop.
        Specific crop is specified by row number followed by column label.
        (for example a1 for the top left crop.)
        If <crops> is not specified, all crops will be planted.
        """

        plot_template = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                         [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        if args:
            for arg in args:
                if len(arg) == 1:
                    try:
                        uni_value = ord(arg.lower())
                    except TypeError:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                        return
                    if uni_value != 0:
                        if 48 < uni_value < 58:
                            for i in range(0, len(plot_template[int(arg) - 1])):
                                plot_template[int(arg) - 1][i] = 1
                        elif 96 < uni_value < 123:
                            column_num = uni_value - 97
                            for row in plot_template:
                                row[column_num] = 1
                        else:
                            await ctx.send(embed=FARMLAND_NOT_FOUND)
                            return
                elif len(arg) == 2:
                    try:
                        uni_value1 = ord(arg[0].lower())
                        uni_value2 = ord(arg[1].lower())
                    except TypeError:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                        return
                    if (48 < uni_value1 < 58) or (96 < uni_value1 < 123):
                        if (48 < uni_value2 < 58) or (96 < uni_value2 < 123):
                            n = True if 48 < uni_value1 < 58 else False
                            m = True if 48 < uni_value2 < 58 else False
                            if n is not m:
                                if n:
                                    plot_template[uni_value1 - 49][uni_value2 - 97] = 1
                                else:
                                    plot_template[uni_value1 - 97][uni_value2 - 49] = 1
                            elif n and m:
                                for i in range(0, len(plot_template[int(arg) - 1])):
                                    plot_template[int(arg) - 1][i] = 1
                            else:
                                await ctx.send(embed=FARMLAND_NOT_FOUND)
                                return
                        else:
                            await ctx.send(embed=FARMLAND_NOT_FOUND)
                            return
                    else:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                        return
                elif len(arg) == 3:
                    uni_value1 = 0
                    uni_value2 = 0
                    uni_value3 = 0
                    try:
                        uni_value1 = ord(arg[0].lower())
                        uni_value2 = ord(arg[1].lower())
                        uni_value3 = ord(arg[2].lower())
                    except TypeError:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                    if (48 < uni_value1 < 58) and (48 < uni_value2 < 58) and (96 < uni_value3 < 123):
                        plot_template[int(arg[:2]) - 1][uni_value3 - 97] = 1
                    elif (96 < uni_value1 < 123) and (48 < uni_value2 < 58) and (48 < uni_value3 < 58):
                        plot_template[int(arg[1:3]) - 1][uni_value1 - 97] = 1
                    else:
                        await ctx.send(embed=FARMLAND_NOT_FOUND)
                else:
                    await ctx.send(embed=FARMLAND_NOT_FOUND)
                    return
        else:
            for row in plot_template:
                for i in range(0, len(row)):
                    row[i] = 1  # Should be function which plants a single farmland.
        for row in plot_template:
            print(row)


def setup(bot):
    bot.add_cog(Farming(bot))
