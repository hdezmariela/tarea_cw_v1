import sys
import pygame
from part_info import collect_part_info
from instructions import present_instructions
from trials import run_trials

# This will generate a new gamut
from constants_helpers import *

# Collect participant info
part_info, part_results_file = collect_part_info()

# Present instructions
present_instructions()

# Run experiment trials
run_trials(part_info, part_results_file)

# Close the experiment graphics
pygame.quit()
sys.exit()