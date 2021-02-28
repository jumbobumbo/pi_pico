from random import randint
from utime import sleep
import picounicorn


def start_up(init=True):
    print('....initialising....')
    picounicorn.init()

def get_screen():
    # get the screen width/height
    return picounicorn.get_width(), picounicorn.get_height()

def _rgb_randomiser():

    def _return_randint():
        return randint(0, 255)

    return _return_randint(), _return_randint(), _return_randint()

def draw(w, h, t, sr=0, sc=0, clear=False):
    for row_w in range(sr, w):
        for col_h in range(sc, h):
            if clear:
                x, y, z = 0, 0, 0
            else:
                x, y, z = _rgb_randomiser()
            picounicorn.set_pixel(row_w, col_h, x, y, z)
            sleep(t)

            if picounicorn.is_pressed(picounicorn.BUTTON_B) and not clear:
                sleep(0.5)
                return row_w, col_h

        if sc != 0:  # to make sure all subsequent rows get randomised
            sc = 0

    return 0, 0

def make_dance(w, h):
    def_t = 0.01
    t = def_t  # default sleep time
    r_num = 0
    row = 0
    col = 0
    while not picounicorn.is_pressed(picounicorn.BUTTON_A):

        row, col = draw(w, h, t, row, col)
        if (row, col) != (0, 0):
            r_num += 1
            if r_num > 4:
                t = def_t
                r_num = 0
            else:
                t = t * 2.5

            print(r_num, t)

    print('Clearing screen')
    draw(w, h, t=0, clear=True)
    sleep(1)

if __name__ == "__main__":
    start_up()
    w, h = get_screen()
    while True:
        make_dance(w, h)
