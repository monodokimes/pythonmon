import pygame
import Configuration
import Constants

from Component import GraphicsComponent
from Helpers import Helpers


class Gui:
    """
    manages the display of graphics onscreen
    """

    _layer_limit = Configuration.layer_limit
    _screen_width = Configuration.screen_width
    _screen_height = Configuration.screen_height
    _draw_tiles = Configuration.draw_tiles
    _screen_centre = _screen_width / 2, _screen_height / 2
    _ticks = 0
    frames_per_second = Configuration.fps

    _screen = pygame.display.set_mode((_screen_width, _screen_height))

    focus = None

    @staticmethod
    def set_focus(entity_name):
        """
        centres view
        :param entity_name: entity to keep at centre of screen
        :return:
        """

        for graphics_component in GraphicsComponent.List:
            if graphics_component.entity.name == entity_name:
                graphics_component.is_focus = True

    @staticmethod
    def draw():
        """
        draw all enabled GraphicsComponents layer by layer
        :return:
        """

        focus = None
        for graphics_component in GraphicsComponent.List:
            if graphics_component.is_focus:
                focus = graphics_component

        draw_pos = focus.draw_x, focus.draw_y
        focus_vector = Helpers.subtract_vector(Gui._screen_centre, draw_pos)

        # clear the screen
        Gui._screen.fill(Constants.BLACK)

        for layer in range(0, Gui._layer_limit):

            for graphics_component in GraphicsComponent.List:
                if graphics_component.layer == layer and graphics_component.enabled:

                    draw_rect = graphics_component.draw_x, graphics_component.draw_y
                    draw_with_offset = Helpers.add_vectors(draw_rect, focus_vector)

                    Gui._screen.blit(
                        graphics_component.surface, draw_with_offset)

        Gui._ticks += 1
        # update the display
        pygame.display.flip()
