def reverse_string(s):
    """
    Reverses a given string.
    
    Args:
        s: The string to reverse.
        
    Returns:
        The reversed string.
    """
    return s[::-1]

def is_palindrome(s):
    """
    Checks if a string is a palindrome (reads the same forwards and backwards).
    Ignores case and non-alphanumeric characters.
    """
    s = ''.join(filter(str.isalnum, s)).lower()
    return s == s[::-1] 