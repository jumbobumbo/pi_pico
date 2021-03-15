
from random import randint

from time import sleep

import picounicorn


class Skies:

    night_base = [32, 32, 32]
    moon_rgb = [211, 211, 211]
    moon_crater_rgb = [47, 79, 79]
    star_rgb = [162, 185, 255]
    dark_sea_rgb = [0, 0, 139]

    def __init__(self):
        self.setup()
        self.width = picounicorn.get_width()
        self.height = picounicorn.get_height()
        self.moon = {
            15: {"0-1": self.night_base, "2-3": self.moon_rgb, "4-5": self.night_base},
            14: {"0": self.night_base, "1-4": self.moon_rgb, "5": self.night_base},
            13: {"0-3": self.moon_rgb, "4": self.moon_crater_rgb, "5": self.moon_rgb, "6": self.night_base},
            12: {"0-2": self.moon_rgb, "3-4": self.moon_crater_rgb, "5": self.moon_rgb, "6": self.night_base},
            11: {"0": self.night_base, "1-2": self.moon_rgb, "3": self.moon_crater_rgb, "4": self.moon_rgb, "5": self.night_base},
            10: {"0-1": self.night_base, "2-3": self.moon_rgb, "4-5": self.night_base},
            9: {"2-3": self.night_base}
        }

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

    def _paint(self, *args, randomise=False, start_row=0, end_row=None, start_px=0, log=False):
        """Sets the screen to one colour - add a better doc string"""
        updated_pixels = {}
        if not end_row:
            end_row = self.width

        if not isinstance(end_row, int):
            raise TypeError('end_row must be an int or None')

        for index, row in enumerate(range(start_row, end_row)):
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
        for row, px_data in vals.items():
            for pxs, rgb in px_data.items():
                try:

                    update_pixels = pxs.split("-")

                except SyntaxError as ex:
                    print("%s thrown. Key should be a string" % ex)
                    update_pixels = str(pxs).split("-")

                for i in update_pixels:
                    if not i.isdigit():
                        print("Pixel keys must be digits, not '%s. Skipping row!" % i)
                        continue

                update_pixels_len = len(update_pixels)
                if update_pixels_len == 1:
                    picounicorn.set_pixel(row, int(update_pixels[0]), *rgb)
                elif update_pixels_len == 2:
                    for p in range(int(update_pixels[0]), int(update_pixels[1]) + 1):
                        picounicorn.set_pixel(row, p, *rgb)
                else:
                    print('Unexpected key format: %s. Please use values like: "1" or "1-4"' % pxs)

    def _night_sky(self, rgb=night_base):
        """Gens the night sky"""
        self._paint(*rgb)
        stars = self._paint(*self.star_rgb, randomise=True, log=True)  # add stars
        self._paint(*self.dark_sea_rgb, end_row=1)  # add the sea
        self._add_sky_object(vals=self.moon)  # add the moon

if __name__ == "__main__":
    sky = Skies()
    for _ in range(0, 2):
        sky.set_night()
        sleep(5)
