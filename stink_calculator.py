def get_stink_value():
    """
    Compute and return the stink value.
    """
    # Example computation (replace with your actual logic)
    import random
    return round(random.uniform(0, 1), 2)

def get_message(stink_value):
    """
    Generate a message based on the stink value.
    """
    if stink_value < 0.3:
        return "The air is fresh and clean!"
    elif 0.3 <= stink_value < 0.7:
        return "The current stink level is moderate."
    else:
        return "It's really stinky in here!"
