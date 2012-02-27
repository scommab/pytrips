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
#
import random
import wx, wx.xrc

from deck import *
import style
import comp

class cardWidget(object):
    def backImage(self):
        bitmap = wx.EmptyBitmap(self.height, self.width)
        dc = wx.MemoryDC()
        dc.SelectObject(bitmap)
        self.parent.style.drawBack(dc)
        dc.SelectObject(wx.NullBitmap)
        return bitmap

    def __init__(self, parent, id, card, height=100,width=100):
        self.parent = parent
        self.height = height
        self.width = width 
        self.flip = 0
        self.card = card
        self.selected = {}
        self.id = id
    
    def toImage(self):
        if self.card == None or self.flip:
            return self.backImage()
        b = self.card.toImage(self.height,self.width,self.parent.style)
        dc = wx.MemoryDC()
        dc.SelectObject(b)
        dc.DrawBitmap(b,0,0)
        dc.SelectObject(wx.NullBitmap)
        for a in self.selected.keys():
            if self.selected[a]:
                dc = wx.MemoryDC()
                #bitmap = self.GetBitmapLabel()
                dc.SelectObject(b)
                self.parent.style.drawSelect(dc,a)
                dc.SelectObject(wx.NullBitmap)
        return b

    def Select(self, id):
        if not self.selected.has_key(id):
            self.selected[id] = 0
        if self.selected[id] == 0:
            self.selected[id] = 1
        else:
            self.selected[id] = 0
        self.Draw()
 
class cardButton(wx.BitmapButton, cardWidget):
    def __init__(self, parent, id, c, height=100,width=100):
        cardWidget.__init__(self, parent, id, c, height, width)
        wx.BitmapButton.__init__(self,parent,id, size=(height,width))
        self.Draw()
    
    def disable(self):
        self.Disable()
        self.flip = 1

    def enable(self):
        self.Enable()
        self.flip = 0

    def Draw(self):
        self.SetBitmapLabel(self.toImage())
        self.Update()

    def Click(self, id):
      self.Select(id)

class cardImage(wx.StaticBitmap, cardWidget):
    def __init__(self, parent, id, c, height=100,width=100):
        cardWidget.__init__(self, parent, id, c, height, width)
        wx.StaticBitmap.__init__(self,parent,id, size=(height,width))
        self.SetBitmap(self.toImage());

    def Draw(self):
        self.SetBitmap(self.toImage())
        

class Selected:
    def __init__(self, parent, name, isCurrentUser=False):
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.Clean = None
        self.total = 0
        self.SetsTotal = 0
        self.parent = parent
        self.buttons = []
        card_size = (50, 50)
        info_size = (30, 30)
        if isCurrentUser:
          card_size = (80, 80)
          info_size = (50, 50)
        self.emptyInfo = self.parent.style.imageNoStateSet(info_size)
        self.emptyRight = self.parent.style.imageRightSet(info_size)
        self.emptyWrong = self.parent.style.imageWrongSet(info_size)
        nameText = wx.StaticText(self.parent, -1, name)
        self.sizer.Add(nameText, wx.ALIGN_LEFT, 1)
        for v in range(3):
            b = cardImage(self.parent, -1, None,height=card_size[0],width=card_size[1])
            #b.Enable(False)
            b.Fit()
            self.buttons.append(b)
            self.sizer.Add((5,5))
            self.sizer.Add(b)
        # TODO convert this to be an image and text 
        self.text = wx.StaticText(self.parent, -1, "")
        self.setInfo = wx.StaticBitmap(self.parent, -1, size=info_size)
        self.setInfo.SetBitmap(self.emptyInfo)
        self.textSets = wx.StaticText(self.parent, -1, "Sets:0")
        self.sizer.Add((10,10))
        self.sizer.Add(self.setInfo, wx.ALIGN_LEFT, 1)
        self.sizer.Add(self.text, wx.ALIGN_LEFT, 1)
        self.sizer.Add(self.textSets, wx.ALIGN_LEFT, 1)
        self.sizer.Layout()
        self.AmPause = 0

    def pause(self):
        if not self.AmPause:
            for a in self.buttons:
                a.disable()
                a.Draw()
                a.Refresh()
            self.AmPause = 1
        else:
            for a in self.buttons:
                a.enable()
                a.Draw()
                a.Refresh()
            self.AmPause = 0

    def clear(self):
        self.removeAll()
        self.SetsTotal = 0
        self.textSets.SetLabel("Sets:" + str(self.SetsTotal))
        self.sizer.Layout()

    def isSet(self):
      self.addToSets()
      self.settext("Set")
      self.setInfo.SetBitmap(self.emptyRight)

    def isNotSet(self, reason=""):
      self.settext(str(reason).capitalize())
      self.setInfo.SetBitmap(self.emptyWrong)

    def addToSets(self):
        self.SetsTotal += 1
        self.textSets.SetLabel("Sets:" + str(self.SetsTotal))
        self.sizer.Layout()

    def settext(self, t):
        self.text.SetLabel(t)
        self.sizer.Layout()

    def add(self, b):
        if self.Clean != None:
            self.cleanUpWait()
        pick = None
        # find the next free button
        for a in range(len(self.buttons)):
            if self.buttons[a].id == -1:
                pick = a
                break
        if pick == None:
            return False
        self.total += 1
        self.buttons[a].id = b.id
        self.buttons[a].card = b.card
        self.buttons[a].Draw()
        self.buttons[a].Refresh()
        return True

    def remove(self, b, wait=0):
        if self.Clean != None:
            self.cleanUpWait()
        pick = None
        for a in range(len(self.buttons)):
            if self.buttons[a].id == b.id:
                pick = a
                break
        if pick == None:
            return 0
        self.total -= 1
        self.buttons[a].id = -1
        if wait != 1:
            self.buttons[a].card = None
        self.buttons[a].Draw()
        self.buttons[a].Refresh()
        return 1

    def removeAll(self):
        for a in self.buttons:
            self.remove(a)
        self.total = 0
        self.text.SetLabel("")
        self.text.Refresh()

    def removeAllSet(self):
        for a in self.buttons:
            self.remove(a,1)
        self.total = 0
        if self.Clean == None:
            self.Clean = wx.FutureCall(1500, self.cleanUpWait)
        else:
            self.Clean.Restart()

    def cleanUpWait(self):
        for a in self.buttons:
            if a.id == -1 and a.card != None:
                a.card = None
                a.Draw()
                a.Refresh()
        self.setInfo.SetBitmap(self.emptyInfo)
        self.text.SetLabel("")
        self.text.Refresh()
        self.Clean.Stop()
        self.Clean = None

    def ids(self):
        ids = []
        for a in self.buttons:
            if a.id != -1:
                ids.append(a.id)
        return ids

    def cards(self):
        cards = []
        for a in self.buttons:
            if a.id != -1:
                cards.append(a.card)
        return cards

class Timer:
    def __init__(self, parent):
        self.parent = parent
        self.TimerCall = None
        self.count = 0
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText(self.parent, -1, "")
        self.display()
        self.sizer.Add(self.text, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND)
        self.sizer.Layout()

    def display(self):
        hold = ""
        c = self.count
        sec  = self.count % 60
        min  = (self.count / 60) % 60
        min_total = self.count / 60
        hour = self.count / 60 / 60
        if hour == 1:
            hold += str(hour) + " Hour "
        elif hour > 0:
            hold += str(hour) + " Hours "
        if min == 1:
            hold += str(min) + " Minute "
        elif min > 0:
            hold += str(min) + " Minutes "
        if sec == 1:
            hold += str(sec) + " Second"
        elif sec >= 0:
            hold += str(sec) + " Seconds"
        self.text.SetLabel("%02d:%02d" % (min_total, sec))

    def start(self):
        if self.TimerCall == None:
            self.count = 0
            self.TimerCall = wx.FutureCall(1000,self.tick)
            return

    def pause(self):
        if self.TimerCall == None:
            self.TimerCall = wx.FutureCall(1000,self.tick)
        else:
            self.TimerCall.Stop()
            self.TimerCall = None

    def reset(self):
        self.count = 0
        self.display()
        self.stop() 

    def stop(self):
        if self.TimerCall != None:
            self.TimerCall.Stop()
            self.TimerCall = None

    def tick(self):
        self.count += 1
        self.display()
        self.sizer.Layout()
        self.parent.Layout()
        self.TimerCall.Restart()


class Table:

    def makeSizer(self):
        self.sizer.Clear()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.Timer.sizer,wx.CENTER,1)
        self.sizer.Add((5,5))
        self.sizer.Add(self.selectedCards[0].sizer)
        self.sizer.Add((10,10))
        count = 0
        for a in range(4):
            sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            for b in range(3):
                sizer2.Add(self.buttons[count])
                count += 1
                sizer2.Add((5,5))
            sizer.Add(sizer2)
            sizer.Add((5,5))
        sizer.Add(self.NothingLeft, wx.CENTER,1)
        self.sizer.Add(sizer)
        for a in range(1,4):
            self.sizer.Add(self.selectedCards[a].sizer)
            self.sizer.Hide(self.selectedCards[a].sizer)
            self.sizer.Add((10,10))
        self.parent.Layout()

    def numOthers(self,num):
        if num > 4:
            num = 4
        for a in range(1,num+1):
            self.sizer.Show(self.selectedCards[a].sizer)
        for a in range(num+1,4):
            self.sizer.Hide(self.selectedCards[a].sizer)
        self.sizer.Layout()
        self.parent.Layout()
        
    def __init__(self, parent, gameOverCallBack):
        self.parent = parent
        self.gameOverCallBack = gameOverCallBack
        self.Timer = Timer(self.parent)
        self.selectedCards = []
        # the first one is special since it is the current users
        self.selectedCards.append(Selected(self.parent, "Your Sets", isCurrentUser=True))
        for a in range(1,4):
            self.selectedCards.append(Selected(self.parent, "Player %d" % a))
        self.deck = setDeck(self.parent.style)
        self.deck.shuffle()
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.NothingLeft = wx.Button(self.parent, -1, "Nothing Left")
        wx.EVT_BUTTON(self.NothingLeft, -1, self.nothingLeftClick)
        self.buttons = []
        for a in range(4):
            for b in range(3):
                c= self.deck.deal()
                id = len(self.buttons)
                b = cardButton(self.parent, id, c)
                b.Fit()
                wx.EVT_BUTTON(b, id, self.OnButton)
                self.buttons.append(b)
        self.makeSizer()

    def nothingLeftClick(self, evn):
        self.Timer.start()
        self.nothingLeft(0)

    def OnButton(self, evn):
        self.Timer.start()
        self.click(evn.GetId(), 0)

    def restart(self):
        self.Timer.reset()
        self.deck.reload()
        self.deck.shuffle()
        for a in self.selectedCards:
            a.clear()
        for a in range(len(self.buttons)):
            self.deal(a)
        self.NothingLeft.Enable()

    def deal(self, id):
        if len(self.deck) > 0:
            self.buttons[id].card = self.deck.deal()
            self.buttons[id].selected={}
            self.buttons[id].Draw()
            self.buttons[id].Refresh()
            self.buttons[id].Enable()
        else:
            self.buttons[id].Disable()
            self.buttons[id].card = None
            self.buttons[id].selected={}
            self.buttons[id].Draw()
            self.buttons[id].Refresh()

    def couldBeDone(self):
        if len(self.deck) <= 0 and self.findSet() == None:
            self.gameOver()

    def pause(self):
        self.Timer.pause()
        if self.NothingLeft.IsEnabled(): 
            for a in self.selectedCards:
                a.pause()
            for a in self.buttons:
                a.disable()
                a.Draw()
                a.Refresh()
            self.NothingLeft.Disable()
        else:
            for a in self.selectedCards:
                a.pause()
            for a in self.buttons:
                a.enable()
                a.Draw()
                a.Refresh()
            self.NothingLeft.Enable()

    def gameOver(self):
        self.Timer.stop()
        self.gameOverCallBack()
        for a in self.buttons:
            a.Disable()
        self.NothingLeft.Disable()

    def findSet(self,f1=-1,f2=-1,f3=-1):
        ans1 = 0
        ans2 = 0
        ans3 = -1
        aR = range(len(self.buttons))
        bR = range(len(self.buttons))
        cR = range(len(self.buttons))
        if f1 != -1:
            aR = [f1]
        if f2 != -1:
            bR = [f2]
        if f3 != -1:
            cR = [f3]
        for a in aR:
            if not self.buttons[a].IsEnabled():
                continue
            for b in bR:
                if not self.buttons[b].IsEnabled() or a == b:
                    continue
                for c in cR:
                    if not self.buttons[c].IsEnabled() or c == a or c == b:
                        continue
                    if self.deck.isset(self.buttons[a].card,self.buttons[b].card,self.buttons[c].card):
                        ans1 = a
                        ans2 = b
                        ans3 = c
                        break
                if ans3 != -1: break
            if ans3 != -1: break

        if ans3 == -1:
            return None
        return (ans1,ans2,ans3)
 
    def nothingLeft(self,id=0):
        hold = self.findSet()
        if hold == None:
            for a in self.selectedCards:
                a.removeAll()
            for a in range(len(self.buttons)):
                if self.buttons[a].card == None:
                    continue
                self.deck.insert(self.buttons[a].card)
                self.deal(a)
            self.parent.Refresh()
            self.couldBeDone()
        else:
            wx.MessageBox("Still Sets Left","Sets Left" ,wx.OK|wx.CENTRE|wx.ICON_INFORMATION)

    # id = card id
    # Pid = player id
    def click(self, id, Pid):
        self.Timer.start()
        if id in self.selectedCards[Pid].ids():
            self.selectedCards[Pid].remove(self.buttons[id])
        else:
            self.selectedCards[Pid].add(self.buttons[id])
        self.buttons[id].Click(Pid)
        if self.selectedCards[Pid].total == 3:
            self.doSets(Pid)
            self.selectedCards[Pid].removeAllSet()
        self.buttons[id].Refresh()
        self.parent.Refresh()

    def doSets(self,id=0):
        cards = self.selectedCards[id].cards()
        ids = self.selectedCards[id].ids()
        ans = self.deck.whynotaset(cards[0],
                                   cards[1],
                                   cards[2])
        if ans == None:
            #is a set
            hold = None
            for a in ids:
                self.deal(a)
            self.selectedCards[id].isSet()
            for a in ids:
                for b in self.selectedCards:
                    if b != self.selectedCards[id]:
                        b.remove(self.buttons[a])
            self.couldBeDone()
        else:
            for a in ids:
                self.buttons[a].Click(id)
            self.selectedCards[id].isNotSet(ans)
        for a in ids:
            self.buttons[a].Refresh()
        self.parent.Refresh()

    def hint(self,id):
#        if self.NumClicks == 2:
#            return
        ans = -1
        if self.selectedCards[id].total == 0:
            #(a,b,c) = self.findSet()
            hold = self.findSet()
            if hold != None:
                ans = hold[0]
        elif self.selectedCards[id].total == 1:
            a = self.selectedCards[id].ids()[0]
            hold = self.findSet(a)
            if hold != None:
                ans = hold[1]
        else:
            ids = self.selectedCards[id].ids()
            a = ids[0]
            b = ids[1]
            hold = self.findSet(a,b)
            if hold != None:
                ans = hold[2]

        if ans != -1:
            self.click(ans,id)



class SetFrame(wx.Frame):
    def __init__(self, s=0):
        size = (512, 512)
        wx.Frame.__init__(self, None,-1,"Play Set",None,size)
        self.style = style.Style()
        wx.EVT_PAINT(self, self.OnPaint)
        self.SetMinSize(size)
        self.SetMaxSize(size)

    def OnPaint(self, event):
        self.style.drawBackground(wx.PaintDC(self))

    
class Set(wx.App):
 
    def Menu(self):
        menu = wx.MenuBar()
        res = wx.xrc.XmlResource_Get()
        res.Load('resources.xrc')
        self.frame.SetMenuBar(res.LoadMenuBar('menubar'))
        wx.EVT_MENU(self, wx.xrc.XRCID('exit'), self.CloseMe)
        wx.EVT_MENU(self, wx.xrc.XRCID('new'), self.Restart)
        wx.EVT_MENU(self, wx.xrc.XRCID('new2'), self.SetUpComp)
        wx.EVT_MENU(self, wx.xrc.XRCID('hint'), self.hint)
        wx.EVT_MENU(self, wx.xrc.XRCID('pause'), self.pause)
        wx.EVT_MENU(self, wx.xrc.XRCID('about'), self.about)
        
    def ChangeStyle(self):
        self.frame.style = style.Style2()
        self.table.updateStyle()
    
    def SetUpComp(self, event):
        self.Restart(None)
        self.table.numOthers(1)
        self.Comp = comp.CompPlayer(1, self.table, 2500)

    def GameOver(self):
        if self.Comp != None:
             self.Comp.stop()

    def Restart(self, event):
        if self.Comp != None:
            self.Comp.stop()
        self.table.restart()
        self.table.numOthers(0)
        self.frame.Refresh()
        return None

    def CloseMe(self,event):
        self.frame.Close()
        return None

    def hint(self,event,id=0):
        self.table.hint(id)

    def pause(self,event):
        self.table.pause();

    def about(self,event):
        wx.MessageBox("PyTrips\nBy: Saul J Bancroft","About" ,wx.OK|wx.CENTRE|wx.ICON_INFORMATION)
        return None
       
    def makeDisplay(self):
        MainSizer = wx.BoxSizer(wx.VERTICAL)#wx.BoxSizer(wx.HORIZONTAL)
        #Menu
        self.Menu()
        MainSizer.Add(self.table.sizer)#, wx.ALIGN_CENTER_HORIZONTAL,1)
        self.frame.SetSizer(MainSizer)
        self.frame.Layout()

        
    def OnInit(self):
        self.Comp = None
        self.frame = SetFrame()#wx.Frame(None,-1,"Play Set",None,(650,100*6))
        self.table = Table(self.frame,self.GameOver)
        self.makeDisplay()
        self.table.numOthers(0)
        self.frame.Show(1)
        self.SetTopWindow(self.frame)
        return 1 


def run():
  app = Set(0)
  app.MainLoop()

if __name__ == '__main__':
    run()
