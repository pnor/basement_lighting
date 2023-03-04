# Space Lighting
Using a Rasberry pi and WS2811 addressable light strips to create cool lighting effects

## How to Run
### Installation
You can quickly install everything you need to run by running `./install.sh`.


Or you can do it manually by running these commands:
``` sh
# Create a virtual environment
python -m venv ./venv
venv/bin/activate
# Install python packages
pip install -r requirements.txt # Or if on MacOS, requirements_macos.txt
# Install node packages
npm install
npm run compile
```

### Website
Run with:

``` sh
flask run
```

### Scripts
The scripts are located in a seperate repository that can be fetched using

``` sh
./update_scripts
```
from the root directory

Alternatively, you can write and put scripts in `scripts/light_scripts` to be
discoverable by the website.


### Running light scripts directly
Run whichever script directly:

``` sh
python light_scripts/<name of script> [optional color] [optional interval/speed]
```

If you construct the ceiling using

``` python
State().create_ceiling()
```
This will create a ceiling with the settings specified by `settings.toml`

## Settings
To change what settings with the light strip, you can edit `settings.toml`.

`dimensions`: int, number of dimensions of the arrangement. Should match arrangement file data.
`arrangement_file`: string, path to file used to specify how lights are arranged
`io_pin`: int, GPIO pin on rasberry pi
`number_lights`: int, number of lights to control (can be inferred from arrangement file)
`rows`: list of int, if strip is arranged in rows, specifies how many per row. Optional
`url`: string, endpoint website is run on

Testing:
`test_mode`: boolean, if true will instead show the light animations in a demo window

`sphere_size`: float, size of spheres in the demo

`camera_position`: array of 3 floats, location  of camera in the demo window

`dimension_mask`: array of 3 integers, represents which dimensions are used when viewing in the 3D demo space. Should typically be [0, 1, 2].
- this is relevant if the light strip uses more than 3 dimensions, where you can choose which dimensions to view
- can rearrange dimensions by changing the indeces (example: [2, 0, 1])


An example is provided in `example/example_settings.toml`

## Adding a light script
You can add a light script by creating a file and putting inside either the `parametric_scripts` directory or the `light_scripts`. Scripts that take inputs should go in `parametric_scripts`, and scripts that do not should go in `light_scripts`.

Both directories are searched at runtime and displayed on the website.

Make sure to include a comment near the top of the file to specify the name of the script that will be displayed on the website

``` python
# NAME: <name here>
```

An example of a starter script file is the `example/example.py`.

## Writing a light script
### Ceiling
Provided is a `Ceiling` class which exists as a layer between ws281x API and the user to make creating light effects easier.

``` python
import board
from backend.ceiling import Ceiling

ceil = State().create_ceiling()


# clear any lights still on
ceil.clear()
```

By default, it lets you index using the linear indexing system NeoPixels provides:

``` python
ceil[0] = np.array((255, 0, 0))
ceil[1] = np.array((255, 0, 0))
ceil[2] = np.array((255, 0, 0))
```

but you can also use other coordinate systems, and other means to access LEDs
``` python
ceil.use_row()
ceil[2, 0] = np.array((255, 0, 0)) # Set the 1st LED in the 3rd row to red
ceil[3] = np.array((255, 0, 0)) # Set all LEDs in the 4th row to red 

ceil.use_cartesian() # All LEDs are in a (0..1)x(0..1) box
# Set the nearest LED to the bottom left corner to blue
ceil[0, 0] = np.array((0, 0, 255)) 
# Set the nearest LED to the top right corner to blue
ceil[1, 1] = np.array((0, 0, 255)) 
# Set all LEDs in the box from (0..0.5)x(0..0.5) to blue
ceil[(0, 0):(0.5, 0.5)] = np.array((0, 0, 255)) 

# Set origin of polar coords to (0.5, 0.5)
ceil.use_float_polar((0.5, 0.5), effect_radius=0.2) 
# Set LEDs within 0.2 units at radius 0.3, degree 270 to green
ceil[0.3, 270] = (0, 255, 0) 
# Set all LEDs in the circle of radius 2 centered at (0, 0) to blue
ceil[0, 0, 0.2] = (0, 255, 0)
```

A quick overview of the coordinate types:

`ceil.use_linear()`: Address LEDS based on their position on the strip. Works the same as the normal NeoPixels addressing method

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

See `example/example_render.py` for an example.
