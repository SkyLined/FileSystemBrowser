import os, sys;

from fInitializeProduct import fInitializeProduct;
fInitializeProduct();

try: # mDebugOutput use is Optional
  import mDebugOutput as m0DebugOutput;
except ModuleNotFoundError as oException:
  if oException.args[0] != "No module named 'mDebugOutput'":
    raise;
  m0DebugOutput = None;

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
  from mColors import *;
  
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
          oConsole.fOutput(ERROR, "- Superflous ", ERROR_INFO, s0LowerName, ERROR, " argument:");
          oConsole.fOutput(ERROR, "  ", ERROR_INFO, sOfflineFolderPath);
          oConsole.fOutput(ERROR, "  ", ERROR_INFO, s0Value);
          oConsole.fOutput(ERROR, "  You can only provide this argument once.");
          sys.exit(1);
        if not s0Value:
          oConsole.fOutput(ERROR, "- Invalid ", ERROR_INFO, s0LowerName, ERROR, " argument:");
          oConsole.fOutput(ERROR, "  You must provide a value for this argument.");
          sys.exit(1);
        sOfflineFolderPath = s0Value;
      elif s0LowerName == "http-direct":
        if s0Value:
          oConsole.fOutput(ERROR, "- Invalid ", ERROR_INFO, s0LowerName, ERROR, " argument value:");
          oConsole.fOutput(ERROR, "  ", ERROR_INFO, s0Value);
          oConsole.fOutput(ERROR, "  You cannot provide a value for this argument.");
          sys.exit(1);
        if m0HTTPClient is None:
          oConsole.fOutput(ERROR, "- The optional ", ERROR_INFO, "mHTTPClient", ERROR, " module is not available.");
          oConsole.fOutput(ERROR, "  Please download this module before using the ", ERROR_INFO, s0LowerName, ERROR, " argument.");
          sys.exit(1);
        aoHTTPClients.append(m0HTTPClient.cHTTPClient(nzTransactionTimeoutInSeconds = nzHTTPRequestTimeoutInSeconds));
      elif s0LowerName == "http-proxy":
        if not s0Value:
          oConsole.fOutput(ERROR, "- Invalid ", ERROR_INFO, s0LowerName, ERROR, " argument:");
          oConsole.fOutput(ERROR, "  You must provide a value for this argument.");
          sys.exit(1);
        if m0HTTPClient is None:
          oConsole.fOutput(ERROR, "- The optional ", ERROR_INFO, "mHTTPClient", ERROR, " module is not available.");
          oConsole.fOutput(ERROR, "  Please download this module before using the ", ERROR_INFO, s0LowerName, ERROR, " argument.");
          sys.exit(1);
        tsHostnameAndPortNumber = s0Value.split(":") if s0Value else [];
        sHostname = tsHostnameAndPortNumber[0] if len(tsHostnameAndPortNumber) == 2 else None;
        try:
          u0PortNumber = int(tsHostnameAndPortNumber[1]) if len(tsHostnameAndPortNumber) == 2 else None;
        except:
          u0PortNumber = None;
        if u0PortNumber is None:
          oConsole.fOutput(ERROR, "- Invalid ", ERROR_INFO, s0LowerName, ERROR, " argument:");
          oConsole.fOutput(ERROR, "  ", ERROR_INFO, s0Value);
          oConsole.fOutput(ERROR, "  You must provide a valid 'hostname:port' value for the http proxy.");
          sys.exit(1);
        oProxyServerURL = mHTTPProtocol.cURL("http", sHostname, u0PortNumber);
        aoHTTPClients.append(m0HTTPClient.cHTTPClientUsingProxyServer(oProxyServerURL, nzTransactionTimeoutInSeconds = nzHTTPRequestTimeoutInSeconds));
      elif s0LowerName == "http-timeout":
        if not s0Value:
          oConsole.fOutput(ERROR, "- Invalid ", ERROR_INFO, s0LowerName, ERROR, "argument:");
          oConsole.fOutput(ERROR, "  You must provide a numeric value for this argument.");
          sys.exit(1);
        try:
          nzHTTPRequestTimeoutInSeconds = float(s0Value);
          if nzHTTPRequestTimeoutInSeconds < 0:
            raise ValueError();
        except ValueError:
          oConsole.fOutput(ERROR, "- Invalid ", ERROR_INFO, s0LowerName, ERROR, "argument:");
          oConsole.fOutput(ERROR, "  You must provide a numeric value for this argument.");
          sys.exit(1);
        if nzHTTPRequestTimeoutInSeconds == 0:
          nzHTTPRequestTimeoutInSeconds = None;
      elif s0LowerName:
        oConsole.fOutput(ERROR, "- Unknown argument \"", ERROR_INFO, s0LowerName, ERROR, "\".");
        sys.exit(1);
      else:
        if sArgument[0] == '"' and sArgument[-1] == '"':
          sArgument = sArgument[1:-1]; # remove wrapping quotes from argument
        if sBaseFolderPath is not None:
          oConsole.fOutput(ERROR, "- Superflous path arguments:");
          oConsole.fOutput(ERROR, "  ", ERROR_INFO, sBaseFolderPath);
          oConsole.fOutput(ERROR, "  ", ERROR_INFO, sArgument);
          oConsole.fOutput(ERROR, "  You can only provide this argument once.");
          sys.exit(1);
        else:
          sBaseFolderPath = sArgument;
    
    oRootFolderFileSystemItem = cFileSystemItem(sBaseFolderPath or os.getcwd());
    if not oRootFolderFileSystemItem.fbIsFolder(bThrowErrors = bDebug):
      oConsole.fOutput(ERROR, "- Root folder %s is not a folder" % oRootFolderFileSystemItem.sPath);
      sys.exit(1);
    oRootFileSystemTreeNode = cFileSystemTreeNode(oRootFolderFileSystemItem, bOpened = True);
    
    sTitle = oRootFolderFileSystemItem.sName if sOfflineFolderPath else oRootFolderFileSystemItem.sPath;
    oTreeServer = cTreeServer(sTitle, bOffline = sOfflineFolderPath is not None);
    oTreeServer.fAppendChild(oRootFileSystemTreeNode);
    if sOfflineFolderPath is None:
      oConsole.fOutput("* Server running @ ", INFO, str(oTreeServer.oURL), NORMAL, ".");
    try:
      oConsole.fStatus("* Reading folder tree for ", INFO, oRootFolderFileSystemItem.sPath, NORMAL, "...");
      def fRefreshTreeProgressCallback(oFileSystemTreeNode):
        oConsole.fStatus("* Reading folder tree for ", INFO, oFileSystemTreeNode.oFileSystemItem.sPath, NORMAL, "...");
      oRootFileSystemTreeNode.fRefreshTree(oTreeServer, aoHTTPClients, bThrowErrors = bDebug, fProgressCallback = fRefreshTreeProgressCallback);
      oConsole.fOutput("* Folder tree complete for ", INFO, oRootFolderFileSystemItem.sPath, NORMAL, ".");
      oTreeServer.fMakeStatic();
      if sOfflineFolderPath is not None:
        oOfflineFolder = cFileSystemItem(sOfflineFolderPath);
    #    if oOfflineFolder.fbIsFolder(bThrowErrors = bDebug):
    #      print "* Cleaning offline folder %s..." % oOfflineFolder.sPath;
    #      if not oOfflineFolder.fbDeleteDescendants(bThrowErrors = bDebug):
    #        print "  - Contents of offline folder cannot be deleted.";
    #        sys.exit(1);
    #    elif oOfflineFolder.fbExists(bThrowErrors = bDebug):
    #      print "- Offline folder %s exists but is not a folder!" % oOfflineFolder.sPath;
    #      sys.exit(1);
    #    elif not oOfflineFolder.fbCreateAsFolder(bThrowErrors = bDebug):
    #      print "- Offline folder %s cannot be created." % oOfflineFolder.sPath;
    #      sys.exit(1);
        oConsole.fStatus("* Determining offline files...");
        dxOfflineFileOrData_by_sRelativePath = oTreeServer.fdxGetOfflineContent();
        doExistingOfflineFileOrFolder_by_sRelativePath = {};
        if oOfflineFolder.fbIsFolder(bThrowErrors = bDebug):
          oConsole.fStatus("* Reading existing offline files in ", INFO, oOfflineFolder.sPath, NORMAL, "...");
          for oDescendant in oOfflineFolder.faoGetDescendants(bThrowErrors = bDebug, bParseZipFiles = False):
            sRelativePath = oOfflineFolder.fsGetRelativePathTo(oDescendant.sPath, bThrowErrors = bDebug);
            doExistingOfflineFileOrFolder_by_sRelativePath[sRelativePath] = oDescendant;
          oConsole.fStatus("* Updating offline files in ", INFO, oOfflineFolder.sPath, NORMAL, "...");
        else:
          oConsole.fStatus("* Saving offline files in ", INFO, oOfflineFolder.sPath, NORMAL, "...");
        asExistingAndNewOfflineFileRelativePaths = list(set(
          list(dxOfflineFileOrData_by_sRelativePath.keys())
          + list(doExistingOfflineFileOrFolder_by_sRelativePath.keys())
        ));
        fPrintOrStatus = oConsole.fOutput if bDebug else oConsole.fStatus;
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
                fPrintOrStatus("  ~ Deleting ", INFO, sRelativePath, "\\*", NORMAL, " (folder no longer needed)");
                if not oExistingOfflineFileOrFolder.fbDelete(bThrowErrors = bDebug):
                  oConsole.fOutput(ERROR, "- Cannot delete folder ", ERROR_INFO, oExistingOfflineFileOrFolder.sPath, ERROR, "!");
                  sys.exit(1);
                oExistingOfflineFileOrFolder = None;
              else:
                fPrintOrStatus("  = Keeping ", INFO, sRelativePath, "\\", NORMAL, " (folder exists and is needed)");
            elif sb0Data is None:
              # This file may be part of a folder that was deleted, so it may no longer exist.
              if oExistingOfflineFileOrFolder.fbExists():
                fPrintOrStatus("  ~ Deleting ", INFO, sRelativePath, NORMAL, " (file no longer needed)");
                if not oExistingOfflineFileOrFolder.fbDelete(bThrowErrors = bDebug):
                  oConsole.fOutput(ERROR, "- Cannot delete file ", ERROR_INFO, oExistingOfflineFileOrFolder.sPath, ERROR, "!");
                  sys.exit(1);
            elif oExistingOfflineFileOrFolder.fsbRead(bThrowErrors = bDebug) == sb0Data:
              if bDebug:
                fPrintOrStatus("  = Keeping ", INFO, sRelativePath, NORMAL, " (file was not modified)");
            else:
              fPrintOrStatus("  * Saving ", INFO, sRelativePath, NORMAL, " (file is modified)");
              try:
                oExistingOfflineFileOrFolder.fbWrite(sb0Data, bThrowErrors = True);
              except Exception as oException:
                oConsole.fOutput(
                  ERROR, "- Cannot write ", ERROR_INFO, str(len(sb0Data)), ERROR, " bytes to ",
                  ERROR_INFO, oExistingOfflineFileOrFolder.sPath, ERROR, ":",
                  ERROR_INFO, repr(oException), ERROR, "!",
                );
                sys.exit(1);
          else:
            assert sb0Data is not None, \
                "File or folder %s does not exist but there is also no data for it!?" % sRelativePath;
            oOfflineFile = oOfflineFolder.foGetDescendant(sRelativePath, bThrowErrors = bDebug);
            fPrintOrStatus("  + Saving ", INFO, sRelativePath, NORMAL, " (new file)");
            try:
              oOfflineFile.fbCreateAsFile(sb0Data, bCreateParents = True, bParseZipFiles = False, bThrowErrors = True);
            except Exception as oException:
              oConsole.fOutput(
                ERROR, "- Cannot write ", ERROR_INFO, str(len(sb0Data)), ERROR, " bytes to ",
                ERROR_INFO, oOfflineFile.sPath, ERROR, ":",
                ERROR_INFO, repr(oException), ERROR, "!",
              );
              sys.exit(1);
      else:
        oConsole.fStatus("* Waiting for server to terminate...");
        oTreeServer.fWait();
        oConsole.fOutput("* Server terminated.");
    except:
      if sOfflineFolderPath is None:
        oTreeServer.fTerminate();
      raise;
    oConsole.fOutput("* Done.");
except Exception as oException:
  if m0DebugOutput:
    m0DebugOutput.fTerminateWithException(oException);
  raise;