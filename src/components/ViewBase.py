from abc import ABC, abstractmethod


class ViewBase(ABC):

    def handle(self):
        self.draw()
        self.checkKeyboard()

    @abstractmethod
    def draw(self):
        '''Draw component contents.'''
        return NotImplemented

    def checkKeyboard(self):
        '''check component input event.'''
        return NotImplemented
