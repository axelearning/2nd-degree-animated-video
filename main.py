#!/usr/bin/env python
from os import symlink
from manimlib.imports import *
import numpy as np


# SOMMAIRE
# -------------------------------------------------------------------
# 1. ECRITURE DU TITRE
# 2. INTRODUCTION
# 3. DEFINITION FORMELLE
# 4. EXEMPLES
# 5. MISTAKES TO AVOID
# 6. VISUALISATION
# 7. RESUME
# 8 OBJECTIF DU COUR

# 1. ECRITURE DU TITRE
# -------------------------------------------------------------------
# VARIABLE GLOBAL
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
class DisplayTitle(GraphScene):
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
	@staticmethod
	def get_title(self):
		# Show the title 
		title = TextMobject(TITLE)
		title.scale(TITLE_SCALE).set_sheen(0.95)
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

# 2. INTRODUCTION
# -------------------------------------------------------------------
# VARIABLE GLOBAL

SENTENCE = "Bienvenue !"

EXAMPLE_1 = "2 x^2 - 3 x + 2"
EXAMPLE_2 = "3 x^2 + 1"
EXAMPLE_3 = "2 x - 1"
EXAMPLE_4 = "x^3 + 2 x^2 + 4 x - 2"
SPACE_BTW_EXP = 1
EXP_SIZE = 1.3
OTHER_EXP_COLOR = GREY
AFFIRMATION = " Polynomes du \\\second degré"
AFFIRMATION_COLOR = YELLOW

CURVE_1_COLOR = PERSIAN_GREEN
CURVE_2_COLOR = BURNT_SIENNA
CURVE_3_COLOR = SANDY_BROWN
FADE_RATIO = 0.85
RUN_TIME = 0.5

# CUSTOM MOBJECT
class SimpleCrossAxes(Axes):
	CONFIG = {
		"axis_config": {
			"color": GREY,
			"include_tip": False,
			"include_ticks": False,
			"include_tip": False,
		},
		"x_axis_config": {},
		"y_axis_config": {
			"label_direction": LEFT,
		},
		"center_point": ORIGIN,
		"x_min" : -5.5,
		"x_max" : 4,
		"y_max" : 3.5,
		"y_min" : -3.5,
	}
# ANIMATION
class Intro(AlexScene):
	CONFIG = {
		"creatures_start_on_screen": True,
		"default_creature_kwargs": {
			"color": SANDY_BROWN,
			"mode": "confident"
		}
	}
	def construct(self, **kwargs):
		digest_config(self, kwargs)
		# info in the left corner
		title = TextMobject(TITLE)
		title.scale(TITLE_SCALE*TITLE_REDUCTION).set_sheen(0.95).to_corner(DL, buff=SMALL_BUFF)

		# Algebrique expressions' examples
		trinome = Expression(EXAMPLE_1, in_color=False)
		trinome_2 = Expression(EXAMPLE_2, in_color=False)
		not_a_trinome= Expression(EXAMPLE_3, in_color=False)
		not_a_trinome_2 = Expression(EXAMPLE_4, in_color=False)
		examples = VGroup(*[trinome, not_a_trinome, trinome_2, not_a_trinome_2])\
			.scale(EXP_SIZE)\
			.arrange(DOWN, buff=SPACE_BTW_EXP)\
			.shift(3*LEFT)\
			.align_elm()
		text = TextMobject(AFFIRMATION)\
			.set_color(AFFIRMATION_COLOR)\
			.scale(1.2)\
			.next_to(self.creature, UL, buff=0.2)\
		
		# Graphs' examples
		axes = SimpleCrossAxes().shift(1*LEFT)
		x_min, x_max = np.roots([0.8,2,-2- axes.y_max])
		curve_1 = axes.get_graph(lambda x: 0.8*x**2 + 2*x - 2, color=CURVE_1_COLOR, x_min=x_min, x_max=x_max)
		curve_2 = axes.get_graph(lambda x: -0.6*x - 1, color=CURVE_2_COLOR)
		curve_3 = axes.get_graph(lambda x: -2*x**3 + 5*x**2 -0.1*x - 2, color=CURVE_3_COLOR, x_min=-0.883, x_max=2.581)
		graph = VGroup(axes,curve_2,curve_3, curve_1)
		line = Line()
		line2= Line().move_to(line.get_center()).rotate(PI/2)
		cross = VGroup(line,line2).rotate(PI/4).scale(0.5).set_color(RED)
		tcheck = Tcheck()

		# animate
		self.add(title)
		self.creature.look_at_u()
		self.appears()
		self.say(SENTENCE, target_mode="confident", look_at_arg=None)
		self.look_at_u()
		self.wait(2)
		self.play(RemoveBubble(self.creature, look_at_arg=None))
		self.play(
			*[FadeInFrom(example,LEFT) for example in examples], 
			lag_ratio=0.3,
			run_time=2, 
			rate_func=rush_into
		)
		self.change_mode("think")
		self.wait()
		self.play(
			LaggedStart(
				ApplyMethod(not_a_trinome.fade, FADE_RATIO),
				ApplyMethod(not_a_trinome_2.fade, FADE_RATIO),
				ApplyMethod(trinome.set_color_coef),
				ApplyMethod(trinome_2.set_color_coef),
				ApplyMethod(self.creature.change, "happy"),
				FadeInFrom(text),
				lag_ratio = 0.1,
				run_time = 0.5
			),
		)
		self.wait()
		self.play(
			FadeOut(examples),
			FadeOut(text)
		)
		self.add(axes)
		self.play(Write(curve_2, rate_func=rush_into, run_time = RUN_TIME))
		self.say(cross, target_mode="confident", run_time=RUN_TIME)
		self.play(
			RemoveBubble(self.creature),
			ApplyMethod(curve_2.fade, 0.85),
			run_time = RUN_TIME
		)
		self.play(Write(curve_3, rate_func=rush_into, run_time = RUN_TIME))
		self.say(cross, target_mode="confident", run_time=RUN_TIME)
		self.play(
			RemoveBubble(self.creature),
			ApplyMethod(curve_3.fade, 0.85),
			run_time = RUN_TIME
		)
		self.play(Write(curve_1, rate_func=rush_into, run_time = RUN_TIME))
		self.say(tcheck, target_mode="happy", run_time=RUN_TIME)
		self.wait(2)


# 2. DEFINITION
# -------------------------------------------------------------------
# VARIABLE GLOBAL

SUBTITLE = "Définition"
SUBTITLE_COLOR = BLUE
SUBTITLE_SCALE = 2
SUBTITLE_WRITING_TIME = 1
SUBTITLE_REDUCTION = 0.5

EXPRESSION_SIZE = 2
A_COLOR = BLUE
B_COLOR = RED
C_COLOR = GREEN
FADE = 0.75
ZOOM_IN_SCALE = 3
NUMBER_TRANSFORM_TIME = 0.3

_SIZE = EXPRESSION_SIZE*ZOOM_IN_SCALE

class Definition(Scene):
	def construct(self):
		# 0 . DISPLAY TITLE & SUBTITLE 
		# ----------------------------
		title = TextMobject(TITLE)
		title.scale(TITLE_SCALE*TITLE_REDUCTION).set_sheen(0.95).to_corner(DL, buff=SMALL_BUFF)
		subtitle = TextMobject(SUBTITLE, color=SUBTITLE_COLOR)
		subtitle.scale(SUBTITLE_SCALE)
		subtitle_as_info = TextMobject(f"/ {SUBTITLE}", color=SUBTITLE_COLOR)
		subtitle_as_info.scale(SUBTITLE_REDUCTION)
		subtitle_as_info.next_to(title, buff=SMALL_BUFF)

		self.add(title)
		self.play(Write(subtitle, run_time=SUBTITLE_WRITING_TIME))
		self.wait()
		self.play(ReplacementTransform(subtitle, subtitle_as_info))

		expression = TexMobject("?~~","+","~~?~~","+","~?").scale(EXPRESSION_SIZE)
		expression[0].set_color(A_COLOR)
		expression[2].set_color(B_COLOR)
		expression[-1].set_color(C_COLOR)
		expression.generate_target()
		expression.target.fade(FADE).to_edge(UP)

		self.play(Write(expression))
		self.play(MoveToTarget(expression))

		# 1. C: constante term
		# ----------------------------
		c = expression[-1].copy()

		# send it to the center
		def zoom_in(mob):
			mob.set_opacity(1)
			mob.scale(ZOOM_IN_SCALE)
			mob.move_to(ORIGIN)
			return mob

		self.play(
			ApplyFunction(zoom_in, c),
			ApplyMethod(expression[-1].set_opacity, 0.9)
		)
		self.wait(4)

		# display different value of c
		integer = Integer(3, color=C_COLOR).scale(_SIZE)
		relatif = Integer(-2, color=C_COLOR).scale(_SIZE)
		decimal = TexMobject(r"\frac{1}{2}", color=C_COLOR).scale(0.6*_SIZE)
		irational = TexMobject(r"\sqrt{2}", color=C_COLOR).scale(0.6*_SIZE)
		notation = TexMobject("c", color=C_COLOR).scale(_SIZE)

		self.play(Transform(c, integer), run_time=NUMBER_TRANSFORM_TIME)
		self.wait(2)
		self.play(Transform(c, relatif), run_time=NUMBER_TRANSFORM_TIME)
		self.wait()
		self.play(Transform(c, decimal), run_time=NUMBER_TRANSFORM_TIME)
		self.wait(2)
		self.play(Transform(c, irational), run_time=NUMBER_TRANSFORM_TIME)
		self.wait(2)
		self.play(Transform(c, notation), run_time=NUMBER_TRANSFORM_TIME)
		self.wait()

		
		# move back to expression
		c.generate_target()
		c.target.scale(1/2).move_to(expression[-2].get_right()+0.6*RIGHT)

		self.wait()
		self.play(MoveToTarget(c), FadeOut(expression[-1]))
		self.play(c.fade,FADE)
		self.wait(0.3)

		# 2. BX
		# ----------------------------
		bx = expression[2].copy()

		# send it to the center
		self.play(
			ApplyFunction(zoom_in, bx),
			ApplyMethod(expression[2].set_opacity, 0.9)
		)
		
		# display different value of b
		term = TexMobject("b","x").scale(_SIZE)
		term[0].set_color(B_COLOR)
		number_position = term[1].get_left() + LEFT

		integer = TexMobject("5", color=B_COLOR)
		integer.scale(_SIZE).move_to(number_position).align_to(term, DOWN)
		decimal = TexMobject(r"\frac{3}{4}", color=B_COLOR)
		decimal.scale(0.7*_SIZE).move_to(number_position)
		irational = TexMobject(r"\sqrt{5}", color=B_COLOR)
		irational.scale(0.7*_SIZE).move_to(number_position+0.7*LEFT)
		irational[-1].align_to(term,DOWN)

		self.play(Transform(bx, term))
		self.wait(2)
		self.play(Transform(bx[0], integer), run_time=NUMBER_TRANSFORM_TIME)
		self.wait(3*NUMBER_TRANSFORM_TIME)
		self.play(Transform(bx[0], decimal), run_time=NUMBER_TRANSFORM_TIME)
		self.wait(3*NUMBER_TRANSFORM_TIME)
		self.play(Transform(bx[0], irational), run_time=NUMBER_TRANSFORM_TIME)
		self.wait(3*NUMBER_TRANSFORM_TIME)
		self.play(Transform(bx[0], term[0]))
		self.wait()

		# move back to expression
		bx.generate_target()
		bx.target.scale(1/2).move_to(expression[2].get_center()).align_to(expression, DOWN)
		
		self.play(MoveToTarget(bx),FadeOut(expression[2]), run_time=0.5)
		self.wait(0.3)
		self.play(bx.fade,FADE)

		# 3. AX^2
		# ----------------------------
		ax2 = expression[0].copy()

		# send it to the center
		self.play(
			ApplyFunction(zoom_in, ax2), 
			ApplyMethod(expression[0].set_opacity, 0.9),
			run_time=0.5
		)

		# display different value of a
		term = TexMobject("a","x^2").scale(_SIZE)
		term[0].set_color(A_COLOR)
		position = term[1].get_left() + LEFT

		integer = TexMobject("3", color=A_COLOR).scale(_SIZE).move_to(position).align_to(term,DOWN)
		decimal = TexMobject(r"\frac{5}{9}", color=A_COLOR).scale(0.7*_SIZE).move_to(position+0.5*DOWN)
		irational = TexMobject(r"\pi", color=A_COLOR).scale(_SIZE).move_to(position)
		irational[-1].align_to(term,DOWN)

		self.play(Transform(ax2, term))
		self.wait(4)
		self.play(Transform(ax2[0], integer), run_time=NUMBER_TRANSFORM_TIME)
		self.wait(3*NUMBER_TRANSFORM_TIME)
		self.play(Transform(ax2[0], decimal), run_time=NUMBER_TRANSFORM_TIME)
		self.wait(3*NUMBER_TRANSFORM_TIME)
		self.play(Transform(ax2[0], irational), run_time=NUMBER_TRANSFORM_TIME)
		self.wait(3*NUMBER_TRANSFORM_TIME)

		# forbiden value
		zero = TexMobject("0", color=A_COLOR)\
			.scale(_SIZE)\
			.move_to(position)\
			.align_to(ax2,DOWN)
		red_cross = Cross(zero)

		self.play(Transform(ax2[0], zero), run_time=NUMBER_TRANSFORM_TIME)
		self.play(ShowCreation(red_cross))

		part_expression = VGroup(expression[1], bx, expression[3], c)
		part_expression.generate_target()
		part_expression.target.set_opacity(0.85)
		part_expression.target.move_to(ORIGIN+RIGHT)
		ax2.generate_target()
		ax2.target\
			.scale(1/EXPRESSION_SIZE)\
			.move_to(part_expression.target.get_left()+LEFT)\
			.align_to(part_expression.target, DOWN)

		self.wait()
		self.play(Uncreate(red_cross))
		self.play(
			LaggedStart(
			FadeOut(expression[0]),
			MoveToTarget(part_expression),
			MoveToTarget(ax2)
			),
			run_time=0.5
		)
		self.wait(0.5)
		self.play(
			FadeOut(ax2), 
			FadeOut(part_expression[0]),
			part_expression[1:].move_to,ORIGIN,
			run_time=0.5
		)
		self.wait(5)
		braces=Brace(part_expression[1:],TOP)
		braces_tex = braces.get_text("Fonction affine")
		self.play(GrowFromCenter(braces),Write(braces_tex))
		self.wait(3)


# 3. DEFINITION FORMELLE
# -------------------------------------------------------------------
# VARIABLE GLOBAL
EXPRESSION = "P(x) = a x^2 + b x + c"
EXPRESSION_SIZE = 2
REDUCTION_FACTOR = 0.8
SENTENCE = "Définition formelle"

DEFINITION_TITLE = "Polynome du second degré"
DEFINITION_TITLE_COLOR = GREY
INFO_1 = ["ou ","a",","," b",","," c"," $\in \mathbb{R}$"]
INFO_2 = ["et~","a","\\neq0"]

class FormalDefinition(AlexScene):
	CONFIG = {
		"default_creature_kwargs": {
			"color": SANDY_BROWN,
			"mode": "confident"
		}
	}

	def construct(self, **kwargs):
		digest_config(self, kwargs)
		# info
		title = TextMobject(TITLE)
		title.scale(TITLE_SCALE*TITLE_REDUCTION).set_sheen(0.95).to_corner(DL, buff=SMALL_BUFF)
		subtitle = TextMobject(f"/ {SUBTITLE}", color=SUBTITLE_COLOR)
		subtitle.scale(SUBTITLE_REDUCTION)
		subtitle.next_to(title, buff=SMALL_BUFF)

		# creature
		mode = self.default_creature_kwargs["mode"]
		self.creature.look_at_u()

		# create content
		info = TextMobject(DEFINITION_TITLE).set_color(DEFINITION_TITLE_COLOR)
		trinome = Expression(EXPRESSION).scale(EXPRESSION_SIZE)
		info1 = TextMobject(*INFO_1)
		info1[1].set_color(A_COLOR)
		info1[3].set_color(B_COLOR)
		info1[5].set_color(C_COLOR)
		info2 = TexMobject(*INFO_2).scale(REDUCTION_FACTOR)
		info2[1].set_color(A_COLOR)
		general_expression = VGroup(info, trinome, info1, info2).arrange(DOWN)
		general_expression.align_elm().move_to (ORIGIN+0.5*UP)
		Group(info1, info2).shift(DOWN)
		info.shift(0.5*UP)
		underline = Underline(info, color=info.get_color())
		
		# animate
		self.add(title, subtitle)
		self.appears()
		self.say(SENTENCE, target_mode=mode)
		self.wait()
		self.play(RemoveBubble(self.creature, target_mode=mode))
		self.play(ShowCreation(info), run_time=2)
		self.play(GrowFromCenter(underline))
		self.wait(2)
		self.play(Write(trinome), run_time=4)
		self.play(Write(info1), run_time=1.5)
		self.wait()
		self.play(Write(info2))	
		self.look_at_u()	
		self.wait(5)
		self.disappears()
		self.play(
			FadeOut(general_expression),
			FadeOut(underline)
		)

# 4. EXEMPLES
# -------------------------------------------------------------------
# VARIABLE GLOBAL
OLD_SUBTITLE = "Définition"
SUBTITLE = "Exemples"
SUBTITLE_COLOR = BLUE
SUBTITLE_SCALE = 2
SUBTITLE_WRITING_TIME = 1
SUBTITLE_REDUCTION = 0.5

EXPRESSION_SIZE = 2
INFO_SIZE = 1.3
QUESTIONMARK_FADE = 0.7
RUN_TIME = 0.3

EXAMPLE_1 = "2 x^2 -3 x + 2"
EXAMPLE_2 = "x^2 + 1"
EXAMPLE_3 = "x - 1"
EXAMPLE_4 = "x^3 + 2 x^2 + 4"

DEV_FORM = "x^2 - 6x + 5"
DEV_TEXT = ["Forme", " développée"]
CANONIC_FORM = "(x - 3)^2 - 4"
CANONIC_TEXT = ["Forme", " canonique"]
FACT_FORM = "(x-1)(x-2)"
FACT_TEXT = ["Forme", " factorisée"]


class Examples(AlexScene):
	CONFIG = {
		"creatures_start_on_screen": False,
		"default_creature_kwargs": {
			"color": SANDY_BROWN,
			"mode": "think_2"
		}
	}

	def construct(self, **kwargs):
		digest_config(self, kwargs)
		self.write_subtitle()
		left_anchor = self.example_1()
		self.example_2(left_anchor)
		self.example_3(left_anchor)
		self.example_4(left_anchor)
		self.other_form(left_anchor)
	
	# SUBSCENE
	# -------------------------------------
	def write_subtitle(self):
		# 1. Subtitle & info 
		title_as_info = TextMobject(TITLE)
		title_as_info.scale(TITLE_SCALE*TITLE_REDUCTION).set_sheen(0.95).to_corner(DL, buff=SMALL_BUFF)
		old_subtitle = TextMobject(f"/ {OLD_SUBTITLE}").scale(SUBTITLE_REDUCTION).set_color(SUBTITLE_COLOR)
		old_subtitle.next_to(title_as_info, buff=SMALL_BUFF)
		subtitle = TextMobject(SUBTITLE, color=SUBTITLE_COLOR).scale(SUBTITLE_SCALE)
		subititle_as_info = TextMobject(f"/ {SUBTITLE}", color=SUBTITLE_COLOR)
		subititle_as_info.scale(SUBTITLE_REDUCTION).next_to(title_as_info, buff=SMALL_BUFF)


		self.add(title_as_info, old_subtitle)
		self.play(Write(subtitle), run_time=SUBTITLE_WRITING_TIME)
		self.wait(0.5)
		self.play(
			Transform(subtitle, subititle_as_info),
			FadeOut(old_subtitle)
		)
	
	def example_1(self):
		example = Expression(EXAMPLE_1, in_color=False).scale(EXPRESSION_SIZE)
		a = TexMobject("a","=","2")
		a[0].set_color(A_COLOR)
		b = TexMobject("b","=","-3")
		b[0].set_color(B_COLOR)
		c =  TexMobject("c","=","2")
		c[0].set_color(C_COLOR)
		info = VGroup(a,b,c).scale(INFO_SIZE).arrange(DOWN).align_elm()
		VGroup(example, info).arrange(DOWN, buff=1).align_elm()
		A,B,C = example[0].copy(), example[2].copy(), example[-1].copy()

		self.play(Write(example))
		self.wait(3)

		# a
		self.play(Indicate(example[1], color= A_COLOR))
		self.play(
			LaggedStart(
				FocusOn(example[0], color=A_COLOR),
				ApplyMethod(example[0].set_color, A_COLOR), 
				lag_ratio=0.3
			)
		)
		self.play(CounterclockwiseTransform(A, a))
		self.wait(2)

		# b 
		self.play(Indicate(example[3], color= B_COLOR))
		self.play(
			LaggedStart(
				FocusOn(example[2], color=B_COLOR),
				ApplyMethod(example[2].set_color, B_COLOR), 
				lag_ratio=0.3
			)
		)
		self.play(CounterclockwiseTransform(B, b))
		self.wait()

		# c
		self.play(
			LaggedStart(
				FocusOn(example[-1], color=C_COLOR),
				ApplyMethod(example[-1].set_color, C_COLOR), 
				lag_ratio=0.3
			)
		)
		self.wait()
		self.play(CounterclockwiseTransform(C, c))
		self.wait(2)
		self.play(
			FadeOut(example),
			*[FadeOut(elm) for elm in [A,B,C]]
		)
		return example
	
	def example_2(self, left_anchor):	
		example = Expression(EXAMPLE_2, in_color=False).scale(EXPRESSION_SIZE)
		# info
		a = TexMobject("a","=","1")
		a[0].set_color(A_COLOR)
		b = TexMobject("b","=","0")
		b[0].set_color(B_COLOR)
		c =  TexMobject("c","=","1")
		c[0].set_color(C_COLOR)

		# align and place elm
		info = VGroup(a,b,c).scale(INFO_SIZE).arrange(DOWN).align_elm()
		VGroup(example, info).arrange(DOWN, buff=1).align_elm(left_anchor)

		# add the hidden term 0x 
		hiding_term  = Expression("+ 0 x ", in_color=False)
		hiding_term.scale(EXPRESSION_SIZE)\
			.move_to(example[1].get_center()+0.45*RIGHT)\
			.align_to(example, DOWN)
		cst_term = VGroup(example[1:])
		cst_term.generate_target()
		cst_term.target.move_to(hiding_term.get_right() + 0.9*RIGHT)
		A,B,C = example[0].copy(), hiding_term[1].copy(), cst_term.target[-1].copy()


		# display 
		self.play(Write(example))
		self.appears()
		self.wait(2)
		# add 0x in the expression
		self.play(
			FadeInFrom(hiding_term),
			MoveToTarget(cst_term)
		)
		self.wait(2)
		# give color to coef
		self.play(
			example.set_color_coef,
			hiding_term.set_color_coef
		)
		self.change_mode("confident")
		self.wait(2)
		# find each coefs (a,b,c)
		self.play(CounterclockwiseTransform(A, a), run_time= RUN_TIME)
		self.wait(2*RUN_TIME)
		self.play(CounterclockwiseTransform(B, b), run_time= RUN_TIME)
		self.wait(2*RUN_TIME)
		self.play(CounterclockwiseTransform(C, c), run_time= RUN_TIME)
		self.wait(2)

		# FadeOut
		self.play(*[FadeOut(elm) for elm in (A,B,C, example, hiding_term)])
		self.change_mode("normal")

	def example_3(self, left_anchor):
		example = Expression(EXAMPLE_3).scale(EXPRESSION_SIZE).align_to(left_anchor, UL)
		bubble_content = TexMobject("a","= 0")
		bubble_content[0].set_color(A_COLOR)
		a_zero = Expression("0 x^2 + ").scale(EXPRESSION_SIZE).align_to(example, UL).fade(0.7)


		self.play(Write(example))
		self.change_mode("think")
		example.save_state()
		example.generate_target()
		example.target.move_to(a_zero.get_right() + 1.3 *RIGHT).align_to(a_zero)
		self.play(
			FadeInFrom(a_zero, LEFT),
			MoveToTarget(example)
		)
		self.say(bubble_content, target_mode="confident")
		self.wait()
		self.play(
			FadeOut(a_zero),
			Restore(example)
		)
		self.wait(2)
		self.play(FadeOut(example), RemoveBubble(self.creature))
		self.change_mode("normal")

	def example_4(self, left_anchor):
		example = Expression(EXAMPLE_4, in_color=False).scale(EXPRESSION_SIZE).align_to(left_anchor, UL)
		example[0].generate_target()
		example[0].target.set_color(YELLOW)
		braces=Brace(example,BOTTOM)
		braces_tex = braces.get_text("Polynome de degr","é"," 3")
		braces_tex[-1].set_color(YELLOW).scale(1.3).align_to(braces_tex[1], DOWN)

		self.wait(2)
		self.play(Write(example), run_time=2)
		self.change_mode("think_2")
		self.wait(2)
		self.play(example.set_color_coef)
		self.play(Indicate(example[0], scale_factor= 1.5)),
		self.change_mode("wow") 
		self.play(
			GrowFromCenter(braces),
			Succession(
				Write(braces_tex),
				MoveToTarget(example[0])
			)
		)
		self.wait(2)
		self.change_mode("normal")
		self.play(
			Uncreate(example),
			Uncreate(braces_tex),
			ShrinkToCenter(braces)
		)

	def other_form(self, left_anchor):
		develop = TexMobject(DEV_FORM).scale(EXPRESSION_SIZE).align_to(left_anchor, UL)
		brace = Brace(develop)
		brace_tex = brace.get_text(*DEV_TEXT)
		brace_tex[-1].set_color(YELLOW)

		self.wait(3)
		self.play(Write(develop), run_time=2)
		self.wait(2)
		self.play(
			GrowFromCenter(brace),
			ShowCreation(brace_tex)
		)
		self.wait(2)
		self.play(
			ShrinkToCenter(brace),
			Uncreate(brace_tex)
		)

		canonic = TexMobject(CANONIC_FORM).scale(EXPRESSION_SIZE).align_to(left_anchor, UL)
		brace = Brace(canonic)
		brace_tex = brace.get_text(*CANONIC_TEXT)
		brace_tex[-1].set_color(YELLOW)

		self.play(ReplacementTransform(develop, canonic))
		self.change_mode("think")
		self.play(
			GrowFromCenter(brace),
			ShowCreation(brace_tex)
		)
		self.wait()
		self.play(
			ShrinkToCenter(brace),
			Uncreate(brace_tex)
		)

		factoriz = TexMobject(FACT_FORM).scale(EXPRESSION_SIZE).align_to(left_anchor, UL)
		brace = Brace(factoriz)
		brace_tex = brace.get_text(*FACT_TEXT)
		brace_tex[-1].set_color(YELLOW)

		self.play(ReplacementTransform(canonic, factoriz))
		self.play(
			GrowFromCenter(brace),
			ShowCreation(brace_tex)
		)
		self.wait()
		self.change_mode("confident")
		self.wait(4)
		self.play(
			FadeOut(factoriz),
			ShrinkToCenter(brace),
			Uncreate(brace_tex)
		)

# 5. MISTAKES TO AVOID
# -------------------------------------------------------------------
# VARIABLE GLOBAL
OLD_SUBTITLE2 = "Exemples"
SUBTITLE2 = "Erreur à éviter"
SUBTITLE_COLOR = BLUE
SUBTITLE_SCALE = 2
SUBTITLE_WRITING_TIME = 1
SUBTITLE_REDUCTION = 0.5

EXEMPLE = "5 x^2 -3 x + 2"
EXPRESSION_SIZE = 2
INFO_SIZE = 1.3
FADE_FACTOR = 0.65

TEXT = "Polynome du second degré"
NEW_TEXT = ["Polynome en "," désordre"]
TEXT_COLOR = GREY

STUDENT_SZIE = 0.7

class MistaketoAvoid(TeacherStudentsScene):
	CONFIG ={
		"student_colors": [GREY_BROWN],
        "teacher_color": SANDY_BROWN,
        "student_scale_factor": 0.7,
		"creatures_start_on_screen": False,
	}
	def construct(self):
		self.write_subtitle()
		self.messy_example()
	
	def write_subtitle(self):
		# 1. Subtitle & info 
		title_as_info = TextMobject(TITLE)
		title_as_info.scale(TITLE_SCALE*TITLE_REDUCTION).set_sheen(0.95).to_corner(DL, buff=SMALL_BUFF)
		old_subtitle = TextMobject(f"/ {OLD_SUBTITLE2}").scale(SUBTITLE_REDUCTION).set_color(SUBTITLE_COLOR)
		old_subtitle.next_to(title_as_info, buff=SMALL_BUFF)
		subtitle = TextMobject(SUBTITLE2, color=SUBTITLE_COLOR).scale(SUBTITLE_SCALE)
		subititle_as_info = TextMobject(f"/ {SUBTITLE2}", color=SUBTITLE_COLOR)
		subititle_as_info.scale(SUBTITLE_REDUCTION).next_to(title_as_info, buff=SMALL_BUFF)


		self.add(title_as_info, old_subtitle)
		self.play(Write(subtitle), run_time=SUBTITLE_WRITING_TIME)
		self.wait(0.5)
		self.play(
			Transform(subtitle, subititle_as_info),
			FadeOut(old_subtitle)
		)
		
	
	def messy_example(self):
		# 1. Display the example in order
		example = Expression(EXEMPLE).scale(EXPRESSION_SIZE)
		general_form = Expression("a x^2 + b x + c").fade(FADE_FACTOR).scale(EXPRESSION_SIZE)
		VGroup(example, general_form).arrange(DOWN, buff=0.8).shift(RIGHT).align_elm()

		self.play(Write(example))
		self.play(ReplacementTransform(example.copy(), general_form))
		self.wait()

		# 2. Shuffle the equation (2 times)
		x2, ax2 = example[:2], general_form[:2]
		x, bx = example[2:4], general_form[3:5]
		cst, c = example[4:], general_form[-1]

		new_x2 = Expression("+ 5 x^2").scale(EXPRESSION_SIZE)
		new_x2.next_to(cst, LEFT).align_to(cst,DOWN)
		new_x = x.copy().next_to(new_x2, LEFT).align_to(new_x2[-2],DOWN)

		new_ax2 = ax2.copy().align_to(bx, DL).shift(0.1*LEFT)
		new_bx = bx.copy().align_to(ax2, RIGHT)


		self.play(
			LaggedStart(
				AnimationGroup(
					ClockwiseTransform(x2, new_x2),
					ClockwiseTransform(x, new_x)
				),
				AnimationGroup(
					ClockwiseTransform(ax2, new_ax2),
					ClockwiseTransform(bx, new_bx)
				),
				lag_ratio = 0.8,
			)
		)

		new_cst = cst.copy().next_to(x, RIGHT).align_to(x, UP)
		new_x2 = x2.copy().next_to(new_cst).align_to(new_cst, DOWN)

		new_c = c.copy().align_to(ax2, DL)
		new_ax2 = VGroup(ax2,general_form[2]).copy().next_to(new_c).align_to(general_form[2], DOWN)


		self.play(
			LaggedStart(
				AnimationGroup(
					ClockwiseTransform(x2, new_x2),
					ClockwiseTransform(cst, new_cst)
				),
				AnimationGroup(
					ClockwiseTransform(ax2, new_ax2),
					ClockwiseTransform(c, new_c),
					FadeOut(general_form[-2])
				),
				lag_ratio = 0.8,
			)
		)

		general_form = VGroup(ax2,bx,c, general_form[2])

		# FadeOut the helper
		self.wait()
		self.play(
			*[FadeToColor(term, WHITE) for term in [x2,x ,cst]],
			*[FadeOut(general_form)]	
		)
		
		# Show the commun error of student
		braces = Brace(x[0], UP).fade(FADE_FACTOR)
		braces_text = braces.get_tex("a").scale(2).set_color(A_COLOR)
		bubble_content = TexMobject("a","= -3")
		bubble_content[0].set_color(A_COLOR)

		self.appears(self.students, target_mode="think")
		self.play(
			Write(braces), 
			GrowFromCenter(braces_text)
		)
		self.student_thinks(bubble_content, target_mode="confident")

		# correction from teacher
		self.appears(target_mode="normal")
		red_cross = Cross(Circle()).scale(0.5)
		self.wait(2)
		self.say(red_cross, target_mode="normal", keep_other_bubble=True)
		self.change_student_modes("sad")
		self.wait(3)
		self.play(RemoveBubble(self.teacher))
		self.wait()


		indication = Brace(x, DOWN)
		indication_text = indication.get_text("$1^{er}$ termes")
		indication = VGroup(indication, indication_text).set_color(YELLOW)

		self.play(ShowCreation(indication))
		self.play(Indicate(x[0], color=A_COLOR))
		self.play(Indicate(braces_text[0], color=A_COLOR, scale_factor=1.5))

		red_cross = Cross(braces_text)
		bubble_content = TexMobject("a","\\neq", "-3")
		bubble_content[0].set_color(A_COLOR)
		bubble_content[1].set_color(RED)

		self.wait(3)
		self.play(
			Uncreate(indication),
			FadeIn(general_form),
			ShowCreation(red_cross),
		)
		self.student_thinks(bubble_content)
		self.wait(4)
		self.play(
			FadeOut(general_form),
			RemoveBubble(self.students[0])
		)
		self.play(
			LaggedStart(
				FocusOn(x2[-1], color=A_COLOR),
				Indicate(x2[-1], color=A_COLOR),
				FadeToColor(x2[1], A_COLOR),
				lag_ratio = 0.5
			),
		)

		real_braces = Brace(x2[1], UP).fade(FADE_FACTOR)
		real_braces_text = real_braces.get_tex("a").scale(2).set_color(A_COLOR)
		bubble_content = TexMobject("a","= 5")
		bubble_content[0].set_color(A_COLOR)

		self.play(
			FadeOut(red_cross),
			ClockwiseTransform(braces, real_braces),
			ClockwiseTransform(braces_text, real_braces_text),
		)
		self.change_student_modes("happy")
		self.student_says(bubble_content, target_mode="cheerful")
		self.wait(5)

# 6. VISUALISATION
# -------------------------------------------------------------------
# VARIABLE GLOBAL
OLD_SUBTITLE3 = "Erreur à éviter"
SUBTITLE3 = "Visualisation"
SUBTITLE_COLOR = BLUE
SUBTITLE_SCALE = 2
SUBTITLE_WRITING_TIME = 1
SUBTITLE_REDUCTION = 0.5

EXPRESSION = "P(x) = a x^2 + b x + c"
EXPRESSION_SIZE = 1.5

PARABOLA_COLOR = YELLOW
PARABOLA_WRITING_TIME =1
GRAPH_FUNCT = [1,1,1]

COEF_POLYNOME_1 = [2,-3,2]
LABEL_1 = "f(x)"
COLOR_1 = PERSIAN_GREEN

COEF_POLYNOME_2 = [-1,-2,1]
LABEL_2 = "g(x)"
COLOR_2 = ORANGE_YELLOW

COEF_POLYNOME_3 = [0.1,0,-1]
LABEL_3 = "h(x)"
COLOR_3 = BURNT_SIENNA

# USEFUL MOBJECT
class Slider(VGroup):
	def __init__(self, color=BLUE, label="a"):
		self.line = Line().set_color(color)
		self.dot = Dot().scale(2)
		self.label = TexMobject(label).set_color(color).scale(2)
		self.label.next_to(self.line, LEFT)
		# self.decimal = DecimalNumber(num_decimal_places=1, include_sign=True)
		# mobjects = [self.line, self.dot, self.label, self.decimal]
		mobjects = [self.line, self.dot, self.label]
		super().__init__(*mobjects)

	# def update(self, multiplicative_factor=10):
	# 	self.decimal = self.decimal.add_updater(lambda d: d.set_value(multiplicative_factor*(self.dot.get_center()[0] - self.line.get_center()[0])+1))

class SimpleAxes(Axes):
	# TODO add the axis label
	CONFIG = {
		"axis_config": {
			"color": GREY,
		},
		"x_axis_config": {
		},
		"y_axis_config": {
		},
		"center_point": ORIGIN,
		"x_min" : -5,
		"x_max" : 5,
		"y_max" : 5,
		"y_min" : -5,
		# "x_axis_label": "x",
		# "y_axis_label": "x",
	}

	def get_graph_label(self, graph, label="f(x)", 
		x_val=None, direction=RIGHT, buff=MED_SMALL_BUFF, color=None,):
			label = TexMobject(label)
			color = color or graph.get_color()
			label.set_color(color)
			if x_val is None:
				# Search from right to left
				for x in np.linspace(self.x_max, self.x_min, 100):
					point = self.input_to_graph_point(x, graph)
					if point[1] < FRAME_Y_RADIUS:
						break
				x_val = x
			label.next_to(
				self.input_to_graph_point(x_val, graph),
				direction,
				buff=buff
			)
			label.shift_onto_screen()
			return label

# ANIMATION
class Visualisation(Scene):
	CONFIG = {
		"decimal_param": {
			"include_sign": True,
			"num_decimal_places": 1,
		}
	}
	def construct(self, **kwargs):
		digest_config(self, kwargs)
		self.write_subtitle()
		axes = self.update_curve()
		self.display_examples(axes)

	def write_subtitle(self):
		# 1. Subtitle & info 
		title_as_info = TextMobject(TITLE)
		title_as_info.scale(TITLE_SCALE*TITLE_REDUCTION).set_sheen(0.95).to_corner(DL, buff=SMALL_BUFF)
		old_subtitle = TextMobject(f"/ {OLD_SUBTITLE3}").scale(SUBTITLE_REDUCTION).set_color(SUBTITLE_COLOR)
		old_subtitle.next_to(title_as_info, buff=SMALL_BUFF)
		subtitle = TextMobject(SUBTITLE3, color=SUBTITLE_COLOR).scale(SUBTITLE_SCALE)
		subititle_as_info = TextMobject(f"/ {SUBTITLE3}", color=SUBTITLE_COLOR)
		subititle_as_info.scale(SUBTITLE_REDUCTION).next_to(title_as_info, buff=SMALL_BUFF)


		self.add(title_as_info, old_subtitle)
		self.play(Write(subtitle), run_time=SUBTITLE_WRITING_TIME)
		self.wait(0.5)
		self.play(
			Transform(subtitle, subititle_as_info),
			FadeOut(old_subtitle)
		)

	def update_curve(self):
		# 1. LEFT SIDE MOBJECTS
		# ----------------------------
		# 1.1 Sliders
		slider_a = Slider(A_COLOR, "a")
		slider_b = Slider(B_COLOR, "b")
		slider_c = Slider(C_COLOR, "c")
		parameters = VGroup(slider_a, slider_b, slider_c).arrange(DOWN, buff=0.5).align_elm()
		# 1.2 Moving Numbers
		a = DecimalNumber(**self.decimal_param).set_color(A_COLOR)
		b = DecimalNumber(**self.decimal_param)
		b[1:].set_color(B_COLOR)
		c = DecimalNumber(**self.decimal_param)
		c[1:].set_color(C_COLOR)
		coefs = [a,b, c]
		# 1.3 Link the position of the slider's dot with the moving numbers
		def create_updater(decimal, slider, factor=10):
			def set_value(decimal):
				x_dot = slider.dot.get_center()[0]
				x_line = slider.line.get_center()[0]
				value = factor * (x_dot - x_line)+1
				return decimal.set_value(value)
			return set_value
		
		for coef, slider in zip(coefs, parameters):
			set_value = create_updater(coef, slider)
			coef.add_updater(set_value)

		# 1.4 Create the expression 
		ax2 = VGroup(a, TexMobject("x^2")).arrange(RIGHT, buff=0.05).align_elm(direction=DOWN)
		bx = VGroup(b, TexMobject("x")).arrange(RIGHT, buff=0.05).align_elm(direction=DOWN)
		expression = VGroup(TexMobject("P(x)="), ax2, bx, c).scale(1.2)
		expression.scale(1.2).arrange(RIGHT, buff=0.15)
		expression.align_elm(expression[0][0][2],direction=DOWN)

		left_mobjects = VGroup(expression, parameters).arrange(DOWN, buff=1).align_elm()


		# ORGANISE LEFT AND RIGHT SIDE
		# ----------------------------
		axes = SimpleAxes().scale(0.6)
		VGroup(left_mobjects, axes).scale(0.9).arrange(buff=1)
		literal_expression = Expression(EXPRESSION).scale(EXPRESSION_SIZE).align_to(expression, DL)

		#  RIGHT SIDE
		# ----------------------------
		curve = axes.get_graph(
			lambda x: x**2 + x + 1, 
			color=PARABOLA_COLOR, 
		)
		label = axes.get_graph_label(curve, label="P(x)", x_val=1)
		parabola = VGroup(curve, label)

		minimun = axes.coords_to_point(- 1 / 2) # b/2a
		parallel_line = Line(start=minimun, end=minimun*10).rotate(TAU/4)
		parallel_line.move_to(minimun).set_color(SANDY_BROWN).fade()

		figure = VGroup(parabola, axes)
		right_mobjects = VGroup(figure)

		
		
		# ANIMATION
		# ----------------------------
		self.play(Write(literal_expression))
		self.wait()
		self.play(GrowFromCenter(axes))
		self.play(Write(parabola))
		# show parallelism
		self.play(FadeIn(parallel_line))
		self.play(Rotate(curve, axis=UP, about_point=minimun))
		self.play(FadeOut(parallel_line))
		self.wait(3)

		# link btw coefs and parabola
		self.play(WiggleOutThenIn(label, scale_factor=1.8)),
		self.play(
			WiggleOutThenIn(literal_expression[2], scale_value=1.5),
			WiggleOutThenIn(literal_expression[5], scale_value=1.5),
			WiggleOutThenIn(literal_expression[-1], scale_value=1.5)
		),
		self.play(
			ApplyMethod(literal_expression.set_opacity, 1),
			ApplyMethod(axes.set_opacity, 1)
		)
		self.wait(2)
		# # show interraction
		self.play(
			LaggedStart(
				self.slider_aparition(literal_expression, slider_a,"a"),
				self.slider_aparition(literal_expression, slider_b, "b"),
				self.slider_aparition(literal_expression, slider_c, "c"),
				lag_ratio = 0.1
			)
		)
		self.play(
			LaggedStart(
				FadeOutAndShift(literal_expression, RIGHT),
				FadeInFrom(expression, LEFT),
			lag_ratio = 0.4
			),
		)
		self.wait()

		# update the parabola with a,b,c
		def update_curve(curve):
			# critical_point = axes.y_max if a.get_value() > 0 else axes.y_min
			# roots = np.roots([a.get_value(), b.get_value(), c.get_value() - critical_point])
			# x_max, x_min = max(roots), min(roots)	
			curve = axes.get_graph(
						lambda x:a.get_value()*x**2 + b.get_value()*x + c.get_value(), 
						color=PARABOLA_COLOR,
						# x_min = x_min,
						# x_max = x_max
					)
			parabola.become(VGroup(curve, label))
		parabola.add_updater(update_curve)
		self.add(a, b, c)

		self.play(
			Indicate(slider_a.dot, scale_factor=1.5),
			Indicate(slider_b.dot, scale_factor=1.5),
			Indicate(slider_c.dot, scale_factor=1.5),
		),
		rate_func = there_and_back
		self.play(
			ApplyMethod(slider_a.dot.shift, LEFT, rate_func=rate_func), 
			ApplyMethod(slider_b.dot.shift, 0.6*RIGHT, rate_func=rate_func),
			ApplyMethod(slider_c.dot.shift, 0.3*RIGHT, rate_func=rate_func),
			run_time = 5
		), 
		self.wait(2)
		self.play(
			LaggedStart(
				*[FadeOut(mob)for mob in left_mobjects],
				FadeOut(parabola)
			)
		)
		return axes
		

	def display_examples(self, axes):
		# create algebrique expression &parabola
		a, b, c = COEF_POLYNOME_1
		expression_1 = Trinome2("f(x) = 2 x^2 -3 x + 2").set_color(COLOR_1)
		x_min, x_max = np.roots([a,b,c-axes.y_max])
		curve = axes.get_graph(lambda x: a*x**2+b*x+c, x_min=x_min, x_max=x_max, color =COLOR_1)
		label = axes.get_graph_label(curve, LABEL_1, x_val=2)
		parabola_1 = VGroup(curve, label)

		a, b, c = COEF_POLYNOME_2
		expression_2 = Trinome2("g(x) = - x^2 -2 x + 1").set_color(COLOR_2)
		x_min, x_max = np.roots([a,b,c-axes.y_min])
		curve = axes.get_graph(lambda x: a*x**2+b*x+c, x_min=x_min, x_max=x_max, color=COLOR_2)
		label = axes.get_graph_label(curve, LABEL_2, x_val=1)
		parabola_2 = VGroup(curve, label)
		
		a, b, c = COEF_POLYNOME_3
		expression_3 = Trinome2("h(x) = 0.1 x^2 -1").set_color(COLOR_3)
		curve = axes.get_graph(lambda x: a*x**2+b*x+c, color=COLOR_3)
		label = axes.get_graph_label(curve, LABEL_3, x_val=-4.5)
		parabola_3 = VGroup(curve, label)

		expressions =  VGroup(expression_1, expression_2, expression_3)
		expressions.scale(1.2).arrange(DOWN, buff= 1).align_elm().to_edge(LEFT)

		# animate
		# 1
		self.play(Write(expression_1))
		self.play(ShowCreation(parabola_1))
		# 2
		self.play(
			AnimationGroup(
				Write(expression_2),
				ApplyMethod(expression_1.set_opacity, 0.5),
				ApplyMethod(parabola_1[0].set_stroke, {"opacity":0.5}),
				ApplyMethod(parabola_1[1].set_opacity, {"opacity":0.5}),
				lag_ratio = 0.2

			)
		)
		self.play(ShowCreation(parabola_2))
		# 3
		self.play(
			AnimationGroup(
				Write(expression_3),
				ApplyMethod(expression_2.set_opacity, 0.5),
				ApplyMethod(parabola_2[0].set_stroke, {"opacity":0.5}),
				ApplyMethod(parabola_2[1].set_opacity, {"opacity":0.5}),
				lag_ratio = 0.2

			)
		)
		self.play(ShowCreation(parabola_3))

		self.wait()
		self.play(
			AnimationGroup(
				ApplyMethod(expression_1.set_opacity, 1),
				ApplyMethod(parabola_1[0].set_stroke, {"opacity":1}),
				ApplyMethod(parabola_1[1].set_opacity, {"opacity":1}),
				ApplyMethod(expression_2.set_opacity, 1),
				ApplyMethod(parabola_2[0].set_stroke, {"opacity":1}),
				ApplyMethod(parabola_2[1].set_opacity, {"opacity":1})
			)
		)
		self.wait(3)

	
	# SUBPROCESSE
	# ----------------
	def slider_aparition(self, expression, slider, coef):
		if coef == "a":
			i =2
		elif coef == "b":
			i = 4
		else:
			i=-1
		return AnimationGroup(
				TransformFromCopy(expression[i],Group(slider.line,slider.label)),
				FadeIn(slider.dot),
				lag_ratio = 1
			)

# 7. RESUMÉ
# -------------------------------------------------------------------
# VARIABLE GLOBAL
OLD_SUBTITLE4 = "Visualisation"
SUBTITLE4 = "Résumé"
SUBTITLE_COLOR = BLUE
SUBTITLE_SCALE = 2
SUBTITLE_WRITING_TIME = 1
SUBTITLE_REDUCTION = 0.5

EXPRESSION_SIZE = 1.5
EXPRESSION_1 = [3,2,-3]
EXPRESSION_2 = [-0.5,1,4]
LABEL_2 = "g(x)"
EXPRESSION_3 = [1,-3,1]
LABEL_3 = "h(x)"
FADE = 0.85

