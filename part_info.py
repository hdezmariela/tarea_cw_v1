import sys
import time
from os import listdir
from os.path import isfile, join
import pygame
from constants_and_helpers import *


def collect_part_info():
	user_input_x = SCREEN.get_rect().w//2
	user_input_y = SCREEN.get_rect().h//1.5
	part_info = {}
	user_input = ""
	counter = 0
	running = True
	while running:
		for evt in pygame.event.get():
			if evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
				running = False
				pygame.quit()
				sys.exit()
			if evt.type == pygame.KEYDOWN:
				if evt.unicode.isalnum():
					user_input += evt.unicode
				elif evt.key == pygame.K_BACKSPACE:
					user_input = user_input[:-1]
				elif evt.key == pygame.K_SPACE:
					user_input += " "
				elif evt.key == pygame.K_RETURN:
					if counter == 0:
						part_info['name'] = user_input
						# if part_info['name'] == "": sys.exit(); pygame.quit()
					if counter == 1:
						part_info['par_id'] = str(user_input)
						# if len(part_info['par_id']) != 3: sys.exit(); pygame.quit()
						# try: int(part_info['par_id']) 
						# except ValueError: sys.exit(); pygame.quit()
					if counter == 2:
						part_info['sex'] = user_input
						# if part_info['sex'] not in ["masculino", "femenino"]: sys.exit(); pygame.quit()
					if counter == 3:
						part_info['age'] = user_input
						# try: int(part_info['age']) 
						# except ValueError: sys.exit(); pygame.quit()
						# if int(part_info['age']) not in list(range(18, 60)): sys.exit(); pygame.quit()
					if counter == 4:
						part_info['session'] = user_input
						# if part_info['session'] not in ["1", "2"]: sys.exit(); pygame.quit()
					if counter == 5:
						part_info['exp_type'] = user_input
						if part_info['exp_type'] not in ["a", "b"]: sys.exit(); pygame.quit()
						running = False
					user_input = ""
					counter += 1
			elif evt.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		SCREEN.fill(BLACK)
		user_input_rendered = FONT.render(user_input, True, WHITE)
		rect = user_input_rendered.get_rect()
		rect.center = (user_input_x, user_input_y)
		SCREEN.blit(user_input_rendered, rect)
		if counter == 0:
			header = FONT.render("Nombre (Nombre y apellidos)", True, WHITE)
		if counter == 1:
			header = FONT.render("ID (Tres dígitos)", True, WHITE)
		if counter == 2:
			header = FONT.render("Sexo (masculino / femenino)", True, WHITE)
		if counter == 3:
			header = FONT.render("Edad (Dos dígitos, años cumplidos)", True, WHITE)
		if counter == 4:
			header = FONT.render("Sesión (1 / 2)", True, WHITE)
		if counter == 5:
			header = FONT.render("Tipo de experimento (a / b)", True, WHITE)
		header_rect = header.get_rect()
		header_rect.center = SCREEN.get_rect().center
		SCREEN.blit(header, header_rect)
		pygame.display.flip()
	part_results_file = ''.join(['./results/', part_info['par_id'], "_" , time.strftime("%d%m%Y_%H%M%S"), '.csv'])
	with open(part_results_file, 'a') as f:
		f.write('{};{};{};{};{};{};{};{};{};{};{};{}\n'.format(
			'trial', 'name', 'par_id', 'sex', 'age', 'session', 'exp_type',
			'hsl_color', 'target_color', 'candi_target', 'non_transformed_error',
			'transformed_error'))
	SCREEN.fill (BLACK)
	pygame.display.flip()
	next_stage = FONT.render("Presione clic en el mouse para continuar.", True, WHITE)
	next_stage_rect = next_stage.get_rect()
	next_stage_rect.center = SCREEN.get_rect().center
	SCREEN.blit(next_stage, next_stage_rect)
	pygame.display.flip()
	return part_info, part_results_file


if __name__ == "__main__":
	pygame.init()
	collect_part_info()