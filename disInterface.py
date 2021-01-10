from discord import Embed


class DiscordInterface:
    webhooks = []

    def __init__(self, whs):
        self.webhooks = whs

    def send_embed(self, sneaker, regime="instore"):
        """
        Отправляет информацию об указанном кроссовке в дискорд по всем вебхукам.
        Параметр regime определяет формат доступа к кроссовку в магазине:
        "instore" — кроссовок доступен в свободной продаже
        "raffle" — кроссовок доступен только в розыгрыше
        """
        print("SENT INFO ABOUT: ", sneaker.getName(), " with link ", sneaker.getLink())
        if regime == "instore":
            title = "Доступен в магазине"
            image = sneaker.getImage()
        elif regime == "raffle":
            title = "Раффл"
            image = ""
        else:
            title = "Не удалось определить тип"
            image = ""
        embed = Embed(
            title=title,
            description=sneaker.compileString()
        )
        embed.set_thumbnail(url=image)
        embed.set_author(name=sneaker.shop)
        for wh in self.webhooks:
            wh.send(embed=embed)
