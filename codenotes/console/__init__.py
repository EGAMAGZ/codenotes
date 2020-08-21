from datetime import datetime, date, timedelta
from prompt_toolkit.styles import Style
from prompt_toolkit import HTML, print_formatted_text
import prompt_toolkit.output.win32 as prompt_toolkit


def args_needed_empty(args) -> bool:
    args_needed = [args.month, args.text, args.today, args.week, args.yesterday]
    if any(args_needed):
        return False
    return True


def dates_to_search(args) -> date:
    if args.today:
        return datetime.now().date()
    elif args.yesterday:
        return datetime.now().date() - timedelta(days=1)


class PrintFormatted:

    def __init__(self, html_text: HTML, styles: Style):
        """ PrintFormatted Constructor """
        self.print = print_formatted_text
        try:
            self.print(html_text, style=styles)
        except prompt_toolkit.NoConsoleScreenBufferError:
            print(html_text.value)

    @classmethod
    def print_html(cls, html_text: HTML, styles: Style):
        """ Class method used to print custom formatted text
        Parameters
        ----------
        html_text : HTML
            HTML text that will be print 
        styles: Style
            Styles that will be use in the HTML text
        """
        return cls(html_text, styles)

    @classmethod
    def print_tasks_storage(cls, task_txt: str):
        """ Class method used to print the process of tasks storage
        Parameters
        ----------
        task_txt : str
            Content of the task that is stored
        """
        custom_html = HTML(
            u'<b>></b><msg>Todo task saved: </msg><task-txt>{}</task-txt>'.format(task_txt[:30])
        )

        custom_style = Style.from_dict({  # Style use for prints related with saving process
            'msg': '#d898ed bold',
            'task-txt': '#616161 italic'
        })
        return cls(custom_html, custom_style)
