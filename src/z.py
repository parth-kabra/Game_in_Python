#----------FASTIOSTART-----------#

from __future__ import division, print_function
import os
import sys
from io import BytesIO, IOBase
if sys.version_info[0] < 3:
    from __builtin__ import xrange as range
    from future_builtins import ascii, filter, hex, map, oct, zip
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
def print(*args, **kwargs):
    sep, file = kwargs.pop("sep", " "), kwargs.pop("file", sys.stdout)
    at_start = True
    for x in args:
        if not at_start:
            file.write(sep)
        file.write(str(x))
        at_start = False
    file.write(kwargs.pop("end", "\n"))
    if kwargs.pop("flush", False):
        file.flush()
if sys.version_info[0] < 3:
    sys.stdin, sys.stdout = FastIO(sys.stdin), FastIO(sys.stdout)
else:
    sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)

#----------FASTIOFINISH----------#
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
try:
	app = Ursina()
	grass_texture = load_texture('assets/grass_block.png')
	stone_texture = load_texture('assets/stone_block.png')
	brick_texture = load_texture('assets/brick_block.png')
	dirt_texture  = load_texture('assets/dirt_block.png')
	sky_texture   = load_texture('assets/skybox.png')
	arm_texture   = load_texture('assets/arm_texture.png')
	white_texture = load_texture('assets/white.jpg')
	punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)
	block_pick = 1

	window.fps_counter.enabled = False
	window.exit_button.visible = True

	def update():
		global block_pick

		if held_keys['left mouse'] or held_keys['right mouse']:
			hand.active()
		else:
			hand.passive()

		if held_keys['1']: block_pick = 1
		if held_keys['2']: block_pick = 2
		if held_keys['3']: block_pick = 3
		if held_keys['4']: block_pick = 4
		if held_keys['5']: block_pick = 5
		


	class Voxel(Button):
		def __init__(self, position = (0,0,0), texture = grass_texture):
			super().__init__(
				parent = scene,
				position = position,
				model = 'assets/block',
				origin_y = 0.5,
				texture = texture,
				color = color.color(0,0,random.uniform(0.9,1)),
				scale = 0.5)

		def input(self,key):
			if self.hovered:
				if key == 'left mouse down':
					punch_sound.play()
					if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
					if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
					if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
					if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)
					if block_pick == 5: voxel = Voxel(position = self.position + mouse.normal, texture = white_texture)
				if key == 'right mouse down':
					punch_sound.play()
					destroy(self)

	class Sky(Entity):
		def __init__(self):
			super().__init__(
				parent = scene,
				model = 'sphere',
				texture = sky_texture,
				scale = 150,
				double_sided = True)

	class Hand(Entity):
		def __init__(self):
			super().__init__(
				parent = camera.ui,
				model = 'assets/arm',
				texture = arm_texture,
				scale = 0.2,
				rotation =	Vec3(150,-10,0),
				position = Vec2(0.4,-0.6))

		def active(self):
			self.position = Vec2(0.3,-0.5)

		def passive(self):
			self.position = Vec2(0.4,-0.6)
	for z in range(30):
		for x in range(30):
			voxel = Voxel(position = (x,0,z))

	player = FirstPersonController()
	sky = Sky()
	hand = Hand()

	app.run()
except:
	pass
