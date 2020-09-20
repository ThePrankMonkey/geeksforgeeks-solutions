"""
Practicing the flood-fill algorithm and making images with pillow.

https://www.geeksforgeeks.org/flood-fill-algorithm-implement-fill-paint/
https://en.wikipedia.org/wiki/Flood_fill
"""


from PIL import Image, ImageDraw


def flood_fill(scene, old_color, new_color, start, image=None):
    if image:
        gif = Gif(image)
    else:
        gif = None

    flood_fill_recursion(scene=scene, old=old_color,
                         new=new_color, location=start, gif=gif)

    if image:
        gif.save_gif()
    return scene


def flood_fill_recursion(scene, old, new, location, gif=None):
    x, y = location
    try:
        if scene[y][x] == old:
            scene[y][x] = new
            # Append Image
            if gif:
                gif.add_image(scene)
            # Check four directions
            flood_fill_recursion(scene, old, new, (x, y-1), gif)  # N
            flood_fill_recursion(scene, old, new, (x+1, y), gif)  # E
            flood_fill_recursion(scene, old, new, (x, y+1), gif)  # S
            flood_fill_recursion(scene, old, new, (x-1, y), gif)  # W
    except IndexError:
        pass


class Gif():
    colors = {
        -1: (128, 128, 128),  # gray
        0: (0, 0, 0),  # black
        1: (255, 255, 255),  # white
        2: (255, 66, 66),  # red
        3: (66, 255, 66),  # green
        4: (66, 66, 255),  # blue
    }

    def __init__(self, file_name):
        self.file_name = file_name
        self.images = []
        self.cell_width = 20
        self.cell_height = 20
        self.speed = 180  # ms
        self.loop = 1

    def add_image(self, scene):
        width = len(scene[0]) * self.cell_width
        height = len(scene) * self.cell_height
        im = Image.new('RGB', (width, height), self.colors[0])
        draw = ImageDraw.Draw(im)
        for i, row in enumerate(scene):
            for j, cell in enumerate(row):
                up_left = (i*self.cell_width, j*self.cell_height)
                low_right = ((i+1)*self.cell_width, (j+1)*self.cell_height)
                draw.rectangle(xy=(up_left, low_right),
                               fill=self.colors[cell], outline=self.colors[-1])
        self.images.append(im)

    def save_gif(self):
        path = f"./{self.file_name}.gif"
        self.images[0].save(
            path, save_all=True, append_images=self.images[1:],
            optimize=False, duration=self.speed, loop=self.loop)


def test_simple():
    given = {
        "scene": [
            [0, 0, 0],
            [0, 1, 1],
            [1, 1, 1],
        ],
        "old_color": 1,
        "new_color": 2,
        "start": (2, 2),
        "image": None,
    }
    expected = [
        [0, 0, 0],
        [0, 2, 2],
        [2, 2, 2],
    ]
    assert flood_fill(**given) == expected


def test_large():
    given = {
        "scene": [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 0, 1, 1],
            [1, 2, 2, 2, 2, 0, 1, 0],
            [1, 1, 1, 2, 2, 0, 1, 0],
            [1, 1, 1, 2, 2, 2, 2, 0],
            [1, 1, 1, 1, 1, 2, 1, 1],
            [1, 1, 1, 1, 1, 2, 2, 1],
        ],
        "old_color": 2,
        "new_color": 3,
        "start": (4, 4),
        "image": "flood_large",
    }
    expected = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0],
        [1, 0, 0, 1, 1, 0, 1, 1],
        [1, 3, 3, 3, 3, 0, 1, 0],
        [1, 1, 1, 3, 3, 0, 1, 0],
        [1, 1, 1, 3, 3, 3, 3, 0],
        [1, 1, 1, 1, 1, 3, 1, 1],
        [1, 1, 1, 1, 1, 3, 3, 1],
    ]
    assert flood_fill(**given) == expected
