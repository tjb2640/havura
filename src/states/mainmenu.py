import typing

from states.base import BaseState

from key import Key
from statesignal import StateSignal
from trigger import Trigger

'''
Displays hardcoded main program options
'''
class MainMenuState(BaseState):
    pos_x = None
    pos_y = None
    options_start_y = None
    data = None
    term = None
    current_choice = None
    setting_option_width = 37
    descriptive_text_width = 36
    descriptive_text_height = 15

    def __action_back(stateref):
        return (StateSignal.BACK, None)
    
    def __action_pass(stateref):
        return (StateSignal.PASS, None)

    @classmethod
    def __init__(self, term):
        self.term = term
        self.options_start_y = 5
        self.current_choice = 0
        self.data = {}
        # Hardcode the menu options with descriptions
        self.data['options'] = [
            {
                'key': 'browse',
                'text': 'Browse',
                'help': 'Read Jewish texts in English courtesy of Sefaria.',
                'action': self.__action_pass
            },
            {
                'key': 'github',
                'text': 'Open GitHub',
                'help': 'Opens your browser and takes you to the Havura project\'s GitHub page.',
                'action': self.__action_pass
            },
            {
                'key': 'quit',
                'text': 'Quit to terminal',
                'help': 'Exits havura and returns to the terminal.',
                'action': self.__action_back
            }
        ]
        pass

    '''
    Draws everything related to a single menu text option.
    Abstracted so that we don't have to redraw the entire screen when options are selected.
    '''
    @classmethod
    def _draw_menu_option(self, option_number):
        T = self.term

        is_current = self.current_choice == option_number # (self.options_start_y + option_number) == self.pos_y
        draw_y = self.options_start_y + option_number
        option_text = self.data['options'][option_number]['text']

        # Print extended background color color if we're printing the currently-selected option
        if is_current:
            T.text_highlighted(self.pos_x, draw_y, self.setting_option_width, ' >> ' + option_text)
        else:
            T.text_normal(self.pos_x, draw_y, self.setting_option_width, option_text)

        # TODO: draw option and its description in the description box on the right side
    
    @classmethod
    def _draw(self, reason: Trigger):
        T = self.term
        if reason == Trigger.ACTIVATED:
            # Top bar which says "Main Menu" and instructions
            T.echo(T.clear + T.move_xy(self.pos_x, self.pos_y) + \
                T.gray100_on_cornflowerblue(T.center(T.bold + "Main Menu")))
            self.pos_x = 2
            self.pos_y = 2
            print(T.move_xy(self.pos_x, self.pos_y) + "Use the up/down keys and hit return to select an option.")

            # Options
            self.pos_y = self.options_start_y
            for option_number in range(0, len(self.data['options'])):
                self._draw_menu_option(option_number)

            # Box on the right
            T.draw_box(41, self.options_start_y - 1, self.descriptive_text_width + 1, self.descriptive_text_height + 1)
        pass
    
    @classmethod
    def activate(self) -> StateSignal:
        self.pos_x = 0
        self.pos_y = 0
        self._draw(Trigger.ACTIVATED)
        return StateSignal.OK
    
    @classmethod
    def close(self) -> StateSignal:
        return StateSignal.OK

    '''
    Arrow up/down: cycle menu options
    Enter: select an option
    '''
    @classmethod
    def input(self, inp) -> (StateSignal, str):
        # are we trying to select an option?
        if inp == Key.ENTER.value:
            return self.data['options'][self.current_choice]['action'](self)
        
        # rotate the menu option if navigating with arrow keys
        old_choice = self.current_choice
        if inp == Key.UP.value:
            self.current_choice = (old_choice - 1) % len(self.data['options'])
        elif inp == Key.DOWN.value:
            self.current_choice = (old_choice + 1) % len(self.data['options'])

        # redraw the old selection and the new selection if changed
        if not (old_choice == self.current_choice):
            self._draw_menu_option(old_choice)
            self._draw_menu_option(self.current_choice)

        return (StateSignal.OK, None)
