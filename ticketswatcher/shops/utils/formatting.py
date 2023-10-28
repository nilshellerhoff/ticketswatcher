def oneline(text: str) -> str:
    """remove tabs and newlines

    Parameters:
        text: input text

    Returns:
        str: output text"""

    return text.strip().replace("\n", " ").replace("\t", "")


def remove_double_space(text: str) -> str:
    text = text.replace("  ", " ")
    if "  " in text:
        return remove_double_space(text)
    return text