import random
import pygame
import pandas
from pygame.math import Vector2
from colormath.color_conversions import convert_color
from colormath.color_objects import HSLColor, AdobeRGBColor
from create_gamut import *


pygame.init()


def import_arrows_files():
	arrow_name = ["".join(["./images/", "arrow", degree, ".png"]) for degree in DISCS_DEGREES]
	arrow_surf = [pygame.image.load(name).convert_alpha() for name in arrow_name]
	arrow_dime = [arrow.get_rect().size for arrow in arrow_surf]
	arrow_coor = []
	for X, Y in arrow_dime:
		arrow_coor.append((int(SCREEN.get_rect().center[0] - X/2), (int(SCREEN.get_rect().center[1] - Y/2))))
	
	arrows_dict = {name:[SCREEN, coor] for (name, SCREEN, coor) in zip(arrow_name, arrow_surf, arrow_coor)}
	return arrows_dict


def rgb2hsl(r, g, b):
	rgb = AdobeRGBColor(r, g, b)
	hsl_angle_color = convert_color(rgb, HSLColor).get_value_tuple()
	return hsl_angle_color[0]


def hsl2rgb(h, s = 1, l = 0.5):
	hsl = HSLColor(h, s, l)
	color = convert_color(hsl, AdobeRGBColor)
	rgb_color =  AdobeRGBColor.get_upscaled_value_tuple(color)
	return rgb_color


def rotate_color_wheel():
	rotated_wheel = pygame.transform.rotate(WHEEL, random.randint(0, 360))
	rotated_wheel_rect = rotated_wheel.get_rect()
	rotated_wheel_rect.center = SCREEN.get_rect().center
	return rotated_wheel, rotated_wheel_rect


def show_fixation_cross():
	SCREEN.fill(BLACK)
	pygame.draw.lines(SCREEN,
		WHITE,
		False,
		[(SCREEN.get_rect().center[0],
			SCREEN.get_rect().center[1] - 30),
		(SCREEN.get_rect().center[0],
			SCREEN.get_rect().center[1] + 30)], 5)
	pygame.draw.lines(SCREEN,
		WHITE,
		False,
		[(SCREEN.get_rect().center[0] - 30,
			SCREEN.get_rect().center[1]),
		(SCREEN.get_rect().center[0] + 30,
			SCREEN.get_rect().center[1])], 5)
	pygame.display.flip()
	fixcross = ''.join(["../images/", "fixation_cross.png"])
	pygame.time.delay(CROSSTIME)
	SCREEN.fill(BLACK)


def show_discs(trial, trials_design, exp_type):
	position = Vector2()
	SCREEN.fill(BLACK)
	pygame.display.flip()
	for disc_degress, color_degrees in zip(
		DISCS_DEGREES, trials_design[trial][9:15]):
		position.from_polar((
			DISTANCE, int(disc_degress)))
		pos = (
			int(SCREEN.get_rect().center[0] + position[0]),
			int(SCREEN.get_rect().center[1] - position[1]))
		rgb = hsl2rgb(h = color_degrees)
		pygame.draw.circle(SCREEN, rgb, pos, RADIUS)
		left = pos[0] - RADIUS
		top = pos[1] - RADIUS
		right = pos[0] + RADIUS
		bottom = pos[1] + RADIUS
	pygame.display.flip()
	trial_discs = ''.join(["../images/", "discs_", exp_type, "_trial_", str(trial), ".png"])
	pygame.time.delay(DISCSTIME)


def precue_time():
	SCREEN.fill(BLACK)
	pygame.display.flip()
	precue = ''.join(["../images/", "precue_time.png"])
	pygame.time.delay(PRECUETIME)


def show_arrows(trial, trials_design):
	for arrow in range(NARROWS):
		SCREEN.fill(BLACK)
		SCREEN.blit(
			ARROWS_DICT[''.join(['./images/', trials_design[trial][arrow]])][0], 
			ARROWS_DICT[''.join(['./images/', trials_design[trial][arrow]])][1])
		pygame.display.flip()
		arrow_dataviewer = ''.join(['../images/', trials_design[trial][arrow]])
		pygame.time.delay(ARROWTIME)
	SCREEN.fill(BLACK)
	pygame.display.flip()


def show_color_wheel(trial, trials_design, rotated_wheel, rotated_wheel_rect):
	position = Vector2()
	SCREEN.blit(rotated_wheel, (
		SCREEN.get_rect().size[0]/2 - rotated_wheel_rect.size[0]/2,
		SCREEN.get_rect().size[1]/2 - rotated_wheel_rect.size[1]/2))
	SCREEN.blit(QUESTION, QUESTION_RECT)
	position.from_polar((DISTANCE, int(trials_design[trial][8][-3:])))
	pos = (int(SCREEN.get_rect().center[0] + position[0]),
		   int(SCREEN.get_rect().center[1] - position[1]))
	pygame.gfxdraw.filled_circle(SCREEN, pos[0], pos[1], RADIUS, BLACK)
	pygame.gfxdraw.aacircle(SCREEN, pos[0], pos[1], RADIUS, WHITE)
	pygame.display.flip()
	pygame.mouse.set_visible(1)
	col_wheel = ''.join(['../images/', 'col_wheel.png'])


def wait_click(trial, trials_design, part_info, part_results_file):
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				x, y = pygame.mouse.get_pos()
				dist = abs(math.sqrt(
					(x - SCREEN.get_rect().center[0]) ** 2 +
					(y - SCREEN.get_rect().center[1]) ** 2))
				if INNER_CIRCLE_RADIUS < dist < OUTER_CIRCLE_RADIUS:
					pygame.mouse.set_pos(SCREEN.get_rect().center)
					pygame.mouse.set_visible(0)
					clicked_color = SCREEN.get_at((x,y))
					hsl_color = rgb2hsl(clicked_color[0], clicked_color[1], clicked_color[2])
					target_color = trials_design[trial][15]
					candi_target = trials_design[trial][7]
					diference = round(abs(trials_design[trial][15] - hsl_color), 3)
					non_transformed_error = diference
					if diference < 180:
						transformed_error = diference
					else:
						transformed_error = 180 - (diference % 180)
					with open(part_results_file, 'a') as f:
						f.write('{};{};{};{};{};{};{};{};{};{};{};{};\n'.format(
							str(trial),
							part_info['name'],
							part_info['par_id'],
							part_info['sex'],
							part_info['age'],
							part_info['session'],
							part_info['exp_type'],
							hsl_color,
							target_color,
							candi_target,
							non_transformed_error,
							transformed_error))
					return 0


WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
FONT = pygame.font.Font("./fonts/Vollkorn-Regular.ttf", 28)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NARROWS = 4
DISCS_DEGREES = ["030", "090", "150", "210", "270", "330"]
DISTANCE = 300
RADIUS = 30
ARROWTIME = 500
NTRIALS = 2
CROSSTIME = 500
DISCSTIME = 1000
PRECUETIME = 500
ARROWS_DICT = import_arrows_files()
INNER_CIRCLE_RADIUS, OUTER_CIRCLE_RADIUS = create_gamut(HEIGHT)
WHEEL = pygame.image.load("./images/" + 'gamut.png').convert_alpha()
QUESTION = FONT.render("¿Color?", True, WHITE)
QUESTION_RECT = QUESTION.get_rect()
QUESTION_RECT.center = SCREEN.get_rect().center