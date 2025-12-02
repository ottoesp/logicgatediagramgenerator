import cProfile
import pstats

import sys
from .main import generate_diagram

if __name__ == "__main__":
    if len(sys.argv) > 1:
        wff = sys.argv[1]
        w = int(sys.argv[2])
    else:
        raise Exception("Expected profiler <wff: str> <w: int>")
    
    profiler = cProfile.Profile()
    profiler.enable()

    result = generate_diagram(wff, w)

    profiler.disable()

    print(result)

    stats = pstats.Stats(profiler).sort_stats("cumtime")
    stats.print_stats()