import gc, math, random, csv
import pandas
import pygame
from pygame.math import Vector2
import pygame.gfxdraw
from constants_and_helpers import *

# Create a single trial
def do_trial(trial, trials_design, exp_type, part_info, rotated_wheel, rotated_wheel_rect, part_results_file):
	gc.disable()
	show_fixation_cross()
	show_discs(trial, trials_design, exp_type)
	precue_time()
	show_arrows(trial, trials_design)
	show_color_wheel(trial, trials_design, rotated_wheel, rotated_wheel_rect)
	clicked = False
	while not clicked:
		clicked = wait_click(trial, trials_design, part_info, part_results_file)
		if clicked != None:
			ret_value = 0
			gc.enable()
			return ret_value

# Run all trials defined by constant NTRIALS
def run_trials(part_info, part_results_file):
	exp_type = part_info['exp_type']
	trials_design = pandas.read_csv(''.join(['./design/trials_design_', exp_type, '.csv']), sep = ';').set_index('trial_ID').T.to_dict('list')
	for trial in range(1, NTRIALS + 1):
		rotated_wheel, rotated_wheel_rect = rotate_color_wheel()
		while 1:
			ret_value = do_trial(trial, trials_design, exp_type, part_info, rotated_wheel, rotated_wheel_rect, part_results_file)
			if ret_value == 0:
				break
	return 0