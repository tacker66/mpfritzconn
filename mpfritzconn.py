#
# A minimalistic solution to connect to an AVM FritzBox using MicroPython
#
# FritzBox API:
#   - https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AHA-HTTP-Interface.pdf
#   - https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AVM_Technical_Note_-_Session_ID.pdf
#
# As MicroPython lacks proper implementations of an XML parser, MD5 hash generation
# and UTF-16LE string encoding these things are all done by hand in a minimalistic way:
#   - Extracting SID and Challenge from the FritBox's XML response is done by string.replace()/split() with some magic chars
#   - The UTF-16LE encoding of the Challenge Response is done in MicroPython and only works for ASCII strings
#   - The MD5 hash for the Challenge Response is computed using Mauro Rivas MicroPython implementation (Thx!)
#
# Installation:
#   - mip.install("github:tacker66/mpfritzconn")
#

import md5
import requests

class MpFritzConn:

    def __init__(self, user, password, url):
        self.url      = url
        self.user     = user
        self.password = password
        self.sid = self.get_sid()

    def ascii2utf16le(self, msg):
        msg = bytearray(msg.encode('utf-8'))
        buf = bytearray()
        for c in msg:
            buf.append(c)
            buf.append(0)
        return(buf)

    def get_md5(self, challenge, password):
        s = self.ascii2utf16le(challenge)
        s = s + self.ascii2utf16le('-')
        s = s + self.ascii2utf16le(password)
        return md5.digest(s)
        
    def get_sid(self):
        r = requests.get(self.url + '/login_sid.lua')
        s = r.text
        s = s.replace("<SID>", "|")
        s = s.replace("</SID>", "|")
        sid = s.split("|")[1]
        s = s.replace("<Challenge>", "€")
        s = s.replace("</Challenge>", "€")
        cha = s.split("€")[1]
        if sid == '0000000000000000':
            res = cha + '-' + self.get_md5(cha, self.password)
            r = requests.get(self.url + '/login_sid.lua?username=' + self.user + '&response=' + res)
            s = r.text
            s = s.replace("<SID>", "|")
            s = s.replace("</SID>", "|")
            sid = s.split("|")[1]
        if sid == '0000000000000000':
            raise Exception('access denied')
        return sid
        
    def call(self, cmd, ain=None):
        if ain:
            uri = self.url + '/webservices/homeautoswitch.lua?ain=' + ain + '&switchcmd=' + cmd + '&sid=' + self.sid
        else:
            uri = self.url + '/webservices/homeautoswitch.lua?switchcmd=' + cmd + '&sid=' + self.sid
        return requests.get(uri).text

if __name__=='__main__':
    adr = "http://xx.xx.xx.xx"
    usr = "<username>"
    pwd = "<password>"
    ain = "<DeviceAIN>"
    fc = MpFritzConn(usr, pwd, adr)
    ret = fc.call("getswitchname", ain)
    print("Name:", ret.strip())
    ret = fc.call("getswitchstate", ain)
    print("State:", ret.strip())
    ret = fc.call("getswitchpower", ain)
    print("Power:", ret.strip())
    ret = fc.call("gettemperature", ain)
    print("Temp:", ret.strip())
