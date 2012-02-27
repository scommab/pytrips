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

import style

types = ["color", "number", "shape", "filling"]
typesOf = 3
class card:
    def __init__(self,vals):
        self.info = {}
        if vals == None:
            for t in types:
                self.info[t] = random.randint(0,typesOf-1)
        else:
            for t in types:
                self.info[t] = vals[t]

    def __eq__(self, other):
        if other == None:
            return 0
        for t in types:
            if self.info[t] != other.info[t]:
                return 0
        return 1

    def __getitem__(self, i):
        if i in types:
            return self.info[i]
        return None

    def __str__(self):
        hold = ""
        for t in types:
            hold += str(t) + ":"+ str(self.info[t]) + "\n"
        return hold

    def toImage(self,w,h,style):
        bitmap = wx.EmptyBitmap(w,h)
        dc = wx.MemoryDC()
        dc.SelectObject(bitmap)
        style.drawShapeBack(dc)
        style.drawCard(dc, self.info["color"], self.info["filling"], 
                       self.info["number"], self.info["shape"],
                       (w, h))
        dc.SelectObject(wx.NullBitmap)
        return bitmap

    def toText(self):
        normal = "\033[0;37m\033[0;40m"
        #        green              yellow       magenta
        color = {0:'\033[0;32m',1:'\033[0;33m',2:'\033[0;35m'}
        #           red             black            white
        filling = {0:'\033[0;41m',1:'\033[0;40m',2:'\033[0;47m'}
        shape = {0:'-',1:'/',2:'!'}
        me = color[self.info["color"]]
        #me += filling[self.info["filling"]] 
        me += shape[self.info["shape"]]
        me = me*4
        hold = []
        hold.append("|====|")
        for a in range(3):
            if self.info["number"] >= a:
                hold.append("|" + me + normal+"|")
            else:
                hold.append("|    |")
        hold.append("|====|")
        return hold


class setDeck:
    def __init__(self, s=None):
        self.deck = []
        self.reload()

    def reload(self):
        self.deck = []
        count = {}
        for a in types:
            count[a] = 0
        while(count[types[len(types)-1]] != typesOf):
            c = card(count)
            self.deck.append(c)
            count[types[0]] += 1
            for b in range(0,len(types)-1):
                if count[types[b]] == typesOf:
                    count[types[b+1]] += 1
                    count[types[b]] = 0

    def __str__(self):
        hold = ""
        for a in self.deck:
            hold += str(a) + "\n"
        return hold

    def __len__(self):
        return len(self.deck)
        
    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop(0)

    def insert(self,c):
        if not c in self.deck:
            self.deck.append(c)
            self.shuffle()

    def isset(self, c1,c2,c3):
        return self.whynotaset(c1,c2,c3) == None

    def whynotaset(self, c1,c2,c3):
        for t in types:
            if c1[t] == c2[t] and c2[t] == c3[t]:
                continue
            if c1[t] != c2[t] and c1[t] != c3[t] and c2[t] != c3[t]:
                continue
            return t
        return None
