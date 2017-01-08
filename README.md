# legoev3_tcs34725
active color-sensor based on TCS34725 for lego mindstorms ev3

# 1st prototype
The prototype is based on the [Adafruit RGB Color Sensor with IR filter and White LED - TCS34725](https://www.adafruit.com/product/1334).
Unfortunately this breakout board already has 10k pullup resistors for the I2C lines. The LEGO EV3 requires
82k pullup resistors instead. So the first step was to remove the two SMD resistors above the SCL and 3V3 pins:

![modifications](./images/ModifiedSensorBreakout.jpeg "modifications")

Next I plugged the board on a mini breadboard and added 82k resistos and also connected the LED pin to GND to disable
the led on the breakout. The LED is only needed to sense reflected light.

The sensor uses a mindstorms cable which I have cut in half and conncted the wires as below:

EV3 Cable | Adafruit pin (JP1)
--------|-----------
Pin 1 (white) | N/C
Pin 2 (black) | N/C
Pin 3 (red) | GND
Pin 4 (green) | VIN
Pin 5 (yellow) | SCL
Pin 6 (blue) | SDA

# demo code

Copy sensor-test.py to the ev3 and run it. It will print brightness and r,g,b values as soon as the change.
