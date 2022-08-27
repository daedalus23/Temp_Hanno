from laser import Laser

import servo

def main():
    laser = Laser()
    laser.off()
    while True:
        # servo.manual_move()
        servo.manual_move()


if __name__ == "__main__":
    main()
