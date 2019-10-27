import re
from typing import Match, Tuple, List

import mistune


class NewsLexer(mistune.InlineLexer):
    several_images = re.compile(
        r'!(grid\d+)?'   # !grid2[Title](Any link)(Any link)(Any link)
        r'(\[(.+)\])?'   # or ![Title](Any link)(Any link)
        r'(\((.+)\))+'   # or !grid100(Any link)
    )

    def enable_several_images(self):
        self.rules.several_images = self.several_images
        self.default_rules.insert(0, 'several_images')

    @staticmethod
    def get_items(m: Match[str]) -> Tuple[str, str, List[str]]:
        grid = m.group(1) if m.group(1) else 'grid1'
        title = m.group(3) if m.group(3) else ''
        image_names = m.group(5).split(')(')
        return grid, title, image_names

    def output_several_images(self, m: Match[str]):
        return self.renderer.several_images(*self.get_items(m))


class NewsRenderer(mistune.Renderer):
    def codespan(self, text: str):
        lang, code = text.split('\n', maxsplit=1)
        return self.block_code(code, lang)

    def block_code(self, code, lang=None):
        if not lang:
            lang = ''
        return """
        <blockquote>
            <p><q>{text}</q></p>
            <footer>{author}</footer>
        </blockquote>""".format(
            text=code, author=lang
        ).strip()

    def several_images(self, grid, title, image_names):
        figure_tmpl = """
        <figure class="column"> 
                <a href="{path}" data-lightbox="roadtrip" data-title="{title}">
                    <img src="{path}" alt="">
                </a>
            </figure>
        """

        return """
        <div class="figures center {grid}">
            {figures}
            <figcaption>{title}</figcaption>
        </div>
        """.format(
            figures=''.join(figure_tmpl.format(path=f'{{{name}}}', title=title) for name in image_names),
            grid=grid,
            title=title
        )


__renderer = NewsRenderer()
__lexer = NewsLexer(__renderer)
__lexer.enable_several_images()
MD = mistune.Markdown(renderer=NewsRenderer(), inline=__lexer)
