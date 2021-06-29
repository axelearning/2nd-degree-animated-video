#!/usr/bin/env python
from operator import eq
import sys
sys.path.insert(1, "/Users/axel/Agensit/manim/manim_3b1b")

from manimlib.imports import *

# 1. Ecriture du titre  
# 2. Apparition: Equations qui pop +  Dessine une parabole (5sec)
# 3. Disparition : equation et parabole 
# 4. Déplacement du titre dans le coin en bas à Gauche

# GLOBAL VARIABLES
# -------------------------------------------------------------------
TITLE =  "Les polynomes du second degré"
TITLE_SCALE = 2
TITLE_REDUCTION = 0.25
TITLE_WRITING_TIME = 5


EQUATION_NUMBER = 150
SPACE_BETWEEN_EQ = 1.5
EQUATION_SCALE = 0.5
EQUATION_COLOR = GREY

PARABOLA_POSITION = 3 * DOWN
PARABOLA_CREATION_TIME = 8
PARABOLA_COLOR = BLUE
SLOPE_COEF = 1


# ANIMATION
# -------------------------------------------------------------------
class Title(GraphScene):
	# MAIN
	# ----------------
	def construct(self):
		title = self.get_title()
		parabola =  self.get_parabola()
		equations = self.get_background()
		equations = Group(*equations)


		self.play(Write(title),run_time = TITLE_WRITING_TIME),
		self.bring_to_back(parabola)
		self.play(
			Write(parabola),
			LaggedStart(*[self.write_equation(equation) for equation in equations]), 
			run_time=PARABOLA_CREATION_TIME
		)

		self.play(FadeOut(parabola))
		title.generate_target()
		title.target.scale(TITLE_REDUCTION).to_corner(buff=SMALL_BUFF)
		self.play(MoveToTarget(title), run_time=2)
		
	# SUBSCENES
	# ----------------
	def get_title(self):
		# Show the title 
		title = TextMobject(TITLE)
		title.scale(TITLE_SCALE).set_sheen(2)
		return title
	
	def get_background(self):
		# display some random equation in the background with a diffused apparition
		background = [self.quadratic_fct()]
		for _ in range(EQUATION_NUMBER):
			trinome = self.quadratic_fct()
			position = trinome.get_center()
			distance = [np.linalg.norm(position-eq.get_center()) for eq in background]
			if min(distance) > SPACE_BETWEEN_EQ:
				background.append(trinome)
		return background

	def get_parabola(self, alpha=1, convexe=True):
		# Draw then undraw a parabola
		parabola = FunctionGraph(lambda x: alpha*x**2) if convexe else FunctionGraph(lambda x: -x**2)
		parabola.shift(PARABOLA_POSITION).set_color(PARABOLA_COLOR)
		return parabola

	def transform_title_into_info(self):
		# scale down and send the title into the left bottom corner
		self.play(
			self.title.scale, TITLE_REDUCTION,
			self.title.to_corner, {"buff":SMALL_BUFF},
			run_time=2
		)


	# SUBPROCESS
	# ----------------
	@ staticmethod
	def quadratic_fct():
		# create and assign a random position (and coef) on the frame
		a,b,c = (np.random.randint(2,8) for i in range(3))
		equation = TexMobject(f"{a}x^2+{b}x+{c}")
		equation.scale(EQUATION_SCALE)
		equation.set_color(EQUATION_COLOR)

		def random_number(min, max, division_factor):
			# generate random floating number: could be possitif or negatif
			number = np.random.randint(min,max) / division_factor
			if np.random.randn() < 0:
				number = - number
			return number

		alpha = random_number(min=10,max=35, division_factor=10)
		beta = random_number(min=0,max=65, division_factor=10)
		equation.move_to(alpha*UP+ beta*LEFT)
		return equation
	
	def write_equation(self, equation):
		self.bring_to_back(equation)
		return Succession(
			Write(equation),
			Animation(Mobject()),
			FadeOut(equation)
		)


