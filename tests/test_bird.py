import sys
import types
import unittest


canvas = {'width': 1600, 'height': 600}


class FakeImage:
    def __init__(self):
        self.draw_calls = []

    def clip_draw(self, *args):
        self.draw_calls.append(('draw', args))

    def clip_composite_draw(self, *args):
        self.draw_calls.append(('composite_draw', args))


fake_image = FakeImage()
pico2d = types.ModuleType('pico2d')
pico2d.get_canvas_width = lambda: canvas['width']
pico2d.get_canvas_height = lambda: canvas['height']
pico2d.load_image = lambda _path: fake_image
sys.modules['pico2d'] = pico2d

import bird
import game_framework


class BirdTests(unittest.TestCase):
    def setUp(self):
        bird.Bird.image = None
        fake_image.draw_calls.clear()
        canvas.update(width=1600, height=600)
        game_framework.frame_time = 0.0

    def test_speed_and_frame_geometry_match_requirements(self):
        self.assertAlmostEqual(bird.BIRD_SPEED_PPS, 92.59259259)
        self.assertEqual(len(bird.FRAME_RECTS), 14)
        for x, y, width, height in bird.FRAME_RECTS:
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertGreater(width, 0)
            self.assertGreater(height, 0)
            self.assertLessEqual(x + width, bird.SPRITE_WIDTH)
            self.assertLessEqual(y + height, bird.SPRITE_HEIGHT)

    def test_frame_rate_uses_measured_wingtip_distance(self):
        expected = (
            bird.BIRD_SPEED_PPS * bird.WINGTIP_SPEED_RATIO
            / (bird.WINGTIP_TRAVEL_SOURCE_PX * bird.BIRD_SCALE
               / bird.WINGTIP_TRANSITION_FRAMES)
        )
        self.assertAlmostEqual(bird.BIRD_FRAME_RATE, expected)

    def test_direction_is_validated_and_initial_position_is_clamped(self):
        with self.assertRaises(ValueError):
            bird.Bird(100, 100, 0)

        instance = bird.Bird(-10, 900)
        self.assertAlmostEqual(instance.x, bird.BIRD_DRAW_WIDTH / 2)
        self.assertAlmostEqual(
            instance.y, canvas['height'] - bird.BIRD_DRAW_HEIGHT / 2
        )

    def test_flight_speed_and_animation_use_elapsed_time(self):
        instance = bird.Bird(800, 300)
        game_framework.frame_time = 0.5
        instance.update()
        self.assertAlmostEqual(
            instance.x, 800 + bird.BIRD_SPEED_PPS * 0.5
        )
        self.assertAlmostEqual(
            instance.frame, bird.BIRD_FRAME_RATE * 0.5 % 14
        )

    def test_large_delta_reflects_at_canvas_edges(self):
        instance = bird.Bird(1500, 300)
        game_framework.frame_time = 2.0
        instance.update()
        half_width = bird.BIRD_DRAW_WIDTH / 2
        self.assertGreaterEqual(instance.x, half_width)
        self.assertLessEqual(instance.x, canvas['width'] - half_width)
        self.assertEqual(instance.direction, -1)

    def test_drawing_selects_current_frame_and_flips_leftward_birds(self):
        instance = bird.Bird(300, 300, -1)
        instance.frame = 5
        instance.draw()

        draw_type, args = fake_image.draw_calls[-1]
        self.assertEqual(draw_type, 'composite_draw')
        self.assertEqual(args[0:4], bird.FRAME_RECTS[5])
        self.assertEqual(args[5], 'h')

    def test_play_mode_registers_and_cleans_up_ten_birds(self):
        boy_module = types.ModuleType('boy')
        grass_module = types.ModuleType('grass')
        boy_module.Boy = type('StubBoy', (), {})
        grass_module.Grass = type('StubGrass', (), {})
        sys.modules['boy'] = boy_module
        sys.modules['grass'] = grass_module

        import game_world
        import play_mode

        game_world.clear()
        play_mode.init()
        self.assertEqual(len(play_mode.birds), 10)
        self.assertEqual(
            sum(isinstance(item, bird.Bird) for item in game_world.world[1]),
            10
        )
        self.assertEqual(len({item.direction for item in play_mode.birds}), 2)

        play_mode.finish()
        self.assertEqual(play_mode.birds, [])
        self.assertTrue(all(not layer for layer in game_world.world))


if __name__ == '__main__':
    unittest.main()
