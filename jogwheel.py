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
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
import kivy.uix.behaviors 
import kivy.uix 
import kivy.resources
import kivy.resources
import os

jogger_res_path=os.path.basename(__file__)

class JogWheelBehavior(object):
    trigger_distance = NumericProperty(4)
    orientation = OptionProperty('horizontal', options=['horizontal', 'vertical'])

    def __init__(self, *args, **kwargs):
        super(JogWheelBehavior, self).__init__(*args,**kwargs)
        self.do_orientation(self, self.orientation)
        self.dsx_collector=0
        self.dsy_collector=0

        self.register_event_type('on_jog')

        self.bind(on_touch_down=self.register_touch)
        self.bind(on_touch_move=self.slide)
        self.bind(on_touch_up=self.unregister_touch)
        self.bind(orientation=self.do_orientation)

    def register_touch(self, o, touch):
        if self.collide_point(touch.x, touch.y):
            touch.grab(self)

    def slide(self,o,event):
        if not event.grab_current is self:
            return True
        self._slide(event)
    
    def slide_x(self,event):
        self.dsx_collector += event.dx
        sign= 0 if self.dsx_collector==0 else (self.dsx_collector/abs(self.dsx_collector))
        while abs(self.dsx_collector) > self.trigger_distance:
            self.dsx_collector -= sign * self.trigger_distance
            self.dispatch('on_jog', self, sign)

    def slide_y(self,event):
        self.dsy_collector += event.dy
        sign= 0 if self.dsy_collector==0 else (self.dsy_collector/abs(self.dsy_collector)) 
        while abs(self.dsy_collector) > self.trigger_distance:
            self.dsy_collector -= sign * self.trigger_distance
            self.dispatch('on_jog', self, sign)

    def do_orientation(self, val, *args):
        if self.orientation == 'horizontal':
            self._slide = self.slide_x
        else:
            self._slide = self.slide_y
             
    def on_jog(self, obj, val):
        pass

    def unregister_touch(self, o, event):
        if event.grab_current is self:
            event.ungrab(self)

        self.dsx_collector=0
        self.dsy_collector=0

class NumericJogWheelBehavior(JogWheelBehavior):
    value = NumericProperty(0)
    minimum = NumericProperty(-1.0)
    maximum = NumericProperty(+1.0)
    step = NumericProperty(0.1)

    def do_jog(self, o, o2, direction):
        value = self.value
        value += direction * self.step
        value = value if value >= self.minimum else self.minimum 
        value = value if value <= self.maximum else self.maximum
        self.value = value

    def __init__(self, *args, **kwargs):
        super(NumericJogWheelBehavior,self).__init__(*args, **kwargs)
        self.bind(on_jog=self.do_jog)


class JogWheelRenderer(Widget ):
    thickness = NumericProperty(cm(0.2))
    graded = BooleanProperty(True)
    def update_dims(self, *args):
        inited=True
        try:
            self.rect
        except:
            inited = False
        bdir = os.path.dirname(__file__)
        bdir = bdir if bdir else os.path.curdir
        if inited:
            if self.orientation == 'horizontal':
                self.rect.size=(self.width, self.thickness)
                self.rect.pos = [self.x+0, self.y+((self.height - self.thickness)/2.0)]
                if self.graded:
                    fpath= os.path.sep.join([bdir,'JogWheel_graded_horizontal.jpg'])
                    self.rect.source = fpath

                else:
                    fpath = os.path.sep.join([bdir,'JogWheel_ungraded_horizontal.jpg'])
                    self.rect.source = fpath
            else:
                self.rect.size=(self.thickness, self.height)
                self.rect.pos = [self.x+((self.width - self.thickness)/2.0), self.y]
                if self.graded:
                    fpath= os.path.sep.join([bdir,'JogWheel_graded_vertical.jpg'])
                    self.rect.source = fpath
                else:
                    fpath= os.path.sep.join([bdir,'JogWheel_ungraded_vertical.jpg'])
                    self.rect.source = fpath

    def __init__(self, *args, **kwargs):
        super(JogWheelRenderer,self).__init__( *args, **kwargs)

        with self.canvas:
            #Color(0.6,0.6,0.6,.7)
            self.rect = Rectangle()

        self.bind(size = self.update_dims,
                  pos  = self.update_dims,
                  thickness   = self.update_dims,
                  orientation = self.update_dims)

        self.update_dims()


class JogWheel(JogWheelRenderer, JogWheelBehavior):
    #def on_orientation(self, o, orientation):
    #    JogWheelBehavior.on_orientation(self, o, orientation)
    pass
    

class NumericJogWheel(JogWheelRenderer, NumericJogWheelBehavior):
    #def on_orientation(self, o, orientation):
    #    JogWheelBehavior.on_orientation(self, o, orientation)
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
            j = NumericJogWheel()
            j.minimum = -2
            j.maximum = 2 
            j.trigger_distance = cm(0.3)
            j.on_jog = updatelbl
            j.orientation = 'horizontal'
            j.graded = False
                
            b.add_widget(j)
            b.add_widget(lbl)
            return b
    ja = JogApp()
    ja.run()
