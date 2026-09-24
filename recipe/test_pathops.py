"""Exercise an actual path operation, not just the import.

Importing pathops only checks that the extension module loads and that libskia
resolves. It does not touch Skia's allocators or the pathops code itself, so a
library that aborts on the first real operation still passes an import test --
which is exactly how a broken osx build shipped before.
"""

import pathops


def rect(x0, y0, x1, y1):
    path = pathops.Path()
    path.moveTo(x0, y0)
    path.lineTo(x1, y0)
    path.lineTo(x1, y1)
    path.lineTo(x0, y1)
    path.close()
    return path


def main():
    a = rect(0, 0, 10, 10)
    b = rect(5, 5, 15, 15)

    union = pathops.Path()
    pathops.union([a, b], union.getPen())
    assert union.bounds == (0.0, 0.0, 15.0, 15.0), union.bounds
    assert len(list(union.segments)) > 0

    difference = pathops.Path()
    pathops.difference([a], [b], difference.getPen())
    assert not difference.bounds == union.bounds

    intersection = pathops.Path()
    pathops.intersection([a], [b], intersection.getPen())
    assert intersection.bounds == (5.0, 5.0, 10.0, 10.0), intersection.bounds

    simplified = rect(0, 0, 10, 10)
    simplified.simplify()
    assert simplified.bounds == (0.0, 0.0, 10.0, 10.0), simplified.bounds

    print("pathops operations ok")


if __name__ == "__main__":
    main()
