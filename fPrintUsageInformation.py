from oConsole import oConsole;

from mColors import *;

def fPrintUsageInformation():
  oConsole.fLock();
  try:
    oConsole.fOutput(HILITE, "Usage:");
    oConsole.fOutput("  ", INFO, "FileSystemBrowser", NORMAL, " [", INFO, "\"path to browse\"", NORMAL, "] [", INFO, "OPTIONS", NORMAL, "]");
    oConsole.fOutput();
    oConsole.fOutput(HILITE, "Arguments:");
    oConsole.fOutput("  ", INFO, "\"path to browser\"");
    oConsole.fOutput("      Path to use as the root node (default = current working directory)");
    oConsole.fOutput();
    oConsole.fOutput(HILITE, "Options:");
    oConsole.fOutput("  ", INFO, "--help");
    oConsole.fOutput("    This cruft.");
    oConsole.fOutput("  ", INFO, "--arguments=\"path\"");
    oConsole.fOutput("    Read and process additional arguments from a file.");
    oConsole.fOutput("  ", INFO, "--offline=\"path\"");
    oConsole.fOutput("    Do not start a webserver to allow browsing but instead create files for");
    oConsole.fOutput("    offline browsing or uploading to server.");
    oConsole.fOutput("  ", INFO, "--apply-sharepoint-hacks");
    oConsole.fOutput("    Modify offline files for use on SharePoint server where .json files are not");
    oConsole.fOutput("    allowed.");
    oConsole.fOutput("  ", INFO, "--http-direct");
    oConsole.fOutput("    Make direct requests to look up favicons for website links.");
    oConsole.fOutput("  ", INFO, "--http-proxy=hostname:port");
    oConsole.fOutput("    Use the specified hostname and port as a HTTP proxy to make requests to");
    oConsole.fOutput("    look up favicons for website links.");
    oConsole.fOutput("  ", INFO, "--http-timeout=<seconds>");
    oConsole.fOutput("    Wait for a HTTP response from a server or proxy for at most the given number");
    oConsole.fOutput("    of seconds before failing the request.");
    oConsole.fOutput("  ", INFO, "--debug");
    oConsole.fOutput("    Show debug output");
    oConsole.fOutput("");
    oConsole.fOutput(HILITE, "Notes:");
    oConsole.fOutput("  You can provide the ", INFO, "--http-direct", NORMAL, " and/or ", INFO, "--http-proxy", NORMAL, " arguments to allow");
    oConsole.fOutput("  FileSystemBrowser to request any webpages that are linked to in order to");
    oConsole.fOutput("  determine their 'favicon' icon and use that for the link. Note that this can");
    oConsole.fOutput("  slow down the creation of the tree significantly.");
    oConsole.fOutput("  You can combine the ", INFO, "--http-direct", NORMAL, " and ", INFO, "--http-proxy", NORMAL, " arguments to try both");
    oConsole.fOutput("  direct requests and requests through a proxy when on an intranet. You can");
    oConsole.fOutput("  also specify multiple ", INFO, "--http-proxy", NORMAL, " arguments to have this");
    oConsole.fOutput("  script to try multiple proxies for each webpage untill the webpage can");
    oConsole.fOutput("  successfully be downloaded.");
    oConsole.fOutput("  If you provide the ", INFO, "--http-timeout", NORMAL, " argument, it will affect only");
    oConsole.fOutput("  connections made by the client based on ", INFO, "--http-direct", NORMAL, " and/or ", INFO, "--http-proxy");
    oConsole.fOutput("  arguments that come after it. This allows you to set different timeouts for");
    oConsole.fOutput("  these arguments.");
    oConsole.fOutput("  The order in which you provide the ", INFO, "--http-direct", NORMAL, " and ", INFO, "--http-proxy", NORMAL, " arguments");
    oConsole.fOutput("  determines the order in which request for webpages are attempted directly or");
    oConsole.fOutput("  through proxies.");
  finally:             
    oConsole.fUnlock();