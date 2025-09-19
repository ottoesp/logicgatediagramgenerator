def index_of_containing_set(target: str, sets: list[set[str]]):
    for i, s in enumerate(sets):
        if target in s:
            return i
    return  -1