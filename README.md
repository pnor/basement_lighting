# byrons basement
Lighting his basement with rasberry pis

Design of web UI
https://www.figma.com/file/CaGVhb8xKwX06VtySUNkGD/byronsbasement-website?node-id=0%3A1&t=5JYDx7SjkIt8KpCZ-3

## Adding a light script
You can add a light script by creating a file and putting inside either the `parametric_scripts` directory or the `light_scripts`. Scripts that take inputs should go in `parametric_scripts`, and scripts that do not should go in `light_scripts`.

Both directories are searched at runtime and displayed on the website.

An example of a starter script file is the `example.py`.

## Writing a light script
### Ceiling
Provided is a `Ceiling` class which exists as a layer between the `NeoPixels` API and the user to make creating light effects easier.

``` python
import board
from backend.ceiling import Ceiling

ceil = Ceiling()

# can specify configurations
ceil = Ceiling(io_pin=board.D10, number_lights=200, auto_write=False)


# clear any lights still on
ceil.clear()
```

By default, it lets you index using the linear indexing system NeoPixels provides by default

``` python
ceil[0] = (255, 0, 0)
ceil[1] = (255, 0, 0)
ceil[2] = (255, 0, 0)
```

but you can also use other coordinate systems, and other means to access LEDs
``` python
ceil.use_row()
ceil[2, 0] = (255, 0, 0) # Set the 1st LED in the 3rd row to red
ceil[3] = (255, 0, 0) # Set all LEDs in the 4th row to red 

ceil.use_cartesian() # All LEDs are in a (0..1)x(0..1) box
ceil[0, 0] = (0, 0, 255) # Set the nearest LED to the bottom left corner to blue
ceil[1, 1] = (0, 0, 255) # Set the nearest LED to the top right corner to blue
ceil[(0, 0):(0.5, 0.5)] = (0, 0, 255) # Set all LEDs in the box from (0..0.5)x(0..0.5) to blue

ceil.use_float_polar((0.5, 0.5), effect_radius=0.2) # Set origin of polar coords to (0.5, 0.5)
ceil[0.3, 270] = (0, 255, 0) # Set LEDs within 0.2 units at radius 0.3, degree 270 to green
ceil[0, 0, 0.2] = (0, 255, 0) # Set all LEDs in the circle of radius 2 centered at (0, 0) to blue
```

A quick overview of the coordinate types:

`ceil.use_lienar()`: Address LEDS based on their position on the strip. Works the same as the normal NeoPixels addressing method

`ceil.use_row()`: Address LEDs based on which row they are on. Can set entire rows by providing just the row index.

`ceil.use_cartesian()`: Address LEDs based on where they are in 2D space using the cartesian coordinate system. LED positions are mapped to a (0..1)x(0..1) box. The closest LED to the coordinate provided (based on size of search_range) will be fetched/set.
You can set rectangles of LEDs by splicing and providing 2 points. 

`ceil.use_polar(origin=)`: Address LEDs based on where they are in 2D space using the polar coordinate system. The origin describes where the origin of the coordinate system is. The closest LED to the coordinate provided (based on size of search_range) will be fetched/set.
You can set circles of LEDs by providing a tuple of 3 elements: (x, y, radius)

`ceil.use_float_cartesian(origin=, effect_radius=)`: Address LEDs based on location in 2D space. Like `use_cartesian` but instead of setting one point, will set all LEDs in the effect radius of the point with varying intensities based on the distance.

`ceil.use_float_polar(origin=, effect_radius=)`: Same as `use_float_cartesian` but uses polar coordinate system.


## Tesintg
You can test scripts without a rasberry pi right in your terminal
A quick way of doing this is to do this in the constructor:

``` python
ceil = Ceiling(test_mode=True)
```

This will avoid importing rasberry pi specific libraries and print the light show to the terminal. Make sure true color terminal is enabled.

