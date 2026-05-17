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


def smoothnoise(x, y, seed):

    corners = (
        deterministicnoise(x - 1, y - 1, seed) +
        deterministicnoise(x + 1, y - 1, seed) +
        deterministicnoise(x - 1, y + 1, seed) +
        deterministicnoise(x + 1, y + 1, seed)
    ) / 16

    sides = (
        deterministicnoise(x - 1, y, seed) +
        deterministicnoise(x + 1, y, seed) +
        deterministicnoise(x, y - 1, seed) +
        deterministicnoise(x, y + 1, seed)
    ) / 8

    center = deterministicnoise(x, y, seed) / 4

    return corners + sides + center


def generatenoise(
    seed,
    width,
    height,
    minval,
    maxval,
    repeat=False,
    mode="static"
):

    pixels = []

    tilesize = 64

    for y in range(height):

        row = []

        for x in range(width):

            if repeat:

                nx = x % tilesize
                ny = y % tilesize

            else:

                nx = x
                ny = y

            if mode == "static":

                value = deterministicnoise(nx, ny, seed)

            elif mode == "smooth":

                value = smoothnoise(nx, ny, seed)

            elif mode == "grid":

                value = deterministicnoise(
                    nx // 8,
                    ny // 8,
                    seed
                )

            elif mode == "cloud":

                value = (
                    smoothnoise(nx // 2, ny // 2, seed) +
                    smoothnoise(nx // 4, ny // 4, seed + 1)
                ) / 2

            else:

                value = deterministicnoise(nx, ny, seed)

            value = int((value + 1) * 127.5)

            value = max(minval, min(maxval, value))

            value = 255 - value

            row.append(value)

        pixels.append(row)

    return pixels
