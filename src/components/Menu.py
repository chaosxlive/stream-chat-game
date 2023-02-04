from typing import TYPE_CHECKING, List
from abc import abstractmethod
import pygame as PYG
from Defined import TextScope, Color
from .ViewBase import ViewBase
from .MenuOption import MenuOption, MenuOptionSelect, MenuOptionEntry

if TYPE_CHECKING:
    from GameEngine import Engine


class Menu(ViewBase):

    def __init__(self, engine: 'Engine'):
        self.engine = engine
        self.isShowTitle = True
        self.isShowCursor = True
        self.isOptionValid = False
        self.isOptionCyclic = True
        self.posX = self.engine.conf_WIN_WIDTH // 2
        self.posY = self.engine.conf_WIN_HEIGHT // 2
        self.textScope = TextScope.NONE
        self.titleText = ''
        self.titleFontSize = 10
        self.titleBiasX = 0
        self.titleBiasY = -20
        self.cursorText = ''
        self.cursorRect: 'PYG.Rect' = None
        self.cursorBiasX = -100
        self.cursorBiasY = 0
        self.cursorIndex = 0
        self.options: List[MenuOption] = []
        self.optionHeightUnits: List[int] = []
        self.optionFontSize = 10
        self.optionGap = 20
        self.optionBiasX = 0
        self.optionBiasY = 30
        self.optionMinIndex = 0
        self.optionMaxIndex = 0

    def initAll(self):
        '''Initialized all components in menu.'''
        self.initTitle()
        self.initCursor()
        self.initOptions()
        self.updateOptions()

    def initTitle(self):
        '''Initialized the title.'''
        return NotImplemented

    @abstractmethod
    def initCursor(self):
        '''Initialized the cursor object.'''
        return NotImplemented

    @abstractmethod
    def initOptions(self):
        '''Initialized the options in this menu.'''
        return NotImplemented

    def draw(self):
        '''Draw all components in menu.'''
        if not self.isOptionValid:
            return
        self.engine.drawDefaultBackground()
        self.drawTitle()
        self.drawOptions()
        self.drawCursor()

    def drawTitle(self):
        '''Draw title.'''
        if not self.isShowTitle:
            return
        self.engine.drawText(self.textScope, self.posX + self.titleBiasX, self.posY + self.titleBiasY, self.titleText, fontSize=self.titleFontSize)

    def drawCursor(self):
        '''Draw cursor.'''
        if not self.isShowCursor:
            return
        x = self.posX + self.cursorBiasX
        y = self.posY + self.cursorBiasY + self.optionBiasY + self.optionGap * self.optionHeightUnits[self.cursorIndex]
        self.cursorRect.midtop = (x, y)
        self.engine.drawText(self.textScope, self.cursorRect.x, self.cursorRect.y, self.cursorText)

    def drawOptions(self):
        '''Draw options.'''
        currentX = self.posX
        currentY = self.posY + self.optionBiasY
        for option in self.options:
            if not option.isHidden:
                if option.isDisabled:
                    self.engine.drawText(self.textScope, currentX, currentY, option.text, Color.DARK_GRAY)
                else:
                    self.engine.drawText(self.textScope, currentX, currentY, option.text)
                currentY += self.optionGap * option.heightUnit

    def updateOptions(self):
        self.isOptionValid = False
        self.optionMinIndex = len(self.options)
        self.optionMaxIndex = 0
        self.optionHeightUnits = [-1] * len(self.options)
        unit = 0
        for index, option in enumerate(self.options):
            if not option.isHidden:
                self.isOptionValid = True
                self.optionMinIndex = min(self.optionMinIndex, index)
                self.optionMaxIndex = max(self.optionMaxIndex, index)
                self.optionHeightUnits[index] = unit
                unit += option.heightUnit

    def checkKeyboard(self):
        if self.isShowCursor:
            self.moveCursor()

    def moveCursor(self):
        if self.engine.keyPressed_UP:
            if self.cursorIndex == self.optionMinIndex:
                if self.isOptionCyclic:
                    self.cursorIndex = self.optionMaxIndex
            else:
                self.cursorIndex -= 1
                while self.options[self.cursorIndex].isHidden:
                    self.cursorIndex -= 1
        elif self.engine.keyPressed_DOWN:
            if self.cursorIndex == self.optionMaxIndex:
                if self.isOptionCyclic:
                    self.cursorIndex = self.optionMinIndex
            else:
                self.cursorIndex += 1
                while self.options[self.cursorIndex].isHidden:
                    self.cursorIndex += 1
        elif self.engine.keyPressed_ENTER:
            if not self.options[self.cursorIndex].isDisabled:
                self.options[self.cursorIndex].onEnter()


class MainMenu(Menu):

    def __init__(self, engine: 'Engine'):
        super().__init__(engine)
        self.textScope = TextScope.SYS
        self.posX = self.engine.conf_WIN_WIDTH // 2
        self.posY = self.engine.conf_WIN_HEIGHT // 2
        self.titleFontSize = self.engine.conf_SYS_FONT_SIZE_TITLE
        self.optionFontSize = self.engine.conf_SYS_FONT_SIZE
        self.initAll()

    def initTitle(self):
        self.titleText = 'Chat Game'
        self.titleBiasY = -240

    def initCursor(self):
        self.cursorText = '*'
        self.cursorRect = PYG.Rect(0, 0, self.optionFontSize, self.optionFontSize)
        self.cursorBiasX = -100
        self.cursorBiasY = 10

    def initOptions(self):
        # Options
        optionOptions = MenuOption('Options')

        def onOptionOptionsEnter():
            self.engine.addView('OptionMenu', OptionMenu(self.engine))
            self.engine.removeView('MainMenu')

        optionOptions.onEnter = onOptionOptionsEnter

        # Credits
        optionCredits = MenuOption('Credits')

        def onOptionCreditsEnter():
            self.engine.addView('CreditMenu', CreditMenu(self.engine))
            self.engine.removeView('MainMenu')

        optionCredits.onEnter = onOptionCreditsEnter

        # Exit
        optionExit = MenuOption('Exit')

        def onOptionExitEnter():
            self.engine.exit()
        
        optionExit.onEnter = onOptionExitEnter

        # Final
        self.options = [
            MenuOption('Start', isDisabled=True),
            optionOptions,
            optionCredits,
            optionExit,
        ]
        self.optionGap = 75


class CreditMenu(Menu):

    def __init__(self, engine: 'Engine'):
        super().__init__(engine)
        self.textScope = TextScope.SYS
        self.posX = self.engine.conf_WIN_WIDTH // 2
        self.posY = self.engine.conf_WIN_HEIGHT // 2
        self.titleFontSize = self.engine.conf_SYS_FONT_SIZE_TITLE
        self.optionFontSize = self.engine.conf_SYS_FONT_SIZE
        self.initAll()

    def initTitle(self):
        self.titleText = 'Credits'
        self.titleBiasY = -300

    def initCursor(self):
        self.isShowCursor = False

    def initOptions(self):
        self.options = [
            MenuOption('Programmer:  Z.B. Weng'),
            MenuOption('Designer:  Z.B. Weng'),
            MenuOption('', heightUnit=4),
            MenuOption('Powered by pygame.'),
        ]
        self.optionBiasY = -200
        self.optionGap = 75

    def checkKeyboard(self):
        if self.engine.keyPressed_BACK or self.engine.keyPressed_ENTER:
            self.engine.addView('MainMenu', MainMenu(self.engine))
            self.engine.removeView('CreditMenu')


class OptionMenu(Menu):

    def __init__(self, engine: 'Engine'):
        super().__init__(engine)
        self.textScope = TextScope.SYS
        self.posX = self.engine.conf_WIN_WIDTH // 2
        self.posY = self.engine.conf_WIN_HEIGHT // 2
        self.titleFontSize = self.engine.conf_SYS_FONT_SIZE_TITLE
        self.optionFontSize = self.engine.conf_SYS_FONT_SIZE
        self.initAll()

    def initTitle(self):
        self.titleText = 'Options'
        self.titleBiasY = -300

    def initCursor(self):
        self.cursorText = '*'
        self.cursorRect = PYG.Rect(0, 0, self.optionFontSize, self.optionFontSize)
        self.cursorBiasX = -250
        self.cursorBiasY = 10

    def initOptions(self):
        self.options = [
            MenuOptionSelect('Platform', [
                'Youtube',
                'Twitch',
            ], isDisabled=True),
            MenuOptionEntry('Video ID', self.engine.helper),
        ]
        self.optionBiasY = -200
        self.optionGap = 75

    def checkKeyboard(self):
        if self.engine.keyPressed_BACK:
            self.engine.addView('MainMenu', MainMenu(self.engine))
            self.engine.removeView('OptionMenu')
        else:
            super().checkKeyboard()
