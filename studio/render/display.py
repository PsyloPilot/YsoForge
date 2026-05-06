import pygame
from pygame.locals import DOUBLEBUF


class Display:
    """
    Verantwortlich für:
    - Fenster erstellen
    - Events liefern
    - Backbuffer bereitstellen
    - Swap/Flip
    """

    def __init__(self, width, height, title):
        pygame.init()
        pygame.display.set_caption(title)

        # Klassisches 2D-Rendering (kein OpenGL nötig)
        self.surface = pygame.display.set_mode(
            (width, height),
            DOUBLEBUF
        )

        self.width = width
        self.height = height
        self.running = True

    # ------------------------------------------------------------
    # EVENT LOOP
    # ------------------------------------------------------------
    def poll_events(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
        return events

    # ------------------------------------------------------------
    # SWAP BUFFERS
    # ------------------------------------------------------------
    def swap(self):
        pygame.display.flip()

    # ------------------------------------------------------------
    # ACCESSORS
    # ------------------------------------------------------------
    def get_surface(self):
        return self.surface

    # ------------------------------------------------------------
    # SHUTDOWN
    # ------------------------------------------------------------
    def close(self):
        pygame.quit()
