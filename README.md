# Basement Lighting
Using a Rasberry pi and WS2811 addressable light strips to create cool lighting effects

## How to Run
### Installation
Setup the python virtual environment:
``` sh
python -m venv ./venv
source venv/bin/activate
```
You can quickly install everything you need to run by running `./install.sh`.


Or you can do it manually by running these commands:
``` sh
# Install python packages
pip install Cython
pip install -r requirements.txt
# Install node packages
npm install
npm run compile
```

You may also want to set the environment variable for colorterm to true to
enable demos in the terminal:

```sh
export COLORTERM=true
```
You can have this done automatically if you have `direnv`

### Website
Make sure to first enter virtual environment and install dependencies.

Run with:

``` sh
flask run
```

### Running light scripts
You can test/run lighting scripts by first installing necessary dependencies by
setting up the python environment or running `./install.sh`

Then run whichever script directly:

``` sh
python light_scripts/<name of script> [optional color] [optional interval/speed]
```

If you are not running on a rasberry pi/want to test how it would look, make sure to set ceiling to testing mode (`ceil = Ceiling(test_mode=True)`)


## Adding a light script
You can add a light script by creating a file and putting inside either the `parametric_scripts` directory or the `light_scripts`. Scripts that take inputs should go in `parametric_scripts`, and scripts that do not should go in `light_scripts`.

Both directories are searched at runtime and displayed on the website.

Make sure to include a comment near the top of the file to specify the name of the script that will be displayed on the website

``` python
# NAME: <name here>
```

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

By default, it lets you index using the linear indexing system NeoPixels provides:

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

## Animations and displays that change over time
Many light scripts will feature an animation. Doing this is best done using a render loop, tracking the time between frames. The scripts library includes a convenience object that handles calling your code every frame.

To use, create a custom object that extends `RenderState`:

``` python
class Render(RenderState):
    def __init__(self, interval: Optional[float]):
        # initialize state used across render frames here
        super().__init__(interval)

    def render(self, delta: float, ceil: Ceiling) -> Union[bool, None]:
        # Update the display every frame
        return super().render(delta, ceil)

    def interval_reached(self, ceil: Ceiling) -> None:
        # This function is run every `interval` seconds
        return super().interval_reached(ceil)
```
then start the render loop in the `run` function with:

``` python
render_loop = Render(interval=1)
render_loop.run(FPS=30, ceil=ceil)
```

`interval` is optional (can be None) and if it is provided, will call `interval_reached` every `interval` seconds. You can also use `self.progress()` to get the percentage you are from the next `interval` being reached.

`render` must be overriden and is called every frame.

See `example_render.py` for an example.

## Testing

You can test scripts without a rasberry pi right in your terminal
A quick way of doing this is to do this in the constructor:

``` python
ceil = Ceiling(test_mode=True)
```

This will avoid importing rasberry pi specific libraries and print the light show to the terminal. Make sure true color terminal is enabled.