PARABOLA_COLOR = YELLOW
# ANIMATION
class Resume(Scene):
	def construct(self):
		self.write_subtitle()
		self.resume()

	def write_subtitle(self):
		# 1. Subtitle & info 
		title_as_info = TextMobject(TITLE)
		title_as_info.scale(TITLE_SCALE*TITLE_REDUCTION).set_sheen(0.95).to_corner(DL, buff=SMALL_BUFF)
		old_subtitle = TextMobject(f"/ {OLD_SUBTITLE4}").scale(SUBTITLE_REDUCTION).set_color(SUBTITLE_COLOR)
		old_subtitle.next_to(title_as_info, buff=SMALL_BUFF)
		subtitle = TextMobject(SUBTITLE4, color=SUBTITLE_COLOR).scale(SUBTITLE_SCALE)
		subititle_as_info = TextMobject(f"/ {SUBTITLE4}", color=SUBTITLE_COLOR)
		subititle_as_info.scale(SUBTITLE_REDUCTION).next_to(title_as_info, buff=SMALL_BUFF)


		self.add(title_as_info, old_subtitle)
		self.play(Write(subtitle), run_time=SUBTITLE_WRITING_TIME)
		self.wait(0.5)
		self.play(
			Transform(subtitle, subititle_as_info),
			FadeOut(old_subtitle)
		)
	
	def resume(self):
		## CREATES THE MOBJECTS
		## --------------------
		axes = SimpleAxes()
		# example 1
		a,b,c = EXPRESSION_1
		expression_1 = Trinome3(a,b,c, in_color=False).scale(EXPRESSION_SIZE)
		braces = []
		x_min, x_max = np.roots([a,b,c-axes.y_max])
		curve = axes.get_graph(lambda x: a*x**2+b*x+c, color=PARABOLA_COLOR, x_min=x_min, x_max=x_max)
		label = axes.get_graph_label(curve, x_val = 1).scale(2).shift(0.5*RIGHT)
		parabola_1 = VGroup(curve, label)

		# example 2
		a,b,c = EXPRESSION_2
		expression_2 = Trinome3(a,b,c, label=LABEL_2).scale(EXPRESSION_SIZE)
		x_min, x_max = np.roots([a,b,c-axes.y_min])
		curve = axes.get_graph(lambda x: a*x**2+b*x+c, color=PARABOLA_COLOR, x_min=x_min, x_max=x_max)
		label = axes.get_graph_label(curve, label=LABEL_2, x_val = 1).scale(2).shift(0.4*TOP+RIGHT)
		parabola_2 = VGroup(curve, label)

		# example 3
		a,b,c = EXPRESSION_3
		expression_3 = Trinome3(a,b,c, label=LABEL_3).scale(EXPRESSION_SIZE)
		x_min, x_max = np.roots([a,b,c-axes.y_max])
		curve = axes.get_graph(lambda x: a*x**2+b*x+c, color=PARABOLA_COLOR, x_min=x_min, x_max=x_max)
		label = axes.get_graph_label(curve, label=LABEL_3, x_val = 1).scale(2).shift(1.3*RIGHT+0.7*DOWN)
		parabola_3 = VGroup(curve, label)
		
		expressions = VGroup(expression_1, expression_2, expression_3)
		graph = VGroup(axes, parabola_1, parabola_2, parabola_3).scale(0.4)
		
		# position
		graph.to_edge(RIGHT)
		expressions.arrange(DOWN, buff=0.7).align_elm().to_edge()
		expressions.align_to(axes, UP)
		link = TexMobject("\Leftrightarrow").scale(3).next_to(graph,1.7*LEFT)

		# create the braces for the coef a,b,c
		zip_list = zip(expression_1.get_coefs(), ["a", "b", "c"], [A_COLOR, B_COLOR, C_COLOR])
		for (coef, text, color) in zip_list:
			brace = Brace(coef)
			brace_text = brace.get_tex(text).set_color(color).scale(2).shift(0.2*DOWN)
			braces += [VGroup(brace, brace_text)]
		brace_text = VGroup(*[brace[1] for brace in braces])
		brace_text.align_elm(brace_text[1], DOWN)
			
		# function to move to middle and bright
		def move_to_midle(mob):
			mob.align_to(expression_2, DL)
			mob.set_opacity(1)
			return mob
		

		# ANIMATION
		# ---------
		self.wait()
		self.play(Write(expression_1))
		self.wait(2)

		# 1. animate first term
		self.play(WiggleOutThenIn(expression_1.ax2),)
		self.play(
			LaggedStart(
				Indicate(expression_1.x2, color=A_COLOR),
				LaggedStart(
					FocusOn(expression_1.a, color=A_COLOR),
					ApplyMethod(expression_1.a.set_color, A_COLOR),
					GrowFromCenter(braces[0][0]),
					Write(braces[0][1]),
					lag_ratio = 0.5
				),
				lag_ratio = 0.9
			)
		)
		# 2. animate the second term
		self.play(WiggleOutThenIn(expression_1.bx),)
		self.play(
			LaggedStart(
				Indicate(expression_1.x, color=B_COLOR),
				LaggedStart(
					FocusOn(expression_1.b, color=B_COLOR),
					ApplyMethod(expression_1.b.set_color, B_COLOR),
					GrowFromCenter(braces[1][0]),
					Write(braces[1][1]),
					lag_ratio = 0.5
				),
				lag_ratio = 0.9
			)
		)
		# 3. animate the third term
		self.play(
			LaggedStart(
				FocusOn(expression_1.c, color=C_COLOR),
				ApplyMethod(expression_1.c.set_color, C_COLOR),
				GrowFromCenter(braces[2][0]),
				Write(braces[2][1]),
				lag_ratio = 0.5
			),
		)

		# 4. show link with parabola
		self.wait(3)
		self.play(
			LaggedStart(
				*[Indicate(coef) for coef in expression_1.get_coefs()],
				lag_ratio = 0.6
			)
		)
		self.play(
			LaggedStart(
				GrowFromCenter(axes),
				Write(parabola_1),
				lag_ratio = 0.9
			)
		)
		# Shoe the different exemples
		self.wait(2)
		self.play(LaggedStart(*[ShrinkToCenter(brace) for brace in braces], lag_ratio=0.1))
		self.wait(4)
		self.play(
			LaggedStart(
				AnimationGroup(
					ApplyMethod(parabola_1.fade, FADE),
					ApplyMethod(expression_1.fade, FADE)
				),
				Write(expression_2),
				Write(parabola_2),
				lag_ratio = 0.9
			)
		)
		self.wait(2)
		self.play(
			LaggedStart(
				AnimationGroup(
					ApplyMethod(parabola_2.fade, FADE),
					ApplyMethod(expression_2.fade, FADE)
				),
				Write(expression_3),
				Write(parabola_3),
				lag_ratio = 0.9
			)
		)
		self.wait(2)
		self.play(
			LaggedStart(
				ApplyFunction(move_to_midle, expression_3),
				FadeOut(expression_1), 
				FadeOut(expression_2),
				FadeOut(parabola_1),
				FadeOut(parabola_2),
				run_time=2
			),
		)
		self.wait(0.5)
		self.play(ShowCreationThenFadeOut(link),run_time=2)
		self.wait(2)
		self.play(
			LaggedStart(
				FocusOn(expression_3.a, color=A_COLOR),
				WiggleOutThenIn(expression_3.a, scale_factor=2),
				lag_ratio = 0.5
			)
		)
		

		# UPDATE EXPRESSION THEN PARABOLA
		a = 9
		roots = np.roots([a, b, c - axes.y_max])
		x_max, x_min = max(roots), min(roots)	
		updated_curve = axes.get_graph(lambda x:a*x**2 + b*x +c, x_min = x_min, x_max = x_max)
		updated_curve.set_color(PARABOLA_COLOR)
		updated_label = axes.get_graph_label(updated_curve, x_val=0, label=LABEL_3)

		self.wait(2)
		self.play(
			ChangeDecimalToValue(expression_3.a, a),
		)
		self.wait()
		self.play(FocusOn(parabola_3))
		self.wait()
		self.play(
			Transform(curve, updated_curve),
			Transform(label, updated_label)
		)
		self.wait(3)

		# UPDATE PARABOLA THEN EXPRESSION
		a, b, c = -1, -2, 3
		roots = np.roots([a, b, c - axes.y_min])
		x_max, x_min = max(roots), min(roots)	
		updated_curve = axes.get_graph(lambda x:a*x**2 + b*x +c, x_min = x_min, x_max = x_max)
		updated_curve.set_color(PARABOLA_COLOR)
		updated_label = axes.get_graph_label(updated_curve, x_val=0.5, label=LABEL_3)

		self.play(
			Transform(curve, updated_curve),
			Transform(label, updated_label)
		)
		self.wait()
		self.play(*[Indicate(coef) for coef in expression_3.get_coefs()])
		self.wait()
		self.play(
			ChangeDecimalToValue(expression_3.a, a),
			ChangeDecimalToValue(expression_3.b, b),
			ChangeDecimalToValue(expression_3.c, c)
		)
		self.wait(5)


# 8. OBJECTIF DU COURS
# -------------------------------------------------------------------
# VARIABLE GLOBAL
OLD_SUBTITLE = "Résumé"
SUBTITLE = "Objectif du cours"
SUBTITLE_COLOR = BLUE
SUBTITLE_SCALE = 2
SUBTITLE_WRITING_TIME = 1
SUBTITLE_REDUCTION = 0.5

TITLE_1 = "Caracatéristiques Importantes-"
TITLE_SIZE = 1.8

FEATURE_1 = "1. Sens de Variation"
FEATURE_2 = "2. Sommet"
FEATURE_3 = "3. Racines"
TITLE_BUFF = 0.5

COEFS = [1,-4,3.5]
PARABOLA_COLOR = BLUE_B
FEATURE_COLOR = YELLOW
AXES_BUFF = 1.2
FADE = 0.8

EXO_COLOR_1 = PERSIAN_GREEN
EXO_COLOR_2 = LIGHT_PINK

FEATURE_1B = "Variation"
FEATURE_2B = "Sommet"
FEATURE_3B = "Racines"

