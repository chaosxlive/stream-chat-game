from typing import TYPE_CHECKING
import pygame as PYG
from Defined import Color, TextScope
from GameLib import Helper
from components.Menu import MainMenu

if TYPE_CHECKING:
    from typing import Tuple, List, Callable
    from components.ViewBase import ViewBase


class Engine:

    def __init__(self):
        PYG.init()

        # Core
        self.clock = PYG.time.Clock()
        self.helper = Helper()

        # Configurations

        # Screen size
        self.conf_WIN_WIDTH = 1200
        self.conf_WIN_HEIGHT = 800
        # Font
        self.conf_SYS_FONT_FAMILY = PYG.font.get_default_font()
        self.conf_SYS_FONT_SIZE_TITLE = 64
        self.conf_SYS_FONT_SIZE = 48
        self.conf_SYS_FONT_COLOR = Color.WHITE

        self.applyConfig()

        self.display = PYG.Surface((self.conf_WIN_WIDTH, self.conf_WIN_HEIGHT))
        self.window = PYG.display.set_mode((self.conf_WIN_WIDTH, self.conf_WIN_HEIGHT))

        # Runtime variable

        # System settings
        self.frameRate = 15
        # Program status
        self.state_RUNNING = True
        self.state_PLAYING = False
        # Keyboard pressed
        self.keyPressed_UP = False
        self.keyPressed_DOWN = False
        self.keyPressed_LEFT = False
        self.keyPressed_RIGHT = False
        self.keyPressed_ENTER = False
        self.keyPressed_BACK = False
        # Views
        self.need_VIES_STACK_SORT = False
        self.current_VIEW_STACK: 'List[Tuple[int,str,ViewBase]]' = []
        self.current_KEYBOARD_EVENT: 'List[Callable]' = []
        self.next_VIEW_STACK: 'List[Tuple[int,str,ViewBase]]' = []

        self.initView()

    def initView(self):
        self.current_VIEW_STACK.append((1, 'MainMenu', MainMenu(self)))

    def loop(self):
        '''Handle the game loop state.'''
        while self.state_PLAYING:
            self.clock.tick(self.frameRate)
            self.checkEvents()
            if self.keyPressed_ENTER:
                self.state_PLAYING = False
            # Set camera background
            self.drawDefaultBackground()

            self.next_VIEW_STACK = self.current_VIEW_STACK[:]
            for _, _, view in self.current_VIEW_STACK:
                view.handle()
            self.current_VIEW_STACK = self.next_VIEW_STACK
            if self.need_VIES_STACK_SORT:
                self.need_VIES_STACK_SORT = False
                self.current_VIEW_STACK.sort(key=lambda v: v[0])

            self.update()

    def update(self):
        '''Do rendering and reset key.'''
        self.window.blit(self.display, (0, 0))
        PYG.display.update()
        self.resetkeyPressed()

    def applyConfig(self):
        '''Loading and apply the config.'''
        pass

    def checkEvents(self):
        for event in PYG.event.get():
            if event.type == PYG.QUIT:
                self.state_RUNNING = False
                self.state_PLAYING = False
            elif event.type == PYG.KEYDOWN:
                if event.key == PYG.K_RETURN:
                    self.keyPressed_ENTER = True
                elif event.key == PYG.K_BACKSPACE:
                    self.keyPressed_BACK = True
                elif event.key == PYG.K_UP:
                    self.keyPressed_UP = True
                elif event.key == PYG.K_DOWN:
                    self.keyPressed_DOWN = True

    def resetkeyPressed(self):
        self.keyPressed_UP = False
        self.keyPressed_DOWN = False
        self.keyPressed_ENTER = False
        self.keyPressed_BACK = False

    def drawDefaultBackground(self):
        self.display.fill(Color.BLACK)

    def drawText(self, scope: int, x: int, y: int, text: str, color: 'Tuple[int, int, int]' = None, fontSize: int = None, fontFamily: str = None):
        '''Draw a text on screen.'''
        # Color
        if color is None:
            if scope == TextScope.SYS:
                color = self.conf_SYS_FONT_COLOR
            else:
                color = Color.WHITE
        # Font family
        if fontFamily is None:
            if scope == TextScope.SYS:
                fontFamily = self.conf_SYS_FONT_FAMILY
            else:
                fontFamily = PYG.font.get_default_font()
        # Font size
        if fontSize is None:
            if scope == TextScope.SYS:
                fontSize = self.conf_SYS_FONT_SIZE
            else:
                fontSize = 12
        font = PYG.font.Font(fontFamily, fontSize)
        textSurface = font.render(text, True, color)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        self.display.blit(textSurface, textRect)

    def addView(self, name: str, view: 'ViewBase', zIndex: int = 1):
        self.next_VIEW_STACK.append((zIndex, name, view))
        self.need_VIES_STACK_SORT = True

    def removeView(self, name: str):
        self.next_VIEW_STACK = list(filter(lambda item: item[1] != name, self.next_VIEW_STACK))

    def setFrameRate(self, frameRate: int = 1):
        self.frameRate = frameRate

    def exit(self):
        self.state_RUNNING = False