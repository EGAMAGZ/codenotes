def abbreviate_menu_text(text: str,max_length: int = 15) -> str:
    if len(text) > 15:
        return f'{text[:max_length]}...'
    else:
        return text
