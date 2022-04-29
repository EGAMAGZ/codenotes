from typing import Mapping, Any, List, Tuple

import click
from click import Context


class NotRequiredIf(click.Option):
    def __init__(self, *args, **kwargs) -> None:
        self.note_required_if = kwargs.pop('note_required_if')
        assert self.note_required_if, "'not_required_if' parameter required"
        kwargs['help'] = (kwargs.get('help', '') +
                          ' NOTE: This argument is mutually exclusive with %s' %
                          self.note_required_if
                          ).strip()
        super().__init__(args, **kwargs)

    def handle_parse_result(
            self, ctx: Context, opts: Mapping[str, Any], args: List[str]
    ) -> Tuple[Any, List[str]]:
        we_are_present = self.name in opts
        other_present = self.note_required_if in opts

        if other_present:
            if we_are_present:
                raise click.UsageError("Illegal usage: `%s` is mutually exclusive with `%s`" % (
                    self.name, self.not_required_if))
            else:
                self.prompt = None

        return super().handle_parse_result(ctx, opts, args)
