import os, sys;

sModulePath = os.path.dirname(__file__);
sys.path = [sModulePath] + [sPath for sPath in sys.path if sPath.lower() != sModulePath.lower()];
from fInitializeProduct import fInitializeProduct;
fInitializeProduct();

try: # mDebugOutput use is Optional
  import mDebugOutput as m0DebugOutput;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mDebugOutput'":
    raise;
  m0DebugOutput = None;

guExitCodeInternalError = 1; # Just in case mExitCodes is not loaded, as we need this later.
try:
  try: # mHTTPClient use is Optional
    import mHTTPClient as m0HTTPClient;
  except ModuleNotFoundError as oException:
    if oException.args[0] != "No module named 'mHTTPClient'":
      raise;
    m0HTTPClient = None;
  from cFileSystemTreeNode import cFileSystemTreeNode;
  from mTreeServer import cTreeServer;
  from mFileSystemItem import cFileSystemItem;
  from mNotProvided import *;
  from mConsole import oConsole;
  
  from fatsArgumentLowerNameAndValue import fatsArgumentLowerNameAndValue;
  from mColorsAndChars import *;
  from mExitCodes import *;
  
  if __name__ == "__main__":
    bDebug = False;
    aoHTTPClients = [];
    sBaseFolderPath = None;
    sOfflineFolderPath = None;
    nzHTTPRequestTimeoutInSeconds = None;
    for (sArgument, s0LowerName, s0Value) in fatsArgumentLowerNameAndValue():
      if s0LowerName == "debug":
        bDebug = True;
        if m0DebugOutput: m0DebugOutput.fEnableAllDebugOutput();
      elif s0LowerName == "offline":
        if sOfflineFolderPath is not None:
          oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Superflous ", COLOR_INFO, s0LowerName, COLOR_NORMAL, " argument:");
          oConsole.fOutput("  ", COLOR_INFO, sOfflineFolderPath);
          oConsole.fOutput("  ", COLOR_INFO, s0Value);
          oConsole.fOutput("  You can only provide this argument once.");
          sys.exit(guExitCodeBadArgument);
        if not s0Value:
          oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Invalid ", COLOR_INFO, s0LowerName, COLOR_NORMAL, " argument:");
          oConsole.fOutput("  You must provide a value for this argument.");
          sys.exit(guExitCodeBadArgument);
        sOfflineFolderPath = s0Value;
      elif s0LowerName == "http-direct":
        if s0Value:
          oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Invalid ", COLOR_INFO, s0LowerName, COLOR_NORMAL, " argument value:");
          oConsole.fOutput("  ", COLOR_INFO, s0Value);
          oConsole.fOutput("  You cannot provide a value for this argument.");
          sys.exit(guExitCodeBadArgument);
        if m0HTTPClient is None:
          oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " The optional ", COLOR_INFO, "mHTTPClient", COLOR_NORMAL, " module is not available.");
          oConsole.fOutput("  Please download this module before using the ", COLOR_INFO, s0LowerName, COLOR_NORMAL, " argument.");
          sys.exit(guExitCodeBadArgument);
        aoHTTPClients.append(m0HTTPClient.cHTTPClient(nzTransactionTimeoutInSeconds = nzHTTPRequestTimeoutInSeconds));
      elif s0LowerName == "http-proxy":
        if not s0Value:
          oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Invalid ", COLOR_INFO, s0LowerName, COLOR_NORMAL, " argument:");
          oConsole.fOutput("  You must provide a value for this argument.");
          sys.exit(guExitCodeBadArgument);
        if m0HTTPClient is None:
          oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " The optional ", COLOR_INFO, "mHTTPClient", COLOR_NORMAL, " module is not available.");
          oConsole.fOutput("  Please download this module before using the ", COLOR_INFO, s0LowerName, COLOR_NORMAL, " argument.");
          sys.exit(guExitCodeBadArgument);
        tsHostnameAndPortNumber = s0Value.split(":") if s0Value else [];
        sHostname = tsHostnameAndPortNumber[0] if len(tsHostnameAndPortNumber) == 2 else None;
        try:
          u0PortNumber = int(tsHostnameAndPortNumber[1]) if len(tsHostnameAndPortNumber) == 2 else None;
        except:
          u0PortNumber = None;
        if u0PortNumber is None:
          oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Invalid ", COLOR_INFO, s0LowerName, COLOR_NORMAL, " argument:");
          oConsole.fOutput("  ", COLOR_INFO, s0Value);
          oConsole.fOutput("  You must provide a valid 'hostname:port' value for the http proxy.");
          sys.exit(guExitCodeBadArgument);
        oProxyServerURL = mHTTPProtocol.cURL("http", sHostname, u0PortNumber);
        aoHTTPClients.append(m0HTTPClient.cHTTPClientUsingProxyServer(oProxyServerURL, nzTransactionTimeoutInSeconds = nzHTTPRequestTimeoutInSeconds));
      elif s0LowerName == "http-timeout":
        if not s0Value:
          oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Invalid ", COLOR_INFO, s0LowerName, COLOR_NORMAL, "argument:");
          oConsole.fOutput("  You must provide a numeric value for this argument.");
          sys.exit(guExitCodeBadArgument);
        try:
          nzHTTPRequestTimeoutInSeconds = float(s0Value);
          if nzHTTPRequestTimeoutInSeconds < 0:
            raise ValueError();
        except ValueError:
          oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Invalid ", COLOR_INFO, s0LowerName, COLOR_NORMAL, "argument:");
          oConsole.fOutput("  You must provide a numeric value for this argument.");
          sys.exit(guExitCodeBadArgument);
        if nzHTTPRequestTimeoutInSeconds == 0:
          nzHTTPRequestTimeoutInSeconds = None;
      elif s0LowerName:
        oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Unknown argument \"", COLOR_INFO, s0LowerName, COLOR_NORMAL, "\".");
        sys.exit(guExitCodeBadArgument);
      else:
        if sArgument[0] == '"' and sArgument[-1] == '"':
          sArgument = sArgument[1:-1]; # remove wrapping quotes from argument
        if sBaseFolderPath is not None:
          oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Superflous path arguments:");
          oConsole.fOutput("  ", COLOR_INFO, sBaseFolderPath);
          oConsole.fOutput("  ", COLOR_INFO, sArgument);
          oConsole.fOutput("  You can only provide this argument once.");
          sys.exit(guExitCodeBadArgument);
        else:
          sBaseFolderPath = sArgument;
    
    oRootFolderFileSystemItem = cFileSystemItem(sBaseFolderPath or os.getcwd());
    if not oRootFolderFileSystemItem.fbIsFolder(bThrowErrors = bDebug):
      oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Root folder ", COLOR_INFO, oRootFolderFileSystemItem.sPath, COLOR_NORMAL, " is not a folder");
      sys.exit(guExitCodeBadArgument);
    oRootFileSystemTreeNode = cFileSystemTreeNode(oRootFolderFileSystemItem, bOpened = True);
    
    sTitle = oRootFolderFileSystemItem.sName if sOfflineFolderPath else oRootFolderFileSystemItem.sPath;
    oTreeServer = cTreeServer(sTitle, bOffline = sOfflineFolderPath is not None);
    oTreeServer.fAppendChild(oRootFileSystemTreeNode);
    if sOfflineFolderPath is None:
      oConsole.fOutput(COLOR_OK, CHAR_OK, COLOR_NORMAL, " Server running @ ", COLOR_INFO, str(oTreeServer.oURL), COLOR_NORMAL, ".");
    try:
      oConsole.fStatus(COLOR_BUSY, CHAR_BUSY, COLOR_NORMAL, " Reading folder tree for ", COLOR_INFO, oRootFolderFileSystemItem.sPath, COLOR_NORMAL, "...");
      def fRefreshTreeProgressCallback(oFileSystemTreeNode):
        oConsole.fStatus(COLOR_BUSY, CHAR_BUSY, COLOR_NORMAL, " Reading folder tree for ", COLOR_INFO, oFileSystemTreeNode.oFileSystemItem.sPath, COLOR_NORMAL, "...");
      oRootFileSystemTreeNode.fRefreshTree(oTreeServer, aoHTTPClients, bThrowErrors = bDebug, fProgressCallback = fRefreshTreeProgressCallback);
      oConsole.fOutput(COLOR_OK, CHAR_OK, COLOR_NORMAL, " Folder tree complete for ", COLOR_INFO, oRootFolderFileSystemItem.sPath, COLOR_NORMAL, ".");
      oTreeServer.fMakeStatic();
      if sOfflineFolderPath is not None:
        oOfflineFolder = cFileSystemItem(sOfflineFolderPath);
    #    if oOfflineFolder.fbIsFolder(bThrowErrors = bDebug):
    #      print "* Cleaning offline folder %s..." % oOfflineFolder.sPath;
    #      if not oOfflineFolder.fbDeleteDescendants(bThrowErrors = bDebug):
    #        print "  - Contents of offline folder cannot be deleted.";
    #        sys.exit(guExitCodeCannotWriteToFileSystem);
    #    elif oOfflineFolder.fbExists(bThrowErrors = bDebug):
    #      print "- Offline folder %s exists but is not a folder!" % oOfflineFolder.sPath;
    #      sys.exit(guExitCodeBadArgument);
    #    elif not oOfflineFolder.fbCreateAsFolder(bThrowErrors = bDebug):
    #      print "- Offline folder %s cannot be created." % oOfflineFolder.sPath;
    #      sys.exit(guExitCodeCannotWriteToFileSystem);
        oConsole.fStatus(COLOR_BUSY, CHAR_BUSY, COLOR_NORMAL, " Determining offline files...");
        dxOfflineFileOrData_by_sRelativePath = oTreeServer.fdxGetOfflineContent();
        doExistingOfflineFileOrFolder_by_sRelativePath = {};
        if oOfflineFolder.fbIsFolder(bThrowErrors = bDebug):
          oConsole.fStatus(COLOR_BUSY, CHAR_BUSY, COLOR_NORMAL, " Reading existing offline files in ", COLOR_INFO, oOfflineFolder.sPath, COLOR_NORMAL, "...");
          for oDescendant in oOfflineFolder.faoGetDescendants(bThrowErrors = bDebug, bParseZipFiles = False):
            sRelativePath = oOfflineFolder.fsGetRelativePathTo(oDescendant.sPath, bThrowErrors = bDebug);
            doExistingOfflineFileOrFolder_by_sRelativePath[sRelativePath] = oDescendant;
          oConsole.fStatus(COLOR_BUSY, CHAR_BUSY, COLOR_NORMAL, " Updating offline files in ", COLOR_INFO, oOfflineFolder.sPath, COLOR_NORMAL, "...");
        else:
          oConsole.fStatus(COLOR_BUSY, CHAR_BUSY, COLOR_NORMAL, " Saving offline files in ", COLOR_INFO, oOfflineFolder.sPath, COLOR_NORMAL, "...");
        asExistingAndNewOfflineFileRelativePaths = list(set(
          list(dxOfflineFileOrData_by_sRelativePath.keys())
          + list(doExistingOfflineFileOrFolder_by_sRelativePath.keys())
        ));
        fConsoleOutputOrStatus = oConsole.fOutput if bDebug else oConsole.fStatus;
        for sRelativePath in sorted(asExistingAndNewOfflineFileRelativePaths, key=lambda sString: sString.lower()):
          xOfflineFileOrData = dxOfflineFileOrData_by_sRelativePath.get(sRelativePath);
          fAssertType("xOfflineFileOrData for sRelativePath %s" % repr(sRelativePath), xOfflineFileOrData, cFileSystemItem, str);
          if isinstance(xOfflineFileOrData, cFileSystemItem):
            sb0Data = xOfflineFileOrData.fsbRead(bThrowErrors = bDebug);
          else:
            sb0Data = bytes(ord(sByte) for sByte in xOfflineFileOrData);
          oExistingOfflineFileOrFolder = doExistingOfflineFileOrFolder_by_sRelativePath.get(sRelativePath);
          if oExistingOfflineFileOrFolder:
            if oExistingOfflineFileOrFolder.fbIsFolder(bThrowErrors = bDebug):
              if sb0Data is not None:
                # There is currently a folder with this name but we want a file: delete the folder.
                bDelete = True;
              else:
                # There is currently a folder with this name, so find out if we need to keep it:
                for sWantedFileRelativePath in dxOfflineFileOrData_by_sRelativePath:
                  if sWantedFileRelativePath.startswith(sRelativePath + os.sep):
                    # We want a file in this folder or a sub-folder: keep it.
                    bDelete = False;
                    break;
                else:
                  bDelete = True;
              if bDelete:
                fConsoleOutputOrStatus("  ", COLOR_REMOVE, CHAR_REMOVE, COLOR_NORMAL, " Deleting ", COLOR_INFO, sRelativePath, "\\*", COLOR_NORMAL, " (folder no longer needed)");
                if not oExistingOfflineFileOrFolder.fbDelete(bThrowErrors = bDebug):
                  oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Cannot delete folder ", COLOR_INFO, oExistingOfflineFileOrFolder.sPath, COLOR_NORMAL, "!");
                  sys.exit(guExitCodeCannotWriteToFileSystem);
                oExistingOfflineFileOrFolder = None;
              else:
                fConsoleOutputOrStatus("  ", CHAR_LIST, " Keeping ", COLOR_INFO, sRelativePath, "\\", COLOR_NORMAL, " (folder exists and is needed)");
            elif sb0Data is None:
              # This file may be part of a folder that was deleted, so it may no longer exist.
              if oExistingOfflineFileOrFolder.fbExists():
                fConsoleOutputOrStatus("  ", COLOR_REMOVE, CHAR_REMOVE, COLOR_NORMAL, " Deleting ", COLOR_INFO, sRelativePath, COLOR_NORMAL, " (file no longer needed)");
                if not oExistingOfflineFileOrFolder.fbDelete(bThrowErrors = bDebug):
                  oConsole.fOutput(COLOR_ERROR, CHAR_ERROR, COLOR_NORMAL, " Cannot delete file ", COLOR_INFO, oExistingOfflineFileOrFolder.sPath, COLOR_NORMAL, "!");
                  sys.exit(guExitCodeCannotWriteToFileSystem);
            elif oExistingOfflineFileOrFolder.fsbRead(bThrowErrors = bDebug) == sb0Data:
              if bDebug:
                fConsoleOutputOrStatus("  ", CHAR_LIST, " Keeping ", COLOR_INFO, sRelativePath, COLOR_NORMAL, " (file was not modified)");
            else:
              fConsoleOutputOrStatus("  ", COLOR_MODIFY, CHAR_MODIFY, COLOR_NORMAL, " Saving ", COLOR_INFO, sRelativePath, COLOR_NORMAL, " (file is modified)");
              try:
                oExistingOfflineFileOrFolder.fbWrite(sb0Data, bThrowErrors = True);
              except Exception as oException:
                oConsole.fOutput(
                  COLOR_ERROR, CHAR_ERROR,
                  COLOR_NORMAL, " Cannot write ",
                  COLOR_INFO, str(len(sb0Data)),
                  COLOR_NORMAL, " bytes to ",
                  COLOR_INFO, oExistingOfflineFileOrFolder.sPath,
                  COLOR_NORMAL, ":",
                  COLOR_INFO, str(oException),
                  COLOR_NORMAL, "!",
                );
                sys.exit(guExitCodeCannotWriteToFileSystem);
          else:
            assert sb0Data is not None, \
                "File or folder %s does not exist but there is also no data for it!?" % sRelativePath;
            oOfflineFile = oOfflineFolder.foGetDescendant(sRelativePath, bThrowErrors = bDebug);
            fConsoleOutputOrStatus("  ", COLOR_ADD, CHAR_ADD, COLOR_NORMAL, " Saving ", COLOR_INFO, sRelativePath, COLOR_NORMAL, " (new file)");
            try:
              oOfflineFile.fbCreateAsFile(sb0Data, bCreateParents = True, bParseZipFiles = False, bThrowErrors = True);
            except Exception as oException:
              oConsole.fOutput(
                COLOR_ERROR, CHAR_ERROR,
                COLOR_NORMAL, " Cannot write ",
                COLOR_INFO, str(len(sb0Data)),
                COLOR_NORMAL, " bytes to ",
                COLOR_INFO, oOfflineFile.sPath,
                COLOR_NORMAL, ":",
                COLOR_INFO, repr(oException),
                COLOR_NORMAL, "!",
              );
              sys.exit(guExitCodeCannotWriteToFileSystem);
      else:
        oConsole.fStatus(COLOR_BUSY, CHAR_BUSY, COLOR_NORMAL, " Waiting for server to terminate...");
        oTreeServer.fWait();
        oConsole.fOutput(COLOR_BUSY, CHAR_BUSY, COLOR_NORMAL, " Server terminated.");
    except:
      if sOfflineFolderPath is None:
        oTreeServer.fTerminate();
      raise;
    oConsole.fOutput(COLOR_OK, CHAR_OK, COLOR_NORMAL, " Done.");
    sys.exit(guExitCodeSuccess);
except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException, guExitCodeInternalError);
  raise;