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
    except tcExceptions as oException:
      if gbDebug:
        oConsole.fOutput(*(
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
        oConsole.fOutput(
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
    except tcExceptions as oException:
      oConsole.fOutput(*(
        [WARNING, "- Cannot retrieve ", WARNING_INFO, str(oURL), WARNING] +
        ([" through ", INFO, str(oProxyServerURL), NORMAL, " "] if oProxyServerURL else []) +
        [": ", WARNING_INFO, str(oException), WARNING, "!"]
      ));
      return None;
    assert oResponse is not None, \
        "HTTP Response should not be None!"; # This can only happen if the client is stopping and we control the client and should not have stopped it.
    if oResponse.uStatusCode != 200:
      oConsole.fOutput(
        WARNING, "- Cannot retrieve ", WARNING_INFO, str(oURL), WARNING, ": the server responded with ",
        WARNING_INFO, "HTTP ", str(oResponse.uStatusCode), " ", str(oResponse.sbReasonPhrase, 'latin1'), WARNING, "!"
      );
      return None;
    else:
      if gbDebug:
        oConsole.fOutput(
          "* FavIcon URL for ", INFO, str(oURL), NORMAL, ": ", INFO, str(oFavIconURL), NORMAL, "."
        );
      return oFavIconURL;
  oConsole.fOutput(WARNING, "- Cannot retrieve ", WARNING_INFO, str(oURL), WARNING, " through any HTTP client.");
  return None;