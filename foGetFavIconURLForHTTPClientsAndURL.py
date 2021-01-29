import re;

from mHTTP.mExceptions import cHTTPException, cTCPIPException, cSSLException;
from oConsole import oConsole;

from mColors import *;

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
      ["Requesting ", INFO, str(oURL), NORMAL] +
      ([" through ", INFO, str(oProxyServerURL), NORMAL] if oProxyServerURL else []) +
      [" to look for favicon..."]
    ));
    try:
      oResponse = oHTTPClient.fozGetResponseForURL(oURL);
    except (cHTTPException, cTCPIPException, cSSLException) as oException:
      if gbDebug:
        oConsole.fPrint(*(
          [WARNING, "Requesting ", WARNING_INFO, str(oURL), WARNING] +
          ([" through ", WARNING_INFO, str(oProxyServerURL), WARNING] if oProxyServerURL else []) +
          [" failed: ", WARNING_INFO, str(oException), WARNING, "!"]
        ));
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
        oConsole.fPrint(
          WARNING, "- ", WARNING_INFO, str(oURL), WARNING,
          " refers to a non-ascii favicon URL: ", WARNING_INFO, repr(oFavIconLinkElementMatch.group(1)), WARNING, "!"
        );
      else:
        oFavIconURL = oURL.foFromRelativeString(sFavIconURL);
    # See if there is a "/favicon.ico" on the server.
    oConsole.fStatus(*(
      ["Requesting ", INFO, str(oFavIconURL), NORMAL] +
      ([" through ", INFO, str(oProxyServerURL), NORMAL] if oProxyServerURL else []) +
      [" to check favicon..."]
    ));
    try:
      oResponse = oHTTPClient.fozGetResponseForURL(oFavIconURL);
    except (cHTTPException, cTCPIPException, cSSLException) as oException:
      oConsole.fPrint(*(
        [WARNING, "- Cannot retrieve ", WARNING_INFO, str(oURL), WARNING] +
        ([" through ", INFO, str(oProxyServerURL), NORMAL, " "] if oProxyServerURL else []) +
        [": ", WARNING_INFO, str(oException), WARNING, "!"]
      ));
      return None;
    assert oResponse is not None, \
        "HTTP Response should not be None!"; # This can only happen if the client is stopping and we control the client and should not have stopped it.
    if oResponse.uStatusCode != 200:
      oConsole.fPrint(
        WARNING, "- Cannot retrieve ", WARNING_INFO, str(oURL), WARNING, ": the server responded with ",
        WARNING_INFO, "HTTP ", str(oResponse.uStatusCode), " ", oResponse.sReasonPhrase, WARNING, "!"
      );
      return None;
    else:
      if gbDebug:
        oConsole.fPrint(
          "* FavIcon URL for ", INFO, str(oURL), NORMAL, ": ", INFO, str(oFavIconURL), NORMAL, "."
        );
      return oFavIconURL;
  oConsole.fPrint(WARNING, "- Cannot retrieve ", WARNING_INFO, str(oURL), WARNING, " through any HTTP client.");
  return None;