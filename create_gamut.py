from PIL import Image
import math
from colormath.color_conversions import convert_color
from colormath.color_objects import HSLColor, AdobeRGBColor

# This function will be called at the beggining of each session
def create_gamut(HEIGHT):

	s = 1
	l = 0.5
	r = 60

	img_size = int(HEIGHT*0.88)
	img_half = img_size / 2
	inner_radius = int(HEIGHT*0.39)
	outer_radius = int(HEIGHT*0.44)

	def ang_to_coord_colors(s, l, r, angle):
	    angle = math.radians(angle)
	    x = s + math.cos(angle)*r
	    y = l + math.sin(angle)*r
	    return int(x), int(y)

	def hsl2rgb(h,s,l):
	    hsl = HSLColor(h, s, l)
	    colour = convert_color(hsl, AdobeRGBColor)
	    rgb_color =  AdobeRGBColor.get_upscaled_value_tuple(colour)
	    return rgb_color

	im = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))

	for x in range (0, img_size):

	  for y in range (0, img_size):

	    dist = abs(math.sqrt((x - img_half) ** 2 + (y - img_half) ** 2))

	    if dist < inner_radius or dist > outer_radius:
	      continue;
	    if x - img_half == 0:
	      angle = -90
	      if y > img_half:
	        angle = 90
	    else:
	      angle = math.atan2((y - img_half), (x - img_half)) * 180 / math.pi
	    angle = 360 - (angle) % 360

	    A,B = ang_to_coord_colors(s, l, r, angle)
	    color = hsl2rgb(angle, s, l)
	    im.putpixel((x, y), color)

	im.save('images/gamut.png')

	return inner_radius, outer_radius

if __name__ == "__main__":
	create_gamut()