import json, xbmc, xbmcplugin, xbmcgui, xbmcaddon, locale, sys, urllib, urllib2, re, os, datetime, base64

def getUrl(url,data,user,pw):
      req = urllib2.Request(url,data)
      userpass = base64.encodestring('%s:%s' % (user, pw))[:-1]
      req.add_header('Authorization', 'Basic %s' % userpass)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

class PlayerEvents(xbmc.Player):
      def onPlayBackStarted(self):
        file = xbmc.Player().getPlayingFile()
        file = file.replace("\\\\","\\")
        ip=settings.getSetting("ip")
        port=settings.getSetting("port")
        user=settings.getSetting("user")
        pw=settings.getSetting("pw")
        while (ip=="" or port=="" or user=="" or pw==""):
          settings.openSettings()
          ip=settings.getSetting("ip")
          port=settings.getSetting("port")
          user=settings.getSetting("user")
          pw=settings.getSetting("pw")
        dialog = xbmcgui.Dialog()
        typeArray = [translation(30007),translation(30006),translation(30009)]
        nr=dialog.select(translation(30008), typeArray)
        if nr>=0:
          type = typeArray[nr]
          if type==translation(30006):
            xbmc.Player().stop()
            data = json.dumps({"jsonrpc": "2.0", "method": "Player.Open", "params": {"item": {"file": file}},  "id": 1})
            json_result = getUrl("http://"+ip+":"+port+"/jsonrpc",data,user,pw)
          elif type==translation(30009):
            xbmc.Player().stop()
            data = json.dumps({"jsonrpc": "2.0", "method": "Playlist.Add", "params": {"item": {"file": file}, "playlistid": 1}, "id": 1})
            json_result = getUrl("http://"+ip+":"+port+"/jsonrpc",data,user,pw)

addonID = "script.play.remote"
settings = xbmcaddon.Addon(id=addonID)
translation = settings.getLocalizedString
player=PlayerEvents()

while (not xbmc.abortRequested):
  xbmc.sleep(100)
