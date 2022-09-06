from flet import UserControl, Column, Text, ListTile


class CodenotesApp(UserControl):
    def build(self):
        return Column(
            [
                Text(value="Codenotes", style="displayLarge"),
                Text(value="General", style="labelLarge")
            ]
        )
