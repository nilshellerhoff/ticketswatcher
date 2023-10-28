def oneline(text: str) -> str:
    """remove tabs and newlines

    Parameters:
        text: input text

    Returns:
        str: output text"""

    return text.strip().replace("\n", " ").replace("\t", "")
