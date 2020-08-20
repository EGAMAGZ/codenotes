from prompt_toolkit.styles import Style
from prompt_toolkit import HTML, print_formatted_text


class PrintFormatted:

    def __init__(self, html_text: HTML, styles: Style):
        self.print = print_formatted_text
        self.print(html_text, style=styles)

    @classmethod
    def print_html(cls, html_text: HTML, styles: Style):
        return cls(html_text, styles)

    @classmethod
    def print_tasks_storage(cls, task_txt: str):
        custom_html = HTML(
            u'<b>></b><msg>Todo task saved: </msg><task-txt>{}</task-txt>'.format(task_txt[:30])
        )

        custom_style = Style.from_dict({  # Style use for prints related with saving process
            'msg': '#d898ed bold',
            'task-txt': '#616161 italic'
        })
        return cls(custom_html, custom_style)
