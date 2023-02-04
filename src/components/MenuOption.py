from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from GameLib import Helper


class MenuOption:

    def __init__(self, text: str, heightUnit: int = 1, isDisabled: bool = False, isHidden: bool = False):
        self.text = text
        self.heightUnit = heightUnit
        self.isDisabled = isDisabled
        self.isHidden = isHidden

    def onEnter(self):
        return NotImplemented


class MenuOptionSelect(MenuOption):

    def __init__(self, text: str, selects: 'List[str]', heightUnit: int = 1, isDisabled: bool = False, isHidden: bool = False):
        super().__init__('', heightUnit, isDisabled, isHidden)
        self.selectedIndex = 0
        self.selectTitleText = text
        self.selects = selects
        self.updateText()

    def updateText(self):
        self.text = f"{self.selectTitleText}: {self.selects[self.selectedIndex]}"


class MenuOptionEntry(MenuOption):

    def __init__(self, text: str, helper: 'Helper', defaultValue: str = '', heightUnit: int = 1, isDisabled: bool = False, isHidden: bool = False):
        super().__init__('', heightUnit, isDisabled, isHidden)
        self.helper = helper
        self.selectedIndex = 0
        self.selectTitleText = text
        self.value = defaultValue
        self.updateText()

    def updateText(self):
        self.text = f"{self.selectTitleText}: {self.value}"

    def onEnter(self):
        self.value = self.helper.popupGetStr('A', 'b')
        self.updateText()
