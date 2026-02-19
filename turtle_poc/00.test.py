from manim import *

class TypeCode(Scene):
    def construct(self):
        code = Code(
            code="print('Hello World')\nfor i in range(5):\n    print(i)",
            language="python",
            font="Monospace"
        )
        self.play(Write(code), run_time=3) # Adjust run_time for speed
        self.wait(2)