from functools import partial

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRoundFlatButton

from multiplyBy11 import MultiplyBy11
from TwoDigitAddition import TwoDigitAddition
from ThreeByOneDigitMultiplication import ThreeByOneDigitMultiplication
from TwoDigitMultiplication import TwoDigitMultiplication


class MentalMathsApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"



        return self.menu()

    def printIDs(self):
        print(self.root.ids)

    def menu(self):
        nrounds = 3
        screen = MDScreen()
        btn1 = MDRoundFlatButton(text='Multiply by 11', pos_hint={'center_x': 0.5, 'center_y': 0.8},
                                 text_color=MDApp.get_running_app().theme_cls.primary_light,
                                 on_release=partial(MultiplyBy11, nrounds)
                                 )
        screen.add_widget(btn1)
        btn2 = MDRoundFlatButton(text='Two digit addition', pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                 text_color=MDApp.get_running_app().theme_cls.primary_light,
                                 on_release=partial(TwoDigitAddition, nrounds)
                                 )
        screen.add_widget(btn2)
        btn3 = MDRoundFlatButton(text='Three by one digit multiplication', pos_hint={'center_x': 0.5, 'center_y': 0.4},
                                 text_color=MDApp.get_running_app().theme_cls.primary_light,
                                 on_release=partial(ThreeByOneDigitMultiplication, nrounds)
                                 )
        screen.add_widget(btn3)
        btn4 = MDRoundFlatButton(text='Two digit multiplication', pos_hint={'center_x': 0.5, 'center_y': 0.2},
                                 text_color=MDApp.get_running_app().theme_cls.primary_light,
                                 on_release=partial(TwoDigitMultiplication, nrounds)
                                 )
        screen.add_widget(btn4)
        """
        
        selection = input("Select skill to practice:\n"
                          "1. Multiply by 11\n"
                          "2. Two digit addition\n"
                          "3. Three by one digit multiplication\n"
                          "4. Two digit multiplication\n"
                          )

        if selection == "1":
            MultiplyBy11(nrounds)
        if selection == "2":
            TwoDigitAddition(nrounds)
        if selection == "3":
            ThreeByOneDigitMultiplication(nrounds)
        if selection == "4":
            TwoDigitMultiplication(nrounds)
        """
        return screen


if __name__ == '__main__':
    MentalMathsApp().run()
