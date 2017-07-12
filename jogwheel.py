#!/usr/bin/python
# The MIT License (MIT)
# Copyright (c) 2017 "Laxminarayan Kamath G A"<kamathln@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.



from kivy.properties import *
from kivy.metrics import  *
from kivy.event import EventDispatcher
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
import kivy.uix.behaviors 
import kivy.uix 



class JogWheelBehavior(object):
    trigger_distance = NumericProperty(4)
    orientation = OptionProperty('horizontal', options=['horizontal', 'vertical'])

    def __init__(self, *args, **kwargs):
        super(JogWheelBehavior, self).__init__(*args,**kwargs)
        self.on_orientation(self, self.orientation)
        self.dsx_collector=0
        self.dsy_collector=0

        self.register_event_type('on_jog')

        self.bind(on_touch_move=self.slide)
        self.bind(on_touch_up=self.unregister_touch)

    def register_touch(self, touch):
        touch.grab(self)

    def slide(self,o,event):
        self._slide(event)
    
    def slide_x(self,event):
        self.dsx_collector += event.dx
        sign= 0 if self.dsx_collector==0 else (self.dsx_collector/abs(self.dsx_collector))
        while abs(self.dsx_collector) > self.trigger_distance:
            self.dsx_collector -= sign * self.trigger_distance
            self.dispatch('on_jog', sign)

    def slide_y(self,event):
        self.dsy_collector += event.dy
        sign= 0 if self.dsy_collector==0 else (self.dsy_collector/abs(self.dsy_collector)) 
        while abs(self.dsy_collector) > self.trigger_distance:
            self.dsy_collector -= sign * self.trigger_distance
            self.dispatch('on_jog', sign)

    def on_orientation(self, val, *args):
        if self.orientation == 'horizontal':
            self._slide = self.slide_x
        else:
            self._slide = self.slide_y
             
    def on_jog(self, val):
        pass

    def unregister_touch(self, o, event):
        if event.grab_current is self:
            event.ungrab(self)

        self.dsx_collector=0
        self.dsy_collector=0

class NumericJogWheelBehavior(EventDispatcher,JogWheelBehavior):
    value = NumericProperty(0)
    minimum = NumericProperty(-1.0)
    maximum = NumericProperty(+1.0)
    step = NumericProperty(0.1)

    def on_jog(self, direction):
        value = self.value
        value += direction * self.step
        value = value if value >= self.minimum else self.minimum 
        value = value if value <= self.maximum else self.maximum
        self.value = value


class JogWheelRenderer(Widget ):
    thickness = NumericProperty(cm(1))
    def update_dims(self):
        if self.orientation == 'horizontal':
            self.rect.size=(self.width, self.thickness)
            #self.rect2.size=(self.width -4, self.thickness -4)
            self.rect.pos = [0, (self.height - self.thickness)/2.0]
            #self.rect2.pos = [1.0, ((self.height - self.thickness)/2.0)+2.0]
        else:
            self.rect.size=(self.thickness, self.height)
            #self.rect2.size=(self.thickness-4, self.height-4)
            self.rect.pos = [(self.width - self.thickness)/2.0, 0]
            #self.rect2.pos = [((self.width - self.thickness)/2.0) +2, 1.0]

    def on_size(self, o, size):
        self.update_dims()

    def on_pos(self, o, pos):
        self.update_dims()

    def on_thickness(self, o, pos):
        self.update_dims()

    def __init__(self, *args, **kwargs):
        super(JogWheelRenderer,self).__init__( *args, **kwargs)

        with self.canvas:
            Color(0.3,0.3,0.3,1)
            self.rect = RoundedRectangle() 
            #Color(0.5,0.5,0.55,1)
            #self.rect2 = RoundedRectangle()

class JogWheel(JogWheelRenderer, JogWheelBehavior):
    pass

class NumericJogWheel(JogWheelRenderer, NumericJogWheelBehavior):
    pass


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.label import Label
    import time

    class JogApp(App):
        def build(self):
            b = BoxLayout()
            lbl = Label(text='')
            def updatelbl(o,direction):
                lbl.text='Direction: %d, Time %.2f' % (direction, o.value)
            j = NumericJogWheel(orientation='vertical', 
                                minimum=-2, 
                                maximum=2, 
                                on_jog=updatelbl,
                                trigger_distance = cm(0.3))
                
            b.add_widget(j)
            b.add_widget(lbl)
            return b
    ja = JogApp()
    ja.run()
