import math, sys
import pandas
import pygame
import pygame.gfxdraw
from pygame.math import Vector2
from constants_and_helpers import *


def import_instructions_file():
	with open('instructions/instructions.txt', encoding = 'latin-1') as f:
		list_instr = f.read().splitlines()
	instructions = {}
	for b in list_instr:
		i = b.split(';')
		instructions[i[0]] = FONT.render(i[1], True, WHITE)
	return 	instructions


instructions = import_instructions_file()
instr_position = Vector2()
trials_design = pandas.read_csv(''.join(['./design/trials_design_', 'a', '.csv']), sep = ';').set_index('trial_ID').T.to_dict('list')


def present_instructions():
	running = True
	counter = 0
	unders_instr = False
	instr_presented = False
	pygame.mouse.set_visible(0)
	while running:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN and not unders_instr and counter < 9:
				SCREEN.fill(BLACK)
				if counter == 0:
					SCREEN.blit(instructions['0.1'], (50, 40))
					SCREEN.blit(instructions['0.0'], (50, HEIGHT - 60))
				if counter == 1:
					SCREEN.blit(instructions['1.0'], (50, 40))
					SCREEN.blit(instructions['0.0'], (50, HEIGHT - 60))
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
				if counter == 2:
					SCREEN.blit(instructions['2.0'], (50, 40))
					SCREEN.blit(instructions['0.0'], (50, HEIGHT - 60))
					for disc_degress, color_degrees in zip(
						DISCS_DEGREES, [0, 90, 180, 270, 300, 330]):
						instr_position.from_polar((
							DISTANCE, int(disc_degress)))
						pos = (
							int(SCREEN.get_rect().center[0] 
								+ instr_position[0]),
							int(SCREEN.get_rect().center[1]
								+ -instr_position[1]))
						rgb = hsl2rgb(h = color_degrees)
						pygame.draw.circle(SCREEN, rgb, pos, RADIUS)
				if counter == 3:
					SCREEN.blit(instructions['3.0'], (50, 40))
					SCREEN.blit(instructions['3.1'], (50, 80))
					SCREEN.blit(instructions['0.0'], (50, HEIGHT - 60))
				if counter == 4:
					for arrow in range(NARROWS):
						SCREEN.blit(
							ARROWS_DICT[''.join(['./images/', 
								trials_design[1][arrow]])][0],
							ARROWS_DICT[''.join(['./images/', 
								trials_design[1][arrow]])][1])
						pygame.display.flip()
						pygame.time.delay(ARROWTIME)
						SCREEN.fill(BLACK)
		
					SCREEN.blit(instructions['0.0'], (50, 80))
					pygame.display.flip()
				if counter == 5:
					SCREEN.blit(instructions['4.0'], (50, 40))
					SCREEN.blit(instructions['0.0'], (50, HEIGHT - 60))
				if counter == 6:
					pygame.mouse.set_visible(1)
					ins_wheel = pygame.transform.rotate(WHEEL, 180)
					ins_wheel_rect = ins_wheel.get_rect()
					ins_wheel_rect.center = SCREEN.get_rect().center
					SCREEN.blit(ins_wheel, (
						SCREEN.get_rect().size[0]/2 - ins_wheel_rect.size[0]/2, int(
							SCREEN.get_rect().size[1]/2 - ins_wheel_rect.size[1]/2)))
					SCREEN.blit(QUESTION, QUESTION_RECT)
					instr_position.from_polar((DISTANCE, 30))
					pos = (int(SCREEN.get_rect().center[0] + instr_position[0]), 
						   int(SCREEN.get_rect().center[1] + -instr_position[1]))
					pygame.gfxdraw.filled_circle(
						SCREEN, pos[0], pos[1], RADIUS, BLACK)
					pygame.gfxdraw.aacircle(
						SCREEN, pos[0], pos[1], RADIUS, WHITE)
					x, y = event.pos
					dist = abs(math.sqrt(
					(x - SCREEN.get_rect().center[0]) ** 2 +
					(y - SCREEN.get_rect().center[1]) ** 2))
					if INNER_CIRCLE_RADIUS < dist < OUTER_CIRCLE_RADIUS:
						pygame.mouse.set_visible(0)
						SCREEN.fill(BLACK)
						counter += 1
				if counter == 7:
					SCREEN.blit(instructions['5.0'], (50, 40))
					SCREEN.blit(instructions['5.1'], (50, 120))
					SCREEN.blit(instructions['5.2'], (50, 160))
				if counter == 8:
					SCREEN.blit(instructions['6.0'], (50, 40))
				if counter != 6:
					counter += 1
				if counter == 9:
					counter = 9
					instr_presented = True
			if (event.type == pygame.KEYDOWN and 
				event.key == pygame.K_n and 
				instr_presented):
				pygame.mouse.set_visible(0)
				SCREEN.fill(BLACK)
				SCREEN.blit(instructions['7.0'], (50, 40))
				pygame.display.flip()
				counter = 0
				unders_instr = False
				instr_presented = False
			if (event.type == pygame.KEYDOWN and 
				event.key == pygame.K_s and 
				instr_presented):
				unders_instr = True
				running = False
		pygame.display.flip()

if __name__ == "__main__":
	present_instructions()