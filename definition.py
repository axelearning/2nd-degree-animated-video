#!/usr/bin/env python
from manimlib.creature.pencil_creature_scene import CreatureScene
import sys
sys.path.insert(1, "/Users/axel/Agensit/manim/manim_3b1b")

from manimlib.imports import *

# 0. Show Synonym
# 1. Write general term : f(x)= ax^2 + bx + c + examples
# 4. Show case when a=0
# 5. display the constraint, a!= 0


# GLOBAL VARIABLES
# -------------------------------------------------------------------
TITLE = "Les polynomes du second degré"
TITLE_SCALE = 0.5

# 0 Show Synonym
SYNONYM1 = "Les polynomes du second degré"
SYNONYM2 = "Les trinomes ?"
SYNONYM3 = "Les fonctions polynomiales \\\ du second degré ?"
SYNONIM_COLOR = GREY

# 1 Write general term : f(x)= ax^2 + bx + c + examples
SUBTITLE =  "1. Définition"
SUBTITLE_SCALE = 2
SUBTITLE_COLOR = BLUE
SUBTITLE_WRITING_TIME = 3
SUBTITLE_REDUCTION =0.5

EXPRESSION_WRITING_TIME = 3 
EXPRESSION_WAITING_TIME = 3 

COEF_POLYNOME_1 = [2,-3,2]
COEF_POLYNOME_2 = [-1,-2,1]
COEF_POLYNOME_3 = [1,2,1]
COEF_POLYNOME_4 = ["\sqrt2",-2,3]
COEF_POLYNOME_5 = [3,"\\frac{3}{5}",1]
WAITING_TIME = 1 # 3



# TEST
# -------------------------------------------------------------------
class Test(Scene):
	def construct(self):
		trinome = Trinome(2,3,4).scale(2)
		self.add(trinome)
# ANIMATION
# -------------------------------------------------------------------

class Synonym(TeacherStudentsScene):
	CONFIG = {
		"creatures_start_on_screen": False
	}
	# MAIN
	# ----------------
	def construct(self):
		# setup the scene
		self.teacher.change("confident")
		for student,mode in zip(self.students, ["think", "confident", "think"]):			
			student.change(mode) 
		self.creatures.shift(0.5*UP)
		title = TextMobject(TITLE).scale(TITLE_SCALE).to_corner(buff=SMALL_BUFF)
		self.add(title)

		# introduce the teacher
		self.add(self.teacher)
		self.wait(2)
		self.teacher_says(SYNONYM1, target_mode="confident")
		self.non_blink_wait(3)

		# # GIVE THE SYNONYM
		self.appears(self.students, direction=DOWN)
		self.wait(2)
		self.student_says(SYNONYM2, target_mode="think")
		self.wait(5)
		self.student_says(SYNONYM3, target_mode="think", student_index=0)
		self.wait(5)
		self.teacher_says(SYNONYM1, target_mode="happy")
		self.play(*[ApplyMethod(student.change,"happy") for student in self.students])
		self.wait(2)

class Definition(AlexScene):
	CONFIG = {
		"creatures_start_on_screen": False,
		"default_creature_kwargs": {
			"color": SANDY_BROWN,
			"mode": "think"
		}
	}
	# MAIN
	# ----------------
	def construct(self):
		self.write_subtitle()
		general_expression = self.general_expression()
		trinome, info = general_expression
		# self.display_examples(trinome)

	# SUBSCENES
	# ----------------
	
	def write_subtitle(self):
		# Show the subtitle then scale it down to the bottom left next to the title

		# 1. add the title in the bottom left corner to create coherence with previous animation
		title = TextMobject(TITLE)
		title.scale(TITLE_SCALE)
		title.to_corner(buff=SMALL_BUFF)
		self.add(title)

		# 2. write the subtitle
		subtitle = TextMobject(SUBTITLE, color=SUBTITLE_COLOR)
		subtitle.scale(SUBTITLE_SCALE)
		self.play(Write(subtitle), run_time=SUBTITLE_WRITING_TIME)
		self.wait(2)

		# 3. send and scale it down close to the title
		subtitle_as_info = TextMobject(f"/ {SUBTITLE}", color=SUBTITLE_COLOR)
		subtitle_as_info.scale(SUBTITLE_REDUCTION)
		subtitle_as_info.next_to(title, buff=SMALL_BUFF)
		self.play(Transform(subtitle, subtitle_as_info), run_time = 2)

	def general_expression(self):
		trinome = Trinome().scale(2)
		general_expression = trinome.get_info()
		student = self.creature

		self.play(Write(general_expression), run_time=EXPRESSION_WRITING_TIME)
		self.appears(direction=RIGHT)
		self.look_at(trinome)
		self.wait(EXPRESSION_WAITING_TIME)
		return general_expression


	def display_examples(self, trinome):	
		# basic exemple	
		self.create_example(COEF_POLYNOME_1, trinome)
		self.change_mode("normal")
		self.wait()
		# self.create_example(COEF_POLYNOME_2, trinome)
		# self.change_mode("confident")
		# self.wait()
		# self.create_example(COEF_POLYNOME_3, trinome)
		# self.disappears(run_time=1)
		# self.create_example(COEF_POLYNOME_4, trinome)
		# self.wait()
		# self.create_example(COEF_POLYNOME_5, trinome)



		# # example 2 → example 3
		# a,b,c = COEF_POLYNOME_3
		# example3_detailed = Trinome(a,b,c, label=LABEL_POLYNOME_3, detailed_exp=True).scale(2)
		# example3_detailed.move_to(self.trinome).align_to(self.trinome, LEFT)
		# self.play(Transform(self.trinome, example3_detailed)) 
		# self.wait()		
		# self.detailed_to_simple(self.trinome, Trinome(a,b,c, label=LABEL_POLYNOME_3))
		# self.wait(WAITING_TIME)
		# self.play(
		# 	*[FadeOut(mob) for mob in self.mobjects if mob.name != "TextMobject"],
		# 	FadeOut(self.info)
		# )
	
	def a_is_null(self):
		self.teacher = Alex().to_corner(DR, buff=0.1)
		self.general_expression()
		self.play(FadeInFrom(self.teacher, RIGHT))
		self.play(Thinks(self.teacher, BOB_SENTENCE_2))
		self.wait()
		self.play(Blink(self.teacher))
		self.wait()
		self.play(
			FadeOut(self.teacher.bubble),
			FadeOut(self.teacher.bubble.content)
		)
		# try for a = 0
		text_a_zero = TextMobject(*["si ","a = 0"])
		text_a_zero.move_to(self.info).align_to(self.info)
		text_a_zero[1].set_color(BLUE)
		text_a_zero.align_to(self.trinome, LEFT)
		# self.play(ApplyWave(self.info))
		self.play(Uncreate(self.info))
		self.play(
			Write(text_a_zero),
			Blink(self.teacher))

		first_degree_detailed = Trinome("0","b","c").expression.scale(2)
		first_degree_detailed.move_to(self.trinome).align_to(self.trinome, LEFT)
		self.play(
			Transform(self.trinome, first_degree_detailed),
			Blink(self.teacher)
			)

		first_degree_simplify = TexMobject(*["f(x)=","b","x","+c"]).scale(2)
		first_degree_simplify.move_to(self.trinome).align_to(self.trinome, LEFT)
		first_degree_simplify[1].set_color(RED)
		first_degree_simplify[3].set_color(GREEN)
		self.play(
			Transform(self.trinome, first_degree_simplify),
			Blink(self.teacher)
		)
		self.wait()

		# correct the expression
		self.play(*[FadeOut(mob) for mob in self.mobjects])

		self.general_expression()
		self.play(*[ApplyMethod(mob.set_opacity,0.8) for mob in self.mobjects])
		self.play(
			self.trinome.set_opacity, 0.8,
			self.info.set_opacity, 0.8	
		)
		text = TextMobject(*["et ", r"$a\neq0$"]).scale(1.2).next_to(self.info)
		text.set_color(BLUE)
		self.play(Write(text))



	# SUBPROCESS
	# ----------------
	def create_example(self, coefs, trinome, run_time=1):
		example =Trinome(*coefs).scale(2)
		example.move_to(trinome).align_to(trinome, LEFT)
		self.play(Transform(trinome, example), run_time=run_time)

	def detailed_to_simple(self, detailed_form, simple_form):
		if not simple_form.a:
			self.play(
				ApplyMethod(detailed_form[4:].move_to, detailed_form[2].get_right()+ 1.2 *RIGHT),
				FadeOutAndShiftDown(detailed_form[2:4]),
			)
		if not simple_form.b:
			self.play(
				ApplyMethod(detailed_form[6].move_to, detailed_form[4].get_center()),
				FadeOutAndShiftDown(detailed_form[4:6]),
			)
		if not simple_form.c:
			self.play(FadeOutAndShiftDown(detailed_form[6]))

class a_is_null(GraphScene):
	CONFIG={
		"camera_config": {
			"background_color": DARKER_GREY
			}
		}
	# MAIN
	# ----------------
	def construct(self):
		trinome = Trinome().expression.scale(2)
		info = TextMobject(*INFO)
		info[1].set_color(BLUE)
		info[3].set_color(RED)
		info[5].set_color(GREEN)

		general_expression = VGroup(trinome, info)
		general_expression.arrange(2.5*DOWN)
		info.align_to(trinome, LEFT)
		general_expression.save_state()

		frame_bg = BackgroundRectangle(general_expression, buff=1, fill_opacity=1)
		frame = Group(frame_bg, general_expression)
		frame_bg.set_stroke(color=BLUE, width=2, opacity=1)
		frame.save_state()
		title = TextMobject("Polynome ", "du ", "second ", "degré").next_to(frame, UP, buff=0.5).align_to(frame, LEFT)
		title[2].set_color(YELLOW)
		frame.scale(0.6).to_corner(UL)

		self.add(frame)

		# Create and Fade pi creatures 
		teacher = Alex().to_corner(DR)
		student1 = Alex(flip_at_start = False).set_color(BLUE_D).scale(0.8)
		student2 = Alex(flip_at_start = False).set_color(BLUE_E).scale(0.8)
		student3 = Alex(flip_at_start = False).set_color(BLUE_D).scale(0.8)
		students = VGroup(student1, student2, student3)
		students.arrange(RIGHT).to_corner(DL)
		self.play(
			FadeInFrom(teacher, RIGHT),
			FadeIn(students),
		)
		for student in students:
			student.make_eye_contact(teacher)
		teacher.make_eye_contact(students[-1])
		self.ask(teacher, "si a = 0")
		self.play(Blink(student2))
		self.play(
			AnimationGroup(
				Restore(frame),
				FadeOut(students, run_time=0.5),
				FadeOut(teacher, run_time=0.5),
			)
		)
		self.add(title)
		self.wait(2)

		# a = 0
		trinome.save_state()
		first_degree_detailed = Trinome("0","b","c").expression.scale(2)
		first_degree_detailed.move_to(trinome).align_to(trinome, LEFT)
		self.play(Transform(trinome, first_degree_detailed))

		first_degree_simplify = TexMobject(*["f(x)=","b","x","+c"]).scale(2)
		first_degree_simplify.move_to(trinome).align_to(trinome, LEFT)
		first_degree_simplify[1].set_color(RED)
		first_degree_simplify[3].set_color(GREEN)
		new_title = TextMobject("Polynome ", "du ", "premier ", "degré").next_to(frame, UP, buff=0.5).align_to(frame, LEFT)
		new_title[2].set_color(YELLOW)

		self.wait(2)
		self.play(
			Transform(trinome, first_degree_simplify),
			Transform(title, new_title)
		)
		self.wait(2)
		self.play(
			Uncreate(general_expression),
			Uncreate(title)
		)

		# give correct definition
		general_expression.restore()
		constraint = TextMobject(*[" et ", r"$a\neq0$"]).scale(1.2).next_to(info)
		constraint[0].set_color(YELLOW)
		constraint[-1].set_color(BLUE)
		self.play(
			Write(general_expression),
		)
		self.wait(2)
		self.play(Write(constraint))

	# SUBPROCESS
	# ----------------
	def ask(self, creature, question):
		self.play(Says(creature, question))
		self.play(Blink(creature))
		self.wait()
		self.play(
			FadeOut(creature.bubble),
			FadeOut(creature.bubble.content)
		)




 





	
