from manim import Scene, FadeIn, VGroup, Line, config, DOWN, UP, LEFT, RIGHT, Create, Rectangle, WHITE, AnimationGroup , Text , DEGREES
from manim.utils.space_ops import line_intersection
from numpy import array
from typing import Union , Callable

rightUp = array([config.frame_x_radius, config.frame_y_radius, 0])
leftBottom = -rightUp

class main(Scene):
    def makeHorizontalLines(self,
                            spacing: Union[int, float],
                            startingX: Union[int, float] = -config.frame_x_radius,
                            endingX: Union[int, float] = config.frame_x_radius,
                            startingY: Union[int, float] = -config.frame_y_radius,
                            endingY: Union[int, float] = config.frame_y_radius,
                            ) -> VGroup:
        HRlines = VGroup()
        if startingY > endingY:
            startingY, endingY = endingY, startingY
        currentY = startingY
        while currentY <= endingY:
            line = Line(array([startingX, currentY, 0]), array([endingX, currentY, 0]))
            HRlines.add(line)
            currentY += spacing
        return HRlines

    def construct(self):
        spacingBW_HR_Lines = 0.6 # distance bw wires
        boxSize = spacingBW_HR_Lines + 0.1 # width of memory cell
        HRlines = self.makeHorizontalLines(spacingBW_HR_Lines, startingY=-1, endingY=2.5)
        slopeLine45 = Line(leftBottom , rightUp).rotate(10 * DEGREES , about_point= leftBottom)

        animations = []

        newHRlines = VGroup()
        for line in HRlines:
            intersection_point = line_intersection([line.get_start(), line.get_end()], [slopeLine45.get_end(), slopeLine45.get_start()])
            l = Line(start=line.get_start(), end=intersection_point)
            newHRlines.add(l)
        HRlines = newHRlines
        self.play(Create(HRlines))
        self.wait(0.5)

        VRlines = VGroup()
        rectangles = VGroup()
        base_y = HRlines.get_bottom()[1] + DOWN[1] * 0.5  # Define a base y-level

        for line in HRlines:
            end_point_hline = line.get_end()
            start_point_vline = end_point_hline
            end_point_vline = array([end_point_hline[0], base_y, 0])
            v_line = Line(start=start_point_vline, end=end_point_vline)
            VRlines.add(v_line)

            rect = Rectangle(color=WHITE, width=boxSize, height=boxSize * 0.4) # Adjust height as needed

            def update_rectangle(rect, v_line=v_line):
                top_end_vline = v_line.get_end()
                rect_top_center = rect.get_top() + DOWN * rect.height / 2 # Calculate the top-center
                rect.move_to(top_end_vline + DOWN * rect.height / 2) # Move the top-center to the end of the v_line

            rect.add_updater(update_rectangle)
            rectangles.add(rect)

        self.play(
            Create(VRlines),
            Create(rectangles),
            run_time=2
        )
        self.wait()

        # To see the static final state, you can remove the updaters
        for rect in rectangles:
            rect.clear_updaters()
        self.wait(1)
        memory = VGroup()
        for i in range(len(HRlines)):
            mem = VGroup()
            wire = VGroup()
            wire.add(HRlines[i], VRlines[i])  # type: ignore
            mem.add(wire, rectangles[i])  # type: ignore
            memory.add(mem)
        self.remove(HRlines, VRlines, rectangles)
        self.add(memory)
        self.wait()

        binarySequence = [0] * len(memory)  # Initialize with zeros
        memoryData = VGroup()

        def updaterReturner(memoryCellNumber: int) -> Callable[[Text], None]:
            def updater(data: Text) -> None:
                data.set_text(str(binarySequence[memoryCellNumber]))
                data.move_to(memory[memoryCellNumber][1].get_center())
            return updater
        for i in range(len(memory)):
            data = Text(str(binarySequence[i]), fill_opacity=1, font_size=20, color=WHITE)  # Increased font_size
            updater = updaterReturner(i)
            data.add_updater(updater) # type: ignore
            memoryData.add(data)  # Add the Text object to memoryData

        self.play(FadeIn(memoryData))
        self.wait(2) # Give some time to see the data