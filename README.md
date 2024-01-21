# mpfritzconn

A minimalistic solution to connect to an AVM FritzBox using MicroPython.

FritzBox API:
  - https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AHA-HTTP-Interface.pdf
  - https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AVM_Technical_Note_-_Session_ID.pdf

As MicroPython lacks proper implementations of an XML parser, MD5 hash generation
and UTF-16LE string encoding these things are all done by hand in a minimalistic way:
  - Extracting SID and Challenge from the FritBox's XML response is done by string.replace()/split() with some magic chars
  - The UTF-16LE encoding of the Challenge Response is done in MicroPython and only works for ASCII strings
  - The MD5 hash for the Challenge Response is computed using Mauro Rivas MicroPython implementation (Thx!)

Installation:
  - mip.install("github:tacker66/mpfritzconn")
