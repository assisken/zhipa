import re

from django import forms
from django.core.exceptions import ValidationError
from djangoeditorwidgets.widgets import MonacoEditorWidget

from .models import News
from .news_md_to_html import NewsLexer

MARKDOWN_HELP = """
    <h3>Небольшой экскурс по markdown. Пригодится при написании новости<h3>
    <h3>Помните! Если хотите новую строку — добавьте две в редакторе. Это не баг. Это Markdown</h3>
    <h2>Стандартный синтаксис Markdown</h2>
    <table>
        <thead>
            <tr>
                <th>Напечатайте так</th>
                <th>Или так</th>
                <th>&hellip; Чтобы получить</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>*Курсив*</td>
                <td>_Курсив_</td>
                <td><em>Курсив</em></td>
            </tr>
            <tr>
                <td>**Жирный**</td>
                <td>__Жирный__</td>
                <td><strong>Жирный</strong></td>
            </tr>
            <tr>
                <td>
                    # Заголовок 1
                </td>
                <td>
                    Заголовок 1<br/>
                    ===========
                </td>
                <td>
                    <h1>Заголовок 1</h1>
                </td>
            </tr>
            <tr>
                <td>
                    ## Заголовок 2
                </td>
                <td>
                    Заголовок 2<br/>
                    -----------
                </td>
                <td>
                    <h2>Заголовок 2</h2>
                </td>
            </tr>
            <tr>
                <td>
                    [Ссылка](http://a.com)
                </td>
                <td>
                    [Ссылка][1]<br/>
                    &#8942;<br/>
                    [1]: http://b.org
                </td>
                <td><a href="https://commonmark.org/help/">Ссылка</a></td>
            </tr>
            <tr>
                <td>
                    ![Картинка](http://url/a.png)
                </td>
                <td>
                    ![Картинка][1]<br/>
                    &#8942;<br/>
                    [1]: http://url/b.jpg
                </td>
                <td>
                    <img src="/static/favicon.ico" width="36" height="36" alt="Картинка"/>
                </td>
            </tr>
            <tr>
                <td>
                    &gt; Цитата
                </td>
                <td>&nbsp;</td>
                <td>
                    <blockquote>Цитата</blockquote>
                </td>
            </tr>
            <tr>
                <td>
                    <p>
                        * Список<br/>
                        * Список<br/>
                        * Список
                    </p>
                </td>
                <td>
                    <p>
                        - Список<br/>
                        - Список<br/>
                        - Список<br/>
                    </p>
                </td>
                <td>
                    <ul>
                        <li>Список</li>
                        <li>Список</li>
                        <li>Список</li>
                    </ul>
                </td>
            </tr>
            <tr>
                <td>
                    <p>
                        1. Один<br/>
                        2. Два<br/>
                        3. Три
                    </p>
                </td>
                <td>
                    <p>
                        1) Один<br/>
                        2) Два<br/>
                        3) Три
                    </p>
                </td>
                <td>
                    <ol>
                        <li>Один</li>
                        <li>Два</li>
                        <li>Три</li>
                    </ol>
                </td>
            </tr>
            <tr>
                <td>
                    Горизонтальная линия<br/>
                    <br/>
                    ---
                </td>
                <td>
                    Горизонтальная линия<br/>
                    <br/>
                    ***
                </td>
                <td>
                    Горизонтальная линия
                    <hr/>
                </td>
            </tr>
            <tr>
                <td>
                    `Моноширинный` с обратными кавычками
                </td>
                <td>&nbsp;</td>
                <td>
                    <code>Моноширинный</code> с обратными кавычками
                </td>
            </tr>
        </tbody>
    </table>

    <h2>Дополнительный синтаксис, который работает в новостях</h2>
    <table>
        <thead>
            <tr>
                <th>Напечатайте так</th>
                <th>&hellip; Чтобы получить</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    &gt; Цитата<br/>
                    &gt; Автор цитаты, описание автора
                </td>
                <td>
                    <blockquote>Цитата</blockquote>
                    <footer><em>— Автор цитаты, описание автора</em></footer>
                </td>
            </tr>
            <tr>
                <td>
                    ![Описание картинки](имя картинки1)(имя картинки2)
                </td>
                <td>
                    <figure style="text-align: center">
                        <img src="/static/favicon.ico" width="36" height="36" alt=""/>
                        <figcaption>Описание картинки</figcaption>
                    </figure>
                </td>
            </tr>
            <tr>
                <td>
                    !grid2[Описание картинки](имя картинки1)(имя картинки2)(имя картинки3)(имя картинки4)
                </td>
                <td>
                    <figure style="text-align: center">
                        <img src="/static/favicon.ico" width="36" height="36" alt=""/>
                        <img src="/static/favicon.ico" width="36" height="36" alt=""/><br/>
                        <img src="/static/favicon.ico" width="36" height="36" alt=""/>
                        <img src="/static/favicon.ico" width="36" height="36" alt=""/>
                        <figcaption>Описание картинки</figcaption>
                    </figure>
                </td>
            </tr>
            <tr>
                <td>
                    !grid3[Описание картинки](имя картинки1)(имя картинки2)(имя картинки3)
                    (имя картинки4)(имя картинки5)(имя картинки6)
                </td>
                <td>
                    <figure style="text-align: center">
                        <img src="/static/favicon.ico" width="36" height="36" alt=""/>
                        <img src="/static/favicon.ico" width="36" height="36" alt=""/>
                        <img src="/static/favicon.ico" width="36" height="36" alt=""/><br/>
                        <img src="/static/favicon.ico" width="36" height="36" alt=""/>
                        <img src="/static/favicon.ico" width="36" height="36" alt=""/>
                        <img src="/static/favicon.ico" width="36" height="36" alt=""/>
                        <figcaption>Описание картинки</figcaption>
                    </figure>

                </td>
            </tr>

        </tbody>
    </table>
    """


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        language = (
            "markdown" if self.instance.render_in == "md" else self.instance.render_in
        )
        self.fields["description"].widget = MonacoEditorWidget(
            attrs={"data-language": language, "data-wordwrap": "on"}
        )
        self.fields["text"].help_text = MARKDOWN_HELP
        self.fields["text"].widget = MonacoEditorWidget(
            attrs={"data-language": language, "data-wordwrap": "on"}
        )

    class Meta:
        model = News
        fields = "__all__"
        exclude = (
            "author",
            "cover",
        )

    def clean(self):
        self.check_text_has_image_name_in_form()
        return super().clean()

    def check_text_has_image_name_in_form(self):
        images = frozenset(
            v
            for k, v in self.data.items()
            if v and re.match(r"newscontentimage_set-\d+-name", k)
        )
        value: str = self.data["text"]
        for line in value.splitlines():
            match = NewsLexer.several_images.match(line)
            if not match:
                continue
            _, _, text_images = NewsLexer.get_items(match)
            if not frozenset(text_images) <= images:
                raise ValidationError(
                    {"text": "Text contains image that does not exist"}
                )
