from noiseforge.config import DEFAULT_TILE_SIZE


def deterministicnoise(x, y, seed):
    n = x + y * 57 + seed * 131
    n = (n << 13) ^ n

    value = 1.0 - (
        (
            (n * (n * n * 15731 + 789221) + 1376312589)
            & 0x7fffffff
        )
        / 1073741824.0
    )

    return value


def generatenoise(
    seed,
    width,
    height,
    minval,
    maxval,
    repeat=False
):
    pixels = []

    for y in range(height):

        row = []

        for x in range(width):

            if repeat:
                nx = x % DEFAULT_TILE_SIZE
                ny = y % DEFAULT_TILE_SIZE
            else:
                nx = x
                ny = y

            value = deterministicnoise(nx, ny, seed)

            value = int((value + 1) * 127.5)

            value = max(minval, min(maxval, value))

            value = 255 - value

            row.append(value)

        pixels.append(row)

    return pixels
