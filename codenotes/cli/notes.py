def add_note_args_empty(args) -> bool:
    args_needed = [
        args.title,
        args.new_category,
        args.text
    ]

    if any(args_needed):
        return False
    return True


class AddNotes:
    def __init__(self, args):
        """ Constructor fro AddTask class 
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        if add_note_args_empty(args):
            pass
        else:
            pass

    @classmethod
    def set_args(cls, args):
        """ Set args and initialize class
        
        Parameters
        ----------
        args : NameSpace
            Arguments of argparse
        """
        return cls(args)
