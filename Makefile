# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: sarabermudez <sarabermudez@student.42.f    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/14 13:35:50 by sarabermude       #+#    #+#              #
#    Updated: 2026/06/04 16:47:44 by sarabermude      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

python := python3
pip := pip
script := a_maze_ing.py

.PHONY: all
all: run

.PHONY: install
install:
	pip install mlx-2.2-py3-ubuntu-any.whl
	
run:
	$(python) $(script) config.txt

debug:
	$(python) -m pdb $(script) config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -r {} + || true
	find . -type d -name ".mypy_cache" -exec rm -r {} + || true

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict