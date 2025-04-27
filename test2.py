from manim import *
import numpy as np
from manim.utils.color import interpolate_color

class OrbitingParticles(Scene):
    def construct(self):
        # Setup black hole with vertical movement
        black_hole = Dot(radius=0.3, color=BLACK, fill_opacity=1)
        # Create a white circle around the black hole
        white_ring = Circle(radius=0.5, color=WHITE, stroke_width=2).move_to(black_hole)
        black_hole_group = VGroup(black_hole, white_ring)
        black_hole_group.move_to(DOWN * 3)
        
        # Create particles and orbits
        particles = VGroup()
        orbits = VGroup()
        
        num_particles = 20
        for _ in range(num_particles):
            # Randomize particle parameters
            r = np.random.uniform(1.5, 4)
            omega = 0.7 / (r ** 1.5)  # Angular velocity (Kepler's third law)
            theta0 = np.random.uniform(0, 2*PI)
            size = 0.1 / r
            color = interpolate_color(RED, YELLOW, np.random.uniform(0.2, 0.8))
            
            # Create particle with updater
            particle = Dot(radius=size, color=color)
            particle.time = 0  # Track individual particle time
            
            # Define particle updater function
            def update_particle(mob, dt, r=r, omega=omega, theta0=theta0):
                mob.time += dt
                angle = (theta0 + omega * mob.time )*10
                bh_center = black_hole_group.get_center()
                x = bh_center[0] + r * np.cos(angle)
                y = bh_center[1] + r * np.sin(angle)
                mob.move_to([x, y, 0])
            
            particle.add_updater(update_particle)
            particles.add(particle)
            
            # Create orbit
            orbit = Circle(
                radius=r,
                color=WHITE,
                stroke_width=1,
                stroke_opacity=0.3
            )
            orbit.add_updater(lambda m: m.move_to(black_hole_group.get_center()))
            orbits.add(orbit)
        
        # Add all elements to scene
        self.add(orbits, black_hole_group, particles)
        
        # Animate black hole moving upward
        self.play(
            black_hole_group.animate.shift(UP * 3),
            rate_func=linear,
            run_time=6
        )
        self.wait(2)