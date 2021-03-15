
from random import randint

from time import sleep

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
        self._night_sky()

    def set_day(self):
        """Sets a sunny day sky"""
        self._gen_sky(True)

    def _gen_sky(self, daytime):
        """Generates the sky

        :param bool daytime: True if daytime, False if Night
        """
        day_base = (22, 113, 153)
        night_base = (0, 0, 0)
        # for row in range(0, self.width):
        #     for px in range(0, self.height):
        #         if daytime:
        #             x, y, z = day_base[0], day_base[1], day_base[2]
        #         else:
        #             x, y, z = night_base[0], night_base[1], night_base[2]

        #         picounicorn.set_pixel(row, px, x, y, z)

    def _paint(self, *args, randomise=False, start_row=0, start_px=0, log=False):
        """Sets the screen to one colour - add a better doc string"""
        updated_pixels = {}
        for index, row in enumerate(range(start_row, self.width)):
            updated_pixels[row] = []
            for px in range(start_px, self.height):
                if randomise:
                    if randint(0, 3) != 1:
                        continue

                    try:

                        within_1 = next((x for x in updated_pixels[row] if abs(x - px) < 2))

                    except StopIteration:  # micropython things...
                        within_1 = None

                    if index == 0:
                        previous_row = []
                    else:
                        previous_row = updated_pixels[row - 1]

                    if any([within_1 is not None, px in previous_row]):  # Truthy Falsey
                        continue

                updated_pixels[row].append(px)
                picounicorn.set_pixel(row, px, *args)

            if log:
                print("Pixels updated on last row: %s" % updated_pixels[row])

        if log:
            print("--- All updated pixels ---\n", updated_pixels)

        return updated_pixels

    def _add_sky_object(self, vals):
        """Adds an object into the sky (sun, moon, clouds, etc)

        :param dict vals: {row_num: {px: [R, G, B]}}

        """
        pass

    def _night_sky(self, rgb=[0, 0, 0]):
        """Gens the night sky"""
        self._paint(*rgb)
        self._paint(*[100, 100, 100], randomise=True)  # add stars


if __name__ == "__main__":
    sky = Skies()
    for _ in range(0, 10):
        sky.set_night()
        sleep(5)
