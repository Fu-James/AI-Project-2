def __valid_input(A: list, B: list) -> bool:
    """
    Raises an exception if the input is not valid.
    Valid parameter should be a list with length 2.

    Parameters:
    ----------
    A : 2D coordinates of A as a list.
    B : 2D coordinates of B as a list.

    Returns:
    -------
    valid_input : True
    """
    if not isinstance(A, list) or not isinstance(B, list):
        raise TypeError("Argument expected to be a list")
    if not len(A) == 2 or not len(B) == 2:
        raise ValueError("Argument length should be 2")
    return True

def __euclidean(A: list, B: list) -> float:
    """
    Computes the Euclidean distance between two coordinate.
    The Euclidean distance between two coordinate A and B, is defined as:
    d((Ax, Ay), (Bx, By)) = ((Ax - Bx) ** 2 + (Ay - By) ** 2) ** 0.5

    Parameters:
    ----------
    A : 2D coordinates of A as a list.
    B : 2D coordinates of B as a list.

    Returns:
    -------
    euclidean : float
        The Euclidean distance between coordinate A and B.
    """
    if __valid_input(A, B):
        Ax, Ay = A
        Bx, By = B
        return ((Ax - Bx) ** 2 + (Ay - By) ** 2) ** 0.5

def __manhattan(A: list, B: list) -> float:
    """
    Computes the Manhattan distance between two coordinate.
    The Manhattan distance between two coordinate A and B, is defined as:
    d((Ax, Ay), (Bx, By)) = |Ax - Bx| + |Ay - By|

    Parameters:
    ----------
    A : 2D coordinates of A as a list.
    B : 2D coordinates of B as a list.

    Returns:
    -------
    manhattan : float
        The Manhattan distance between coordinate A and B.
    """
    if __valid_input(A, B):
        Ax, Ay = A
        Bx, By = B
        return (abs(Ax - Bx) + abs(Ay - By))

def __chebyshev(A: list, B: list) -> float:
    """
    Computes the Chebyshev distance between two coordinate.
    The Chebyshev distance between two coordinate A and B, is defined as:
    d((Ax, Ay), (Bx, By)) = max(|Ax - Bx|, |Ay - By|)

    Parameters:
    ----------
    A : 2D coordinates of A as a list.
    B : 2D coordinates of B as a list.

    Returns:
    -------
    chebyshev : float
        The Chebyshev distance between coordinate A and B.
    """
    if __valid_input(A, B):
        Ax, Ay = A
        Bx, By = B
        return (max(abs(Ax - Bx), abs(Ay - By)))

def __double_chebyshev(A: list, B: list) -> float:
    """
    This function is for Q9
    Computes the Chebyshev distance between two coordinate and multiply by 2.
    """
    return __chebyshev(A, B) * 2

def __double_manhattan(A: list, B: list) -> float:
    """
    This function is for Q9
    Computes the Manhattan distance between two coordinate and multiplied by 2.
    """
    return __manhattan(A, B) * 2

def heuristics(A: list, B: list, option: int=0):
    """
    Computes the heuristic distance between two coordinate based on the option slected.

    Parameters:
    ----------
    A : 2D coordinates of A as a list.
    B : 2D coordinates of B as a list.
    option : int
        0 - Manhattan Distance (Default)
        1 - Euclidean Distance
        2 - Chebyshev Distance
        3 - Double Manhattan Distance
        4 - Double Chebyshev Distance

    Returns:
    -------
    distance : float
        The distance between coordinate A and B based on the heuristic selected.
    """
    if option == 4:
        return __double_chebyshev(A, B)
    if option == 3:
        return __double_manhattan(A, B)
    elif option == 2:
        return __chebyshev(A, B)
    elif option == 1:
        return __euclidean(A, B)
    else:
        return __manhattan(A, B)