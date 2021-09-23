from mConsole import oConsole;

from mColorsAndChars import *;

def fOutputUsageInformation():
  oConsole.fLock();
  try:
    oConsole.fOutput(COLOR_HILITE, "Usage:");
    oConsole.fOutput("  ", COLOR_INFO, "FileSystemBrowser", COLOR_NORMAL, " [", COLOR_INFO, "\"path to browse\"", COLOR_NORMAL, "] [", COLOR_INFO, "OPTIONS", COLOR_NORMAL, "]");
    oConsole.fOutput();
    oConsole.fOutput(COLOR_HILITE, "Arguments:");
    oConsole.fOutput("  ", COLOR_INFO, "\"path to browser\"");
    oConsole.fOutput("      Path to use as the root node (default = current working directory)");
    oConsole.fOutput();
    oConsole.fOutput(COLOR_HILITE, "Options:");
    oConsole.fOutput("  ", COLOR_INFO, "-h", COLOR_NORMAL, ", ", COLOR_INFO, "--help");
    oConsole.fOutput("    This cruft.");
    oConsole.fOutput("  ", COLOR_INFO, "--version");
    oConsole.fOutput("    Show version information.");
    oConsole.fOutput("  ", COLOR_INFO, "--version-check");
    oConsole.fOutput("    Check for updates and show version information.");
    oConsole.fOutput("  ", COLOR_INFO, "--license");
    oConsole.fOutput("    Show license information.");
    oConsole.fOutput("  ", COLOR_INFO, "--license-update");
    oConsole.fOutput("    Download license updates and show license information.");
    oConsole.fOutput("  ", COLOR_INFO, "--arguments", COLOR_NORMAL, "=<", COLOR_INFO, "file path", COLOR_NORMAL, ">");
    oConsole.fOutput("    Load additional arguments from the provided value and insert them in place");
    oConsole.fOutput("    of this argument.");
    
    oConsole.fOutput("  ", COLOR_INFO, "--debug");
    oConsole.fOutput("    Show debug output.");
    oConsole.fOutput("  ", COLOR_INFO, "--offline=\"path\"");
    oConsole.fOutput("    Do not start a webserver to allow browsing but instead create files for");
    oConsole.fOutput("    offline browsing or uploading to server.");
    oConsole.fOutput("  ", COLOR_INFO, "--http-direct");
    oConsole.fOutput("    Make direct requests to look up favicons for website links.");
    oConsole.fOutput("  ", COLOR_INFO, "--http-proxy=hostname:port");
    oConsole.fOutput("    Use the specified hostname and port as a HTTP proxy to make requests to");
    oConsole.fOutput("    look up favicons for website links.");
    oConsole.fOutput("  ", COLOR_INFO, "--http-timeout=<seconds>");
    oConsole.fOutput("    Wait for a HTTP response from a server or proxy for at most the given number");
    oConsole.fOutput("    of seconds before failing the request.");
    oConsole.fOutput("  ", COLOR_INFO, "--arguments=\"path\"");
    oConsole.fOutput("    Read and insert additional arguments from a file.");
    oConsole.fOutput("");
    oConsole.fOutput(COLOR_HILITE, "Notes:");
    oConsole.fOutput("  You can provide the ", COLOR_INFO, "--http-direct", COLOR_NORMAL, " and/or ", COLOR_INFO, "--http-proxy", COLOR_NORMAL, " arguments to allow");
    oConsole.fOutput("  FileSystemBrowser to request any webpages that are linked to in order to");
    oConsole.fOutput("  determine their 'favicon' icon and use that for the link. Note that this can");
    oConsole.fOutput("  slow down the creation of the tree significantly.");
    oConsole.fOutput("  You can combine the ", COLOR_INFO, "--http-direct", COLOR_NORMAL, " and ", COLOR_INFO, "--http-proxy", COLOR_NORMAL, " arguments to try both");
    oConsole.fOutput("  direct requests and requests through a proxy when on an intranet. You can");
    oConsole.fOutput("  also specify multiple ", COLOR_INFO, "--http-proxy", COLOR_NORMAL, " arguments to have this");
    oConsole.fOutput("  script to try multiple proxies for each webpage untill the webpage can");
    oConsole.fOutput("  successfully be downloaded.");
    oConsole.fOutput("  If you provide the ", COLOR_INFO, "--http-timeout", COLOR_NORMAL, " argument, it will affect only");
    oConsole.fOutput("  connections made by the client based on ", COLOR_INFO, "--http-direct", COLOR_NORMAL, " and/or ", COLOR_INFO, "--http-proxy");
    oConsole.fOutput("  arguments that come after it. This allows you to set different timeouts for");
    oConsole.fOutput("  these arguments.");
    oConsole.fOutput("  The order in which you provide the ", COLOR_INFO, "--http-direct", COLOR_NORMAL, " and ", COLOR_INFO, "--http-proxy", COLOR_NORMAL, " arguments");
    oConsole.fOutput("  determines the order in which request for webpages are attempted directly or");
    oConsole.fOutput("  through proxies.");
  finally:             
    oConsole.fUnlock();