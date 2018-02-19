def validate_dog_age(letter):
    """this function takes a letter as age
    and returns a tuple or range of ages"""

    if "b" or "y" or "a" or "s" in letter:
        return (1, 97)
    elif "b" or "y" in letter:
        return (1, 26)
    elif "a" or "s" in letter:
        return (25, 97)
    elif 'b' in letter:
        return (1, 13)
    elif 'y' in letter:
        return (13, 26)
    elif 'a' in letter:
        return (25, 38)
    else:
        return (37, 97)
