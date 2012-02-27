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

import random
import wx, wx.xrc

class Style:
    def playerColor(self,num):
        if num == 0:
            return wx.Color(255,0,0)
        if num == 1:
            return wx.Color(0,255,0)
        if num == 2:
            return wx.Color(0,0,255)
        if num == 3:
            return wx.Color(0,255,255)

    def drawShapeBack(self, dc):
      dc.SetBackground(wx.Brush(wx.Color(100,100,100)))
      dc.Clear()

    def drawCard(self, dc, color, filling, number, type, size):
      width = size[0]
      height = size[1]
      color_list = [wx.Color(0,255,0), wx.Color(255,0,0), wx.Color(0,0,255)]
      filling_list = [wx.TRANSPARENT, wx.SOLID, wx.FDIAGONAL_HATCH]
      brush = wx.Brush(color_list[color],filling_list[filling])
      pen = wx.Pen(color_list[color],1)
      shiftx = width / 20
      shifty = height / 10
      scalex = width - shiftx * 2
      scaley = (height - shifty * 2) / 4
      shift = height / 10
      for a in range(number+1):
        self.drawShape(dc, pen, brush, type,
                       shiftx, shift, scalex, scaley)
        shift += scaley+ shifty

    def drawShape(self,dc,p,b,shape,x,y,width,height):
        scaley = height/3
        scalex = width/2
        dc.SetBrush(b)
        dc.SetPen(p)
        if shape== 0:
            poly = [(x,scaley*2+y),
                    (x+scalex,scaley+y),
                    (x+2*scalex,scaley*2+y),
                    (x+scalex,scaley*3+y)]
            dc.DrawPolygon(poly, 0,0)
        elif shape== 1:
            dc.DrawEllipse(x, y, width, height)
        else:
            dc.DrawRectangle(x, y, width, height)

    def drawSelect(self,dc,a):
        pen = wx.Pen(self.playerColor(a))
        dc.SetPen(pen)
        dc.DrawLine(0+a*10,0,100-a*10,100)
        dc.DrawLine(0+a*10,100,100-a*10,0)

    def drawBack(self, dc):
        dc.SetBackground(wx.Brush(wx.Color(200,200,200)))
        dc.Clear()

    def drawBackground(self, dc):
        color = wx.Color(51, 255, 51)
        fill = wx.SOLID
        dc.SetBrush(wx.Brush(color, fill))
        dc.DrawRectangle(0, 0, 1000, 1000)

    def imageNoStateSet(self, size):
      i = wx.Image("noinfo.png")
      i = i.Scale(size[0], size[1])
      return i.ConvertToBitmap()

    def imageRightSet(self, size):
      i = wx.Image("check.png")
      i = i.Scale(size[0], size[1])
      return i.ConvertToBitmap()

    def imageWrongSet(self, size):
      i = wx.Image("x.png")
      i.Rescale(size[0], size[1])
      return i.ConvertToBitmap()



class Style2(Style):
    def drawBack(self, dc):
        dc.DrawBitmap(self.card,0,0)

    def __init__(self):
        self.back = wx.Bitmap("back.png")
        self.card = wx.Bitmap("card.png")

    #def drawSelect(self,dc,a):
    #    b = wx.Pen(self.playerColor(a))
    #    dc.SetPen(b)
    #    player_name = "Player %s" % a
    #    dc.DrawText(player_name, 10, a*20)
    #    #dc.DrawLine(0+a*10,0,100-a*10,100)
    #    #dc.DrawLine(0+a*10,100,100-a*10,0)
    def drawShapeBack(self, dc):
      dc.SetBackground(wx.Brush(wx.Color(0,0,118)))
      #dc.SetBackground(wx.Brush(wx.Color(255,255,255)))
      dc.Clear()

    def drawBackground(self, dc):
        dc.DrawBitmap(self.back,0,0)

    def drawShapeTest(self,dc,p,b,shape,x,y,width,height):
        scaley = height/3
        scalex = width/2
        dc.SetBrush(b)
        dc.SetPen(p)
        if shape== 0:
            poly = [(x,scaley*2+y),
                    (x+scalex,scaley+y),
                    (x+2*scalex,scaley*2+y),
                    (x+scalex,scaley*3+y),
                    (x,scaley*2+y)]
            dc.DrawSpline(poly)
            dc.FloodFill(poly[0][0]+1, poly[0][1]+1, wx.Color(0,0,0))
        elif shape== 1:
            dc.DrawEllipse(x, y, width, height)
        else:
            dc.DrawRectangle(x, y, width, height)
