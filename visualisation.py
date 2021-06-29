#!/usr/bin/env python
import sys
sys.path.insert(1, "/Users/axel/Agensit/manim/manim_3b1b")

from manimlib.imports import *

# 1.
# 2. 
# 3. 

# GLOBAL VARIABLES
# -------------------------------------------------------------------

# Visulaisation
PARABOLA_COLOR = YELLOW
PARABOLA_WRITING_TIME =1

# Exemple
COEF_POLYNOME_1 = [2,-3,2]
LABEL_POLYNOME_1 = "f(x)"
COLOR_POLYNOME_1 = PERSIAN_GREEN

COEF_POLYNOME_2 = [-1,-2,1]
LABEL_POLYNOME_2 = "g(x)"
COLOR_POLYNOME_2 = ORANGE_YELLOW

COEF_POLYNOME_3 = [0.1,0,-1]
LABEL_POLYNOME_3 = "h(x)"
COLOR_POLYNOME_3 = BURNT_SIENNA

WAITING_TIME = 1 # 3



# CUSTOM CLASS 
# -------------------------------------------------------------------
class Slider:
	def __init__(self, color, label):
		self.line = Line().set_color(color)
		self.dot = Dot().scale(2)
		self.label = TexMobject(label).set_color(color).scale(2)
		self.label.next_to(self.line, LEFT)

		self.decimal = ValueTracker()
		self.group = Group(self.line, self.dot, self.decimal, self.label)

	def update(self, multiplicative_factor=3):
		self.decimal = self.decimal.add_updater(lambda d: d.set_value(multiplicative_factor*(self.dot.get_center()[0] - self.line.get_center()[0])+1))
		
# -------------------------------------------------------------------
class Trinome():
	def __init__(self, a="a",b="b",c="c", label="f(x)", color_coef=True, detailed_exp=False):
		# create expression
		self.expression = self.construct(label, a, b, c)


		if  detailed_exp:
			self.label = self.expression[0]
			self.a = self.expression[2]
			self.b = self.expression[4]
			self.c = self.expression[-1]
		else:
			self.simple_form(a, b, c)
			self.assign_coef(a,b,c)

		if color_coef:
			self.colorized()

	def construct(self, label, a, b, c):
		# create the trinome as a TexMobject
		expression = [label, "="]
		if (type(a)==int or type(a)==float) and (type(b)== int or type(b)==float) and (type(c)==int or type(c)==float):
			# 1. add a coef
			if a == 1 :
				expression.extend(["+","x^2"])
			elif a == -1 :
				expression.extend(["-","x^2"])
			else :
				expression.extend([str(a),"x^2"])
			# 2. add b coef
			if b == 1 :
				expression.extend(["+","x"])
			elif b == -1 :
				expression.extend(["-","x"])		
			elif b >= 0:
				expression.extend([f"+{b}","x"])
			else:
				expression.extend([str(b),"x"])	
			# 3. add c coef
			if c >= 0:
				expression.append(f"+{c}")
			else:
				expression.append(str(c))

		else:
			expression = [label, "=", f"{a}","x^2",f"+{b}","x",f"+{c}"]

		return TexMobject(*expression)

	def simple_form(self, a, b, c):
		if a == 0:
			try:
				self.expression.tex_strings.remove("+0")
				self.expression.tex_strings.remove("x^2")
			except:
				print("not a")

		if b == 0:
			try:
				self.expression.tex_strings.remove("+0")
				self.expression.tex_strings.remove("x")
			except:
				print("not b")

		if c == 0:
			try:
				self.expression.tex_strings.remove("+0")
			except:
				print("not c")

		self.expression = TexMobject(*self.expression.tex_strings)

	def assign_coef(self, a,b,c):
		self.label = self.expression[0]
		if a !=0 :
			self.a = self.expression[2]
		else:
			self.a = None
		if b != 0:
			index = self.expression.tex_strings.index("x")
			self.b = self.expression[index-1]
		else:
			self.b = None
		if c !=0 :
			self.c = self.expression[-1]
		else:
			self.c = None

	def colorized(self):
		try:
			self.a.set_color(BLUE)
		except:
			pass
		try:
			self.b.set_color(RED)
		except:
			pass
		try:
			self.c.set_color(GREEN)
		except:
			pass

	def shuffle(self):
		pass
		

# ANIMATION
# -------------------------------------------------------------------
class Visualisation(GraphScene):
	CONFIG = {
		"x_min" : -6,
		"x_max" : 6,
		"y_max" : 10,
		"y_min" : -10,
		"y_tick_frequency": 10,
		"x_tick_frequency": 6,
		"y_axis_height": 11,
		"x_axis_width": 7,
		"x_axis_label" : "$x$",
		"y_axis_label" : "",
		"graph_origin": 1*DOWN + 2.3*RIGHT
	}
	# MAIN
	# ----------------
	def construct(self):
		# general case
		trinome = Trinome().expression.scale(1.5)
		trinome.to_corner(UL)

		# initialise and show the curve
		self.play(FadeInFrom(trinome, LEFT))
		self.setup_axes(animate=True)
		curve = self.get_graph(lambda x: x**2 + x + 1, color=PARABOLA_COLOR)
		self.label = self.get_graph_label(curve, label="f(x)", x_val=1)
		parabola = Group(curve, self.label)
		self.play(ShowCreation(parabola), run_time=PARABOLA_WRITING_TIME)
		
		# create sliders
		slider_a = Slider(BLUE, "a")
		slider_b = Slider(RED, "b")
		slider_c = Slider(GREEN, "c")

		parameters = Group(slider_a.group, slider_b.group, slider_c.group)
		parameters.arrange(DOWN, buff=0.5)
		slider_b.group.align_to(slider_a.group, LEFT)
		slider_c.group.align_to(slider_a.group, LEFT)
		parameters.next_to(trinome, DOWN, buff=0.8)
		parameters.align_to(trinome, LEFT)

		a = slider_a.decimal
		b = slider_b.decimal
		c = slider_c.decimal		

		slider_a.update(multiplicative_factor=10)
		slider_b.update(multiplicative_factor=10)
		slider_c.update(multiplicative_factor=10)

		self.play(
			AnimationGroup(
				self.anim_coef_to_slider(trinome, slider_a,"a"),
				self.anim_coef_to_slider(trinome, slider_b, "b"),
				self.anim_coef_to_slider(trinome, slider_c, "c"),
				lag_ratio = 0.1
			)
		)
		self.wait()

		# update the parabola with a,b,c
		def update_curve(curve):
			curve = self.get_graph(
						lambda x:a.get_value()*x**2 + b.get_value()*x + c.get_value(), 
						color=PARABOLA_COLOR
					)
			label = self.label.move_to(self.label.get_center())
			parabola.become(Group(curve,self.label))


		parabola.add_updater(update_curve)
		self.add(*[a, b, c])
		self.play(
			Succession(
				Indicate(slider_a.dot, scale_factor=1.5, run_time=0.2),
				ApplyMethod(slider_a.dot.shift, RIGHT, rate_func=there_and_back, run_time=5),
			),
		)
		self.wait(2)
		self.play(
			Succession(
				AnimationGroup(
					Indicate(slider_a.dot, scale_factor=1.5),
					Indicate(slider_b.dot, scale_factor=1.5),
					Indicate(slider_c.dot, scale_factor=1.5),

				),
				AnimationGroup(
					ApplyMethod(slider_a.dot.shift, LEFT, rate_func=there_and_back), 
					ApplyMethod(slider_b.dot.shift, 0.6*RIGHT, rate_func=there_and_back),
					ApplyMethod(slider_c.dot.shift, 0.3*RIGHT, rate_func=there_and_back),
				), 
				run_time=10
			)
		)
		self.wait(2)


	# SUBPROCESSE
	# ----------------
	def anim_coef_to_slider(self, trinome, slider, coef):
		if coef == "a":
			i =2
		elif coef == "b":
			i = 4
		else:
			i=6
		return AnimationGroup(
				TransformFromCopy(trinome[i],Group(slider.line,slider.label)),
				FadeIn(slider.dot),
				lag_ratio = 1
			)

class Exemples(GraphScene):
	CONFIG={
		"x_min" : -9,
		"x_max" : 9,
		"y_max" : 10,
		"y_min" : -10,
		"y_tick_frequency": 10,
		"x_tick_frequency": 9,
		"y_axis_height": 7,
		"x_axis_width": 7,
		"x_labeled_nums": list(range(-9,10,3)),
		"x_axis_label" : "$x$",
		"y_axis_label" : "",
		"graph_origin": 2.3*RIGHT
	}
	def construct(self):
		self.setup_axes(animate=True)
		example_1, parabola_1 = self.create_trinome(coefs=COEF_POLYNOME_1, label=LABEL_POLYNOME_1, color=COLOR_POLYNOME_1)
		example_2, parabola_2 = self.create_trinome(coefs=COEF_POLYNOME_2, label=LABEL_POLYNOME_2, color=COLOR_POLYNOME_2, x_val=2)
		example_3, parabola_3 = self.create_trinome(coefs=COEF_POLYNOME_3, label=LABEL_POLYNOME_3, color=COLOR_POLYNOME_3, x_val=6)
		trinomes = Group(example_1, example_2, example_3).arrange(DOWN).to_corner(UL)
		example_2.align_to(example_1, LEFT)
		example_3.align_to(example_1, LEFT)

		self.play(Write(example_1))
		self.play(ShowCreation(parabola_1), run_time=3)

		self.play(
			AnimationGroup(
				Write(example_2),
				ApplyMethod(example_1.set_opacity, 0.5),
				ApplyMethod(parabola_1[0].set_stroke, {"opacity":0.5}),
				ApplyMethod(parabola_1[1].set_opacity, {"opacity":0.5}),
				lag_ratio = 0.2

			)
		)
		self.play(ShowCreation(parabola_2), run_time=3)

		self.play(
			AnimationGroup(
				Write(example_3),
				ApplyMethod(example_2.set_opacity, 0.5),
				ApplyMethod(parabola_2[0].set_stroke, {"opacity":0.5}),
				ApplyMethod(parabola_2[1].set_opacity, {"opacity":0.5}),
				lag_ratio = 0.2

			)
		)
		self.play(ShowCreation(parabola_3), run_time=3)

		self.play(
			AnimationGroup(
				ApplyMethod(example_1.set_opacity, 1),
				ApplyMethod(parabola_1[0].set_stroke, {"opacity":1}),
				ApplyMethod(parabola_1[1].set_opacity, {"opacity":1}),
				ApplyMethod(example_2.set_opacity, 1),
				ApplyMethod(parabola_2[0].set_stroke, {"opacity":1}),
				ApplyMethod(parabola_2[1].set_opacity, {"opacity":1})
			)
		)
	
	def create_trinome(self, coefs, label, color, x_val=None):
		a,b,c = coefs
		example = Trinome(a,b,c, label=label).expression.set_color(color)
		if a>0:
			x_min, x_max = np.roots([a,b, (c- self.y_max)])
		else:
			x_min, x_max = np.roots([a,b, (c- self.y_min)])

		curve = self.get_graph(
			lambda x: a*x**2 + b*x + c, 
			color=color,
			x_min = x_min,
			x_max = x_max
		)
		label = self.get_graph_label(curve, label=label, x_val=x_val)
		parabola = Group(curve, label)

		return example, parabola


