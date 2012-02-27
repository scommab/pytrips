# Copyright (C) 2005 Saul J B
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

import wx

class myButton(wx.BitmapButton):
    def __init__(self, frame, i):
        wx.BitmapButton.__init__(self, frame, -1, i)
        wx.EVT_PAINT(self, self.OnPaint)

    def OnPaint(self, event):
        paintDC = wx.PaintDC(self)
        self.PrepareDC(paintDC)
        w = self.GetSize().GetWidth()
        h = self.GetSize().GetHeight()
        scalex = w/2
        scaley = 5
        poly = [wx.Point(0,0),
                wx.Point(1*scalex,-1*scaley),
                wx.Point(2*scalex,0),
                wx.Point(1*scalex,1*scaley)]
        paintDC.DrawRectangle(0,0,w,10)
        paintDC.DrawEllipse(0,15,w, 10)
        paintDC.DrawPolygon(poly,0,30)

class HelloWorld(wx.App):
    def OnInit(self):
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        sizer = []
        sizer.append(wx.BoxSizer(wx.HORIZONTAL))
        sizer.append(wx.BoxSizer(wx.HORIZONTAL))
        sizer.append(wx.BoxSizer(wx.HORIZONTAL))
        sizer.append(wx.BoxSizer(wx.HORIZONTAL))
        frame = wx.Frame(None,-1,"hello world")
        buttons = []
        for a in sizer:
            for v in range(3):
                #a.Add(wx.Button(frame,  wx.ID_OK, 'OK'))
                i = wx.Bitmap("card.bmp")
                b = myButton(frame, i)
                #b = wx.Button(frame,  wx.ID_OK, 'OK')
                b.SetLabel("TEST")
                b.Fit()
                buttons.append(b)
                a.Add(b)
            MainSizer.Add(a)
        frame.SetSizer(MainSizer)
        frame.Show(1)
        self.SetTopWindow(frame)
        return 1 

app = HelloWorld(0)
app.MainLoop()
