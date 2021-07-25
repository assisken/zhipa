import re
from typing import List, Match, Tuple

import mistune
from funcy import last


class NewsLexer(mistune.InlineLexer):
    grid_images = re.compile(
        r"!(grid\d+)?"  # !grid2[Title](Any link)(Any link)(Any link)
        r"(\[(.*)\])?"  # or ![Title](Any link)(Any link)
        r"(\((.+)\))+"  # or !grid100(Any link)
    )

    def enable_grid_images(self):
        self.rules.grid_images = self.grid_images
        self.default_rules.insert(0, "grid_images")

    @staticmethod
    def get_grid_images(m: Match[str]) -> Tuple[int, str, List[str]]:
        grid = m.group(1) if m.group(1) else "grid1"
        title = m.group(3) if m.group(3) else ""
        image_names = m.group(5).split(")(")
        return int(grid.replace("grid", "")), title, image_names

    def output_grid_images(self, m: Match[str]):
        return self.renderer.grid_images(*self.get_grid_images(m))

    carousel = re.compile(
        r"!carousel(\d)?"  # !carousel[Title](Any link)(Any link)(...)
        r"(\[(.*)\])?"  # or !carousel(Any link)
        r"(\((.+)\))+"  #
    )

    def enable_carousel(self):
        self.rules.carousel = self.carousel
        self.default_rules.insert(0, "carousel")

    @staticmethod
    def get_carousel(m: Match[str]) -> Tuple[int, str, List[str]]:
        number = m.group(1) if m.group(1) else "1"
        title = m.group(3) if m.group(3) else ""
        image_names = m.group(5).split(")(")
        return int(number), title, image_names

    def output_carousel(self, m: Match[str]):
        return self.renderer.carousel(*self.get_carousel(m))


class NewsRenderer(mistune.Renderer):
    def block_quote(self, text: str):
        if text.endswith("\n"):
            text = text[:-1]
        text = re.sub("</?p>", "", text)
        quote = text.rsplit("\n", maxsplit=2)
        if len(quote) == 1:
            template = '<blockquote class="blockquote"><p>{author}</p></blockquote>'
        else:
            template = """
            <figure>
                <blockquote class="blockquote"><p>{text}</p></blockquote>
                <figcaption class="blockquote-footer">{author}</figcaption>
            </figure>
            """
        return template.format(text=" ".join(quote[:-1]), author=last(quote)).strip()

    def grid_images(self, grid_size: int, title: str, image_names: List[str]):
        image_tmpl = """
        <a class="col-md-{size}" href="{path}" data-lightbox="roadtrip" data-title="{title}">
            <img src="{path}" alt="" class="img-fluid">
        </a>
        """

        return """
        <figure>
            <div class="row">
                {images}
            </div>
            <figcaption class="figure-caption text-center">{title}</figcaption>
        </figure>
        """.format(
            images="".join(
                image_tmpl.format(path=f"{{{name}}}", title=title, size=12 // grid_size)
                for name in image_names
            ),
            title=title,
        )

    def carousel(self, number: int, title: str, image_names: List[str]):
        image_tmpl = """
        <div class="carousel-item {active}">
            <img src="{path}" class="d-block w-100">
        </div>
        """
        buttons_tmpl = """
        <button
           type="button"
           data-bs-target="#carousel{number}"
           data-bs-slide-to="{i}"
           class="{active}"
           aria-current="{current}"
        />
        """

        return """
        <figure>
            <div id="carousel{number}" class="carousel slide" data-bs-ride="carousel">
                <div class="carousel-indicators">
                    {buttons}
                </div>
                <div class="carousel-inner">
                    {images}
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#carousel{number}" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#carousel{number}" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                    <span class="visually-hidden">Next</span>
                </button>
            </div>
            <figcaption class="figure-caption text-center">{title}</figcaption>
        </figure>
        """.format(  # noqa
            title=title,
            number=number,
            images="".join(
                image_tmpl.format(path=f"{{{name}}}", active="active" if i == 0 else "")
                for i, name in enumerate(image_names)
            ),
            buttons="".join(
                buttons_tmpl.format(
                    i=i,
                    active="active" if i == 0 else "",
                    current=i == 0,
                    number=number,
                )
                for i, _ in enumerate(image_names)
            ),
        )


__renderer = NewsRenderer()
__lexer = NewsLexer(__renderer)
__lexer.enable_carousel()
__lexer.enable_grid_images()
MD = mistune.Markdown(renderer=NewsRenderer(), inline=__lexer)