# ANIMATION
class Goals(AlexScene):
	CONFIG = {
		"creatures_start_on_screen": False,
		"default_creature_kwargs": {
			"color": SANDY_BROWN,
			"mode": "think"
		}
	}
	def construct(self):
		self.write_title(OLD_SUBTITLE, SUBTITLE)
		self.create_scene()
		self.variation()
		self.vertex()
		self.roots()
		self.clear()
		self.exercises()
		self.link_wth_expression()

	def write_title(self, old_title, title):
		# 1. Subtitle & info 
		title_as_info = TextMobject(TITLE)
		title_as_info.scale(TITLE_SCALE*TITLE_REDUCTION).set_sheen(0.95).to_corner(DL, buff=SMALL_BUFF)
		old_subtitle = TextMobject(f"/ {old_title}").scale(SUBTITLE_REDUCTION).set_color(SUBTITLE_COLOR)
		old_subtitle.next_to(title_as_info, buff=SMALL_BUFF)
		subtitle = TextMobject(title, color=SUBTITLE_COLOR).scale(SUBTITLE_SCALE)
		subititle_as_info = TextMobject(f"/ {title}", color=SUBTITLE_COLOR)
		subititle_as_info.scale(SUBTITLE_REDUCTION).next_to(title_as_info, buff=SMALL_BUFF)


		self.add(title_as_info, old_subtitle)
		self.play(Write(subtitle), run_time=SUBTITLE_WRITING_TIME)
		self.wait(0.5)
		self.play(
			Transform(subtitle, subititle_as_info),
			FadeOut(old_subtitle)
		)

	def create_scene(self):
		# Text Mobject
		annotation = Title(TITLE_1, scale_factor=TITLE_SIZE)
		features = BulletedList(FEATURE_1, FEATURE_2, FEATURE_3, dot_scale_factor=0, buff=0.4)
		features.scale(1.5).to_edge(buff=TITLE_BUFF)
		
		# Graph
		a,b,c = COEFS
		axes = SimpleAxes(y_min=-1, x_min=-1).scale(0.8).to_corner(DR, buff=AXES_BUFF)
		self.x_min, self.x_max = np.roots([a,b,c-axes.y_max])
		curve = axes.get_graph(lambda x: a*x**2 + b*x + c,x_min=self.x_min, x_max=self.x_max)
		curve.set_color(PARABOLA_COLOR)
		label = axes.get_graph_label(curve, x_val=3)
		parabola = VGroup(curve,label)

		# animate
		self.play(
			LaggedStart(
				Write(annotation),
				FadeIn(axes),
				Write(parabola),
				lag_ratio = 0.6,
				run_time = 1.5
			)
		)
		self.wait(3)

		# create self variable
		self.parabola = parabola
		self.axes = axes
		self.features = features
		self.annotation = annotation
	
	def variation(self):
		curve = self.parabola[0]
		feature = self.features[0]
		ball = ball = Dot(curve.get_start(), color=FEATURE_COLOR).scale(2)

		self.play(FadeInFrom(feature, LEFT))
		self.play(
			Succession(
				GrowFromCenter(ball),
				MoveAlongPath(ball, curve),
				ShrinkToCenter(ball),
			),
			run_time = 6
		)
	
	def vertex(self):
		curve = self.parabola[0]
		feature = self.features[1]
		old_features = self.features[0]
		axes = self.axes

		# add vertex and lines
		a,b,_= COEFS
		x_coord = -b/(2*a)
		y_cord = np.polyval(COEFS, x_coord)
		vertex = Dot(axes.input_to_graph_point(x_coord, curve)).set_color(FEATURE_COLOR)
		vertex.scale(2)
		x_point = Dot(axes.x_axis.number_to_point(x_coord))
		y_point = Dot(axes.y_axis.number_to_point(y_cord))
		vertical_line = DashedLine(start=vertex, end=x_point)
		horizontal_line = DashedLine(start=vertex, end=y_point)
		symbol = TexMobject("S", color=FEATURE_COLOR).scale(1.4).next_to(vertex, DOWN)

		self.play(
			FadeInFrom(feature, LEFT),
			ApplyMethod(old_features.fade, FADE)
		)

		self.play(
			LaggedStart(
				GrowFromCenter(vertex),
				AnimationGroup(
					ShowCreation(vertical_line),
					ShowCreation(horizontal_line)
				),
				GrowFromCenter(symbol),
				lag_ratio = 0.8,
				run_time=2
			)
		)
		self.wait(2)
		self.play(
			ShrinkToCenter(vertex),
			ShrinkToCenter(symbol),
			Uncreate(horizontal_line),
			Uncreate(vertical_line),
		)
		self.wait()

	def roots(self):
		curve = self.parabola[0]
		feature = self.features[2]
		old_features = self.features[1]
		axes = self.axes

		root2, root1 = np.roots(COEFS)
		x1 = Dot(axes.coords_to_point(root1), color=FEATURE_COLOR).scale(2)
		x2 = Dot(axes.coords_to_point(root2), color=FEATURE_COLOR).scale(2)
		symbol1 = TexMobject("r_1", color=FEATURE_COLOR).scale(1.2).next_to(x1, DOWN)
		symbol2 = TexMobject("r_2",  color=FEATURE_COLOR).scale(1.2).next_to(x2, DOWN)

		self.play(
			FadeInFrom(feature, LEFT),
			ApplyMethod(old_features.fade, FADE)
		)
		self.wait()
		self.play(
			LaggedStart(
				GrowFromCenter(x1),
				GrowFromCenter(symbol1), 
				GrowFromCenter(x2),
				GrowFromCenter(symbol2),
				lag_ratio = 0.1
			),
		)
		self.wait(2)
		self.play(
			ShrinkToCenter(x1),
			ShrinkToCenter(x2),
			FadeOut(symbol1),
			FadeOut(symbol2)
		)

	def clear(self):
		heart = Heart().scale(2).to_edge(RIGHT, buff=3)
		self.play(
			LaggedStart(
				Uncreate(self.parabola),
				ApplyMethod(self.features.set_opacity, 1),
				FadeOut(self.axes),
				Write(heart),
				lag_ratio = 0.3
			)
		)
		self.wait(4)
		self.play(
			ShrinkToCenter(heart),
			FadeOut(self.features),
			FadeOut(self.annotation)
		)
		self.play(FadeOut(heart), run_time=0.2)

	def exercises(self):
		# 1. EXO 1
		# --------
		expression = Expression("P(x) = 3 x^2 -2 x + 4", in_color=False).scale(1.8)
		questions = BulletedList(
			"1. Trouver les racines de $P$",
			"3. Trouver le sommet $S$ du polynome",
			dot_scale_factor = 0
		)
		exercise = VGroup(expression,questions).arrange(DOWN, buff=1).align_elm()
		background = SurroundingRectangle(exercise, color=EXO_COLOR_1, buff=0.5)
		title = TextMobject("Exercice 1").scale(SUBTITLE_SCALE).next_to(background, UP)
		title[0][-1].set_color(EXO_COLOR_1)
		board = VGroup(title, background, exercise)
		# get special word
		roots = questions[0][13:20]
		vertex = questions[1][12:18]

		# animate
		self.wait(1.5)
		self.play(
			FadeInFrom(title),
			FadeInFrom(background)
		)
		self.wait(0.5)
		self.play(Write(expression))
		self.wait()
		self.play(Write(questions))
		self.appears(run_time = 0.5)
		self.wait(3)
		self.play(ApplyMethod(expression.set_color_coef))
		self.wait(0.5)
		self.play(
			FadeToColor(roots, FEATURE_COLOR),
			ApplyWave(roots)
		)
		self.play(
			FadeToColor(vertex, FEATURE_COLOR),
			ApplyWave(vertex)
		)
		self.wait(3)
		self.play(FadeOutAndShift(board, UP))

		# 2. EXO 2
		# --------		
		sentence_1 = TextMobject("Soit le polynome $P$ tels que:").scale(1.2)
		sentence_2 = BulletedList(
			"3 et 1 racines de P",
			"$S$ le sommet de la parabole pour $x=2$",
		)
		sentence = VGroup(sentence_1, sentence_2).arrange(DOWN, buff=0.5).align_elm()
		question = TextMobject("Trouver ","a,"," b,"," c").scale(1.5)
		question[1][0].set_color(A_COLOR)
		question[2][0].set_color(B_COLOR)
		question[3].set_color(C_COLOR)

		exercise = VGroup(sentence, question).arrange(DOWN, buff=1).align_elm()
		background = SurroundingRectangle(exercise, color=EXO_COLOR_2, buff=0.5)
		title = TextMobject("Exercice 2").scale(SUBTITLE_SCALE).next_to(background, UP)
		title[0][-1].set_color(EXO_COLOR_2)
		board = VGroup(title, background, exercise)
		# select word
		roots = sentence_2[0][5:12]
		r12 = VGroup(sentence_2[0][1], sentence_2[0][4])
		vertex = sentence_2[1][4:10]
		x_vertex = sentence_2[1][26:29]

		self.play(
			FadeInFrom(title),
			FadeInFrom(background)
		)
		self.play(
			Write(sentence),
			ApplyMethod(self.creature.change_mode, "think_2")
		)
		self.wait(0.5)
		self.play(Write(question))
		self.wait(5)
		self.play(
			LaggedStart(
				*[Indicate(r) for r in r12[::-1]], 
				FadeToColor(r12, FEATURE_COLOR),
				lag_ratio = 0.3
			)
		)
		self.wait(1.5)
		self.play(
			LaggedStart(
				Indicate(x_vertex), 
				FadeToColor(x_vertex, FEATURE_COLOR),
				lag_ratio = 0.3
			)
		)
		self.wait(4)
		self.disappears()
		self.wait()
		self.play(FadeOut(board))
	
	def link_wth_expression(self):
		# create tools 
		tool = Tool(fill_opacity=0.5).scale(2)
		tools = VGroup(tool.copy(), tool, tool.copy()).arrange(buff=INTER_BUFF)

		def make_it_smaller(mob):
			mob.scale(0.6)
			mob.to_edge(UP)
			mob.fade(0.6)
			return mob


		# create vertical expression
		features = BulletedList(
			FEATURE_1B, FEATURE_2B, FEATURE_3B, 
			dot_scale_factor=0, 
			buff=0.7
		)
		features.scale(1.5).to_edge(buff=TITLE_BUFF).shift(0.3*DOWN)
		expression = Expression("a x^2 + b x + c").scale(2).to_edge(RIGHT, buff=AXES_BUFF)
		ax2 = expression[:2]
		plus_sign = expression[2]
		bx = expression[3:5]
		plus_sign2 = expression[5]
		c = expression [6] 
		expression = VGroup(ax2, plus_sign, bx, plus_sign2, c)
		def make_it_vertical(mob):
			mob.arrange(DOWN).shift(0.3*DOWN)
			mob.to_edge(RIGHT, buff=AXES_BUFF)
			mob[1].fade(1)
			mob[3].fade(1)
			return mob
		
		# ANIMATE #1
		
		self.play(FadeInFromLarge(tools))
		self.wait()
		self.play(
			ApplyFunction(make_it_smaller, tools))
		self.play(FadeInFrom(expression), run_time = 0.3)
		self.wait(0.5)
		self.play(ApplyFunction(make_it_vertical, expression), run_time = 0.3)
		self.wait()
		self.play(Write(features))

		# create lefts dots
		dot_size = 1.5
		variation_pt = Dot().next_to(features[0]).scale(dot_size)
		roots_pt = Dot().next_to(features[2]).scale(dot_size)
		vertex_pt = Dot().next_to(features[1]).scale(dot_size)
		left_pts = VGroup(variation_pt, roots_pt, vertex_pt).align_elm(direction=RIGHT)#.set_color(GREY)
		# create right dots
		ax2_pt = Dot().next_to(ax2[0], LEFT).scale(dot_size).set_color(A_COLOR)
		bx_pt = Dot().next_to(bx, LEFT).scale(dot_size).set_color(B_COLOR)
		c_pt = Dot().next_to(c, LEFT).scale(dot_size).set_color(C_COLOR)
		right_pts = VGroup(ax2_pt, bx_pt, c_pt).align_elm()

		pts = VGroup(left_pts, right_pts).fade()

		# create links
		variation_links = Line(variation_pt, ax2_pt).set_color(A_COLOR)
		link1 = Line(vertex_pt, ax2_pt).set_color_by_gradient(A_COLOR)
		link2 = Line(vertex_pt, bx_pt).set_color(B_COLOR)
		vertex_links = VGroup(link1, link2)
		link1 = Line(roots_pt, ax2_pt).set_color(A_COLOR)
		link2 = Line(roots_pt, bx_pt).set_color(B_COLOR)
		link3 = Line(roots_pt, c_pt).set_color(C_COLOR)
		roots_links = VGroup(link1, link2, link3)
		links = VGroup(variation_links, vertex_links, roots_links).fade()

		# ANIMATE #2
		# tool 1
		self.play(
			LaggedStart(
				*[GrowFromCenter(dot) for dot in right_pts], 
				lag_ratio = 0.1,
				run_time =1
			)
		)
		self.play(ApplyMethod(tools[0].set_opacity, 1), run_time=0.2)
		run_time = 1
		self.play(
			GrowFromCenter(variation_pt),
			ShowCreation(variation_links),
			run_time = run_time
		),
		self.wait()
		# tool 2
		self.play(
			ApplyMethod(tools[0].fade, 0.6),
			ApplyMethod(tools[1].set_opacity, 1), 
			run_time=0.2
		)
		self.play(
			LaggedStart(
				ApplyMethod(variation_links.fade, FADE),
				ApplyMethod(variation_pt.fade, FADE),
				GrowFromCenter(vertex_pt),
				ShowCreation(vertex_links)
			),
			run_time = 2*run_time/3
		),
		self.wait()
		# tool 3
		self.play(
			ApplyMethod(tools[1].fade, 0.6),
			ApplyMethod(tools[2].set_opacity, 1), 
			run_time=0.2
		)
		self.play(
			GrowFromCenter(roots_pt),
			ShowCreation(roots_links),
			ApplyMethod(vertex_links.fade, FADE),
			ApplyMethod(vertex_pt.fade, FADE),
			run_time = run_time/3
		)
		self.play(
			FadeOut(features),
			FadeOut(expression),
			FadeOut(tools),
			FadeOut(links),
			FadeOut(pts)
		)

	
