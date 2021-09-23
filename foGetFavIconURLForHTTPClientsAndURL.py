import re;

from mHTTPConnection.mExceptions import cHTTPException;
from mTCPIPConnection.mExceptions import cTCPIPException, cSSLException;
try: # mSSL support is optional
  from mSSL.mExceptions import cSSLException;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mSSL'":
    raise;
  tcException = (cHTTPException, cTCPIPException);
else:
  tcException = (cHTTPException, cTCPIPException, cSSLException);

from mConsole import oConsole;

from mColorsAndChars import *;

grFavIconLinkElement = re.compile(
  r'<link'
  r'(?:\s+\w+="[^"]+")*'
  r'\s+rel="(?:shortcut )icon"'
  r'(?:\s+\w+="[^"]+")*'
  r'\s+href="([^"]+)"'
  r'\s*\/?>',
  re.I
);
gbDebug = False;

def foGetFavIconURLForHTTPClientsAndURL(aoHTTPClients, oURL):
  if len(aoHTTPClients) == 0:
    return None;
  for oHTTPClient in aoHTTPClients:
    # Load the page and see if there is a <link ... rel="icon" ... href="..."> element in it.
    oProxyServerURL = oHTTPClient.foGetProxyServerURL();
    oConsole.fStatus(*(
      ["Requesting ", COLOR_INFO, str(oURL), COLOR_NORMAL] +
      ([" through ", COLOR_INFO, str(oProxyServerURL), COLOR_NORMAL] if oProxyServerURL else []) +
      [" to look for favicon..."]
    ));
    try:
      oResponse = oHTTPClient.fozGetResponseForURL(oURL);
    except tcExceptions as oException:
      if gbDebug:
        oConsole.fOutput(
          COLOR_WARNING, CHAR_WARNING,
          COLOR_NORMAL, " Requesting ",
          COLOR_INFO, str(oURL),
          [
            COLOR_NORMAL, " through ",
            COLOR_INFO, str(oProxyServerURL),
          ] if oProxyServerURL else [],
          COLOR_NORMAL, " failed: ",
          COLOR_INFO, str(oException),
          COLOR_NORMAL, "!",
        );
      continue; # This HTTP client cannot retreive the page; try the next client.
    assert oResponse is not None, \
        "HTTP Response should not be None!"; # This can only happen if the client is stopping and we control the client and should not have stopped it.
    # See if there is a "/favicon.ico" on the server.
    oFavIconLinkElementMatch = (
      grFavIconLinkElement.search(oResponse.szData or "") if oResponse.uStatusCode == 200 and oResponse.szMediaType == "text/html" \
      else None
    );
    oFavIconURL = oURL.foFromRelativeString("/favicon.ico"); # The default value unless the webpage specifies a different URL
    if oFavIconLinkElementMatch is not None:
      try:
        sFavIconURL = str(oFavIconLinkElementMatch.group(1));
      except:
        oConsole.fOutput(
          COLOR_WARNING, CHAR_WARNING,
          " ",
          COLOR_INFO, str(oURL),
          COLOR_NORMAL, " refers to a non-ascii favicon URL: ",
          COLOR_INFO, repr(oFavIconLinkElementMatch.group(1)),
          COLOR_WARNING, "!",
        );
      else:
        oFavIconURL = oURL.foFromRelativeString(sFavIconURL);
    # See if there is a "/favicon.ico" on the server.
    oConsole.fStatus(
      COLOR_BUSY, CHAR_BUSY, 
      COLOR_NORMAL, " Requesting ",
      COLOR_INFO, str(oFavIconURL),
      [
        COLOR_NORMAL, " through ",
        COLOR_INFO, str(oProxyServerURL),
      ] if oProxyServerURL else [],
      COLOR_NORMAL, " to check favicon...",
    );
    try:
      oResponse = oHTTPClient.fozGetResponseForURL(oFavIconURL);
    except tcExceptions as oException:
      oConsole.fOutput(
        COLOR_WARNING, CHAR_WARNING,
        COLOR_NORMAL, " Cannot retrieve ",
        COLOR_INFO, str(oURL),
        [
          COLOR_NORMAL, " through ",
          COLOR_INFO, str(oProxyServerURL),
        ] if oProxyServerURL else [],
        COLOR_NORMAL, ": ",
        COLOR_INFO, str(oException),
        COLOR_NORMAL, "!",
      );
      return None;
    assert oResponse is not None, \
        "HTTP Response should not be None!"; # This can only happen if the client is stopping and we control the client and should not have stopped it.
    if oResponse.uStatusCode != 200:
      oConsole.fOutput(
        COLOR_WARNING, CHAR_WARNING,
        COLOR_NORMAL, " Cannot retrieve ",
        COLOR_INFO, str(oURL),
        COLOR_NORMAL, ": the server responded with ",
        COLOR_INFO, "HTTP ", str(oResponse.uStatusCode), " ", str(oResponse.sbReasonPhrase, 'latin1'),
        COLOR_NORMAL, "!"
      );
      return None;
    else:
      if gbDebug:
        oConsole.fOutput(
          COLOR_INFO, CHAR_INFO,
          COLOR_NORMAL, " FavIcon URL for ",
          COLOR_INFO, str(oURL),
          COLOR_NORMAL, ": ",
          COLOR_INFO, str(oFavIconURL),
          COLOR_NORMAL, ".",
        );
      return oFavIconURL;
  oConsole.fOutput(
    COLOR_WARNING, CHAR_WARNING,
    COLOR_NORMAL, " Cannot retrieve ",
    COLOR_INFO, str(oURL),
    COLOR_NORMAL, " through any HTTP client.",
  );
  return None;