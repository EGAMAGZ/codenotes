from typing import Text, Final


CLI_USAGE_TEXT: Final[Text] = """[quote]Write any thought you have without quitting from the command line[/quote]

[header]USAGE[/header]
codenotes <command> <subcommand> <text> <flags>

[header]CORE COMMANDS[/header]
add     Create new note or task with the content typed
search  Search for notes or tasks with the parameters specified

[header]SUBCOMMANDS[/header]
note/task       Type of annotations

[header]FLAGS[/header]
--version, -v   Show codenotes version

[header]EXAMPLES[/header]
$ codenotes add task Finish coding the tests --new-categoery Reminders
$ codenotes add task Create documentation for the codenotes proyect; Release the proyect -p
$ codenotes search note --today

[header]FEEDBACK[/header]
Open an issue in [u]github.com/EGAMAGZ/codenotes[/u]"""


ADD_NOTE_USAGE_TEXT: Final[Text] = """[quote]Write any thought you have without quitting from the command line[/quote]

[header]USAGE[/header]
codenotes add note <text> <flags>

[header]FLAGS[/header]
--title,-t <title> Sets a title to the note with a limit of 30 characters. When a title is not specified, it takes
\t\tthe first 30 characters from the note
--category,-c <category> Create a new category if it not exist and will store the note in it
--preview, -p Shows a preview of the note that will be save

[header]USAGE[/header]
$ codenotes add note I got an idea for UI --title UI Idea --category Codenotes"""


ADD_TASK_USAGE_TEXT: Final[Text] = """[quote]Write any thought you have without quitting from the command line[/quote]

[header]USAGE[/header]
codenotes add task <text> <flags>

[header]FLAGS[/header]
--category,-c <category> Create a new category if it not exist and will store the note in it
--preview, -p Shows a preview of the note that will be save

[header]TEXT[/header]
To save two or more task, use the symbol ; to indicate the ending of a task.
[header]USAGE[/header]
$ codenotes add task Finish coding the tests --new-categoery Reminders
$ codenotes add task Create documentation for the codenotes proyect; Release the proyect -p"""