# 9. Sommaire
# -------------------------------------------------------------------
# VARIABLE GLOBAL
SCREEN_SIZE = 5.5
COEFS = [1,-4,3.5]
INTER_BUFF = 1.5

class Summary(AlexScene):
	CONFIG = {
		"creatures_start_on_screen": False,
		"default_creature_kwargs": {
			"color": SANDY_BROWN,
			"mode": "think"
		}
	}

	def construct(self):
		self.create_mobjects()
		self.video_variation()
		self.video_roots()
		self.video_vertex()

	def create_mobjects(self):
		# Create the graph
		a,b,c = COEFS
		axes = SimpleAxes(y_min=-1, x_min=-1).scale(0.8)
		self.x_min, self.x_max = np.roots([a,b,c-axes.y_max])
		curve = axes.get_graph(
			lambda x: a*x**2 + b*x + c,
			x_min=self.x_min, 
			x_max=self.x_max
		)
		curve.set_color(PARABOLA_COLOR)
		label = axes.get_graph_label(curve, x_val=3)
		parabola = VGroup(curve,label)
		graph = VGroup(axes, parabola)

		# create the screen and elm inside
		screen = ScreenRectangle()
		board = VGroup(graph, graph.copy())\
			.scale(0.8)\
			.arrange(buff=INTER_BUFF)\
			.shift(0.3*DOWN)
		screen.surround(board, buff= 0.8)

		# create attr
		self.parabola = parabola
		self.axes = axes
		self.screen = screen

	def video_variation(self):
		screen = self.screen
		curve = self.parabola[0]
		axes = self.axes
		graph = VGroup(axes, self.parabola)

		# 1. TITLE & ANNOTATION
		name = TextMobject("Vidéo 2: Sens de variation et ").scale(1.3)
		coef = TexMobject("a", color=A_COLOR).scale(1.7)
		title = VGroup(name, coef)\
			.arrange(buff=0.2)\
			.next_to(screen, UP)\
			.align_elm(direction=DOWN)
		annotation = TexMobject("a",">","0").next_to(screen.get_top(), DOWN)
		annotation[0].set_color(A_COLOR)

		# RIGHT MOBJECT
		a,b,c = COEFS
		x_vertex = -b/(2*a)
		# split the curve in two pieces 
		starting_point = Dot(curve.get_start())
		ending_point = Dot(curve.get_end())
		min_point = Dot(axes.input_to_graph_point(x_vertex,curve))

		descending_curve = axes.get_graph(
			lambda x: a*x**2 + b*x + c,
			x_min = x_vertex, 
			x_max = self.x_max
		)
		descending_part = VGroup(descending_curve, starting_point, min_point)

		ascending_curve = axes.get_graph(
			lambda x: a*x**2 + b*x + c,
			x_min = self.x_min, 
			x_max = x_vertex
		)
		ascending_part = VGroup(ascending_curve, ending_point, min_point)

		VGroup(descending_curve, ascending_curve).set_color(curve.get_color())
		VGroup(descending_part, ascending_part).next_to(graph, buff=INTER_BUFF)
		ball = Dot(curve.get_start(), color=FEATURE_COLOR).scale(4)

		# Create arrow
		descending_arrow = Arrow(start=starting_point, end=min_point)\
			.set_color(PARABOLA_COLOR)
		ascending_arrow = Arrow(start=min_point, end=ending_point)\
			.set_color(PARABOLA_COLOR)

		# ANIMATE
		self.play(
			Write(title),
			FadeIn(screen),
			FadeIn(axes)
		)
		self.wait()
		self.play(Write(self.parabola))
		self.play(
			AnimationGroup(
				LaggedStart(
					FadeIn(ball),
					MoveAlongPath(ball, curve),
					lag_ratio = 0.3,
					run_time=2
				),
				LaggedStart(
					FadeIn(starting_point),
					GrowArrow(descending_arrow),
					FadeIn(min_point),
					GrowArrow(ascending_arrow),
					FadeIn(ending_point),
					Write(annotation),
					lag_ratio = 0.9,
					run_time=2
				)
			)
		)
		self.wait()
		self.play(
			FadeOut(ball),
			ShrinkToCenter(starting_point),
			ShrinkToCenter(ending_point),
			ShrinkToCenter(min_point),
			ShrinkToCenter(descending_arrow),
			ShrinkToCenter(ascending_arrow),
			Uncreate(title),
			FadeOut(annotation)
		)	

	def video_roots(self):
		screen = self.screen
		curve = self.parabola[0]
		axes = self.axes
		graph = VGroup(axes, self.parabola)

		# 1. TITLE & ANNOTATION
		name = TextMobject("Vidéo 3: Les Racines et ").scale(1.3)
		coef = TexMobject("\Delta").scale(1.7)\
			.set_color_by_gradient([A_COLOR, C_COLOR, B_COLOR])
		title = VGroup(name, coef)\
			.arrange(buff=0.2)\
			.next_to(screen, UP)\
			.align_elm(direction=DOWN)
		
		# CURVE
		root2, root1 = np.roots(COEFS)
		x1 = Dot(axes.coords_to_point(root1), color=FEATURE_COLOR).scale(2)
		x2 = Dot(axes.coords_to_point(root2), color=FEATURE_COLOR).scale(2)

		exp1 = TexMobject(r"r_1=\frac{-b+\sqrt{\Delta}}{2a}")
		exp2 = TexMobject(r"r_2=\frac{-b+\sqrt{\Delta}}{2a}")
		result = VGroup(exp1, exp2).arrange(DOWN, buff=1).next_to(graph, buff=INTER_BUFF)
		symbol1 = TexMobject("r_1", color=FEATURE_COLOR).scale(1.2).next_to(x1, DOWN)
		symbol2 = TexMobject("r_2",  color=FEATURE_COLOR).scale(1.2).next_to(x2, DOWN)

		def apply_color(mob):
			mob[0][:2].set_color(FEATURE_COLOR)
			mob[0][4].set_color(B_COLOR)
			mob[0][-1].set_color(A_COLOR)
			mob[0][8].set_color_by_gradient([A_COLOR, C_COLOR, B_COLOR])
			return mob

		# ANIMATION
		self.play(Write(title))
		self.play(
			LaggedStart(
				GrowFromCenter(x1),
				GrowFromCenter(symbol1), 
				GrowFromCenter(x2),
				GrowFromCenter(symbol2),
				lag_ratio = 0.1
			),
		)
		self.wait()
		self.play(
			LaggedStart(
				ReplacementTransform(x1.copy(), exp1),
				ReplacementTransform(x2.copy(), exp2),
				lag_ratio = 0.5
			)
		)
		self.play(
			LaggedStart(
				ApplyFunction(apply_color, exp1),
				ApplyFunction(apply_color, exp2)
			)
		)
		self.wait()
		self.play(
			FadeOut(result),
			ShrinkToCenter(x1),
			ShrinkToCenter(x2),
			ShrinkToCenter(symbol1),
			ShrinkToCenter(symbol2),
			Uncreate(title)
		)
		

	def video_vertex(self):
		screen = self.screen
		curve = self.parabola[0]
		axes = self.axes
		graph = VGroup(axes, self.parabola)

		# 1. TITLE & ANNOTATION
		title = TextMobject("Vidéo 4: Sommet et coefs a, b")\
			.scale(1.3)\
			.next_to(screen,UP)
		title[0][-1].set_color(B_COLOR)
		title[0][-3].set_color(A_COLOR)
		
		# add vertex and lines
		a,b,_= COEFS
		x_coord = -b/(2*a)
		y_cord = np.polyval(COEFS, x_coord)
		vertex = Dot(axes.input_to_graph_point(x_coord, curve)).set_color(FEATURE_COLOR)
		vertex.scale(2)
		x_point = Dot(axes.x_axis.number_to_point(x_coord))
		y_point = Dot(axes.y_axis.number_to_point(y_cord))
		vertical_line = DashedLine(start=vertex, end=x_point)
		horizontal_line = DashedLine(start=vertex, end=y_point)
		symbol = TexMobject("S", color=FEATURE_COLOR).scale(1.4).next_to(vertex, DOWN)

		# add annotation
		vf = r"\frac{-b}{2a}"
		annotation = TexMobject(rf"S\left({vf}, f\left({vf}\right)\right)")
		annotation.scale(1.2).next_to(graph, buff=0.5)
		annotation[0][0].set_color(FEATURE_COLOR)

		# animate
		self.play(Write(title))
		self.play(
			LaggedStart(
				GrowFromCenter(vertex),
				AnimationGroup(
					ShowCreation(vertical_line),
					ShowCreation(horizontal_line)
				),
				GrowFromCenter(symbol),
				lag_ratio = 0.8,
				run_time=2
			)
		)
		self.play(ReplacementTransform(vertex.copy(),annotation))
		self.play(
			annotation[0][3].set_color, B_COLOR,
			annotation[0][11].set_color, B_COLOR,
			annotation[0][6].set_color, A_COLOR,
			annotation[0][14].set_color, A_COLOR
		)
		self.wait()
		self.play(
			ShrinkToCenter(vertex),
			ShrinkToCenter(symbol),
			Uncreate(horizontal_line),
			Uncreate(vertical_line),
			FadeOut(annotation),
			# FadeOut(feature),
		)
				



class Test(Scene):
	def construct(self):
		self.add(Heart())
		
		
		


