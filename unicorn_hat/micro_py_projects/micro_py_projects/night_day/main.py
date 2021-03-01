import picounicorn


class Skies:

    def __init__(self):
        self.setup()
        self.width = picounicorn.get_width()
        self.height = picounicorn.get_height()

    def setup(self):
        print('....initialising....')
        picounicorn.init()

    def set_night(self):
        """Sets the night sky, sparkly stars"""
        self._gen_sky(False)

    def set_day(self):
        """Sets a sunny day sky"""
        self._gen_sky(True)

    def _gen_sky(self, daytime):
        """Generates the sky

        :param bool daytime: True if daytime, False if Night
        """
        day_base = (22, 113, 153)
        night_base = (6, 6, 10)
        for row in range(0, self.width):
            for px in range(0, self.height):
                if daytime:
                    x, y, z = day_base[0], day_base[1], day_base[2]
                else:
                    x, y, z = night_base[0], night_base[1], night_base[2]

                picounicorn.set_pixel(row, px, x, y, z)


if __name__ == "__main__":
    sky = Skies()
    sky.set_day()
