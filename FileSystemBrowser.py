import os, sys;

from fInitializeProduct import fInitializeProduct;
fInitializeProduct();

try: # mDebugOutput use is Optional
  from mDebugOutput import *;
except: # Do nothing if not available.
  mDebugOutput = None;

try:
  from cFileSystemTreeNode import cFileSystemTreeNode;
  from cTreeServer import cTreeServer;
  from cFileSystemItem import cFileSystemItem;
  from oConsole import oConsole;
  import mHTTP;
  
  from fPrintUsageInformation import fPrintUsageInformation;
  from fPrintVersionInformation import fPrintVersionInformation;
  from mColors import *;
  
  if __name__ == "__main__":
    bDebug = False;
    aoHTTPClients = [];
    sBaseFolderPath = None;
    sOfflineFolderPath = None;
    bApplySharePointHacks = False;
    nzHTTPRequestTimeoutInSeconds = None;
    asArguments = sys.argv[1:];
    uArgumentIndex = 0;
    while uArgumentIndex < len(asArguments):
      sArgument = asArguments[uArgumentIndex];
      if sArgument in ["/h", "/?", "-h", "-?", "/help"]:
        fPrintUsageInformation();
        sys.exit(0);
      elif sArgument in ["-v", "--version", "/version"]:
        fPrintVersionInformation(
          bCheckForUpdates = True,
          bCheckAndShowLicenses = True,
          bShowInstallationFolders = True,
        );
        sys.exit(0);
      sSwitchName = sArgument[2:].lower().split("=")[0] if sArgument.startswith("--") else None;
      if sSwitchName is None:
        if sArgument[0] == '"' and sArgument[-1] == '"':
          sArgument = sArgument[1:-1]; # remove wrapping quotes from argument
        if sBaseFolderPath is not None:
          oConsole.fPrint(ERROR, "- Superflous path arguments:");
          oConsole.fPrint(ERROR, "  ", ERROR_INFO, sBaseFolderPath);
          oConsole.fPrint(ERROR, "  ", ERROR_INFO, sSwitchValue);
          oConsole.fPrint(ERROR, "  You can only provide this argument once.");
          sys.exit(1);
        else:
          sBaseFolderPath = sArgument;
      else:
        sSwitchValue = sArgument[len(sSwitchName) + 3:] if len(sArgument) > len(sSwitchName) + 3 else None;
        if sSwitchValue and sSwitchValue[0] == '"' and sSwitchValue[-1] == '"':
          sSwitchValue = sSwitchValue[1:-1]; # remove wrapping quotes from named argument value
        if sSwitchName == "debug":
          bDebug = True;
          if mDebugOutput: mDebugOutput.fEnableAllDebugOutput();
        elif sSwitchName == "help":
          fPrintUsageInformation();
          sys.exit(0);
        elif sSwitchName == "arguments":
          if not sSwitchValue:
            oConsole.fPrint(ERROR, "- Invalid ", ERROR_INFO, "--", sSwitchName, ERROR, "argument:");
            oConsole.fPrint(ERROR, "  You must provide a value for this argument.");
            sys.exit(1);
          # Read additional arguments from file and insert them after the current argument.
          oArgumentsFile = cFileSystemItem(sSwitchValue);
          if not oArgumentsFile.fbIsFile():
            oConsole.fPrint(ERROR, "- Invalid ", ERROR_INFO, "--", sSwitchName, ERROR, " argument:");
            oConsole.fPrint(ERROR, "  ", ERROR_INFO, oArgumentsFile.sPath);
            oConsole.fPrint(ERROR, "  File not found.");
            sys.exit(1);
          sArgumentsFileContent = oArgumentsFile.fsRead();
          asArguments = asArguments[:uArgumentIndex + 1] + [
            os.path.expandvars(sStrippedArgumentFileLine) for sStrippedArgumentFileLine in [
              sArgumentFileLine.strip() for sArgumentFileLine in sArgumentsFileContent.split("\n")
            ] if sStrippedArgumentFileLine != ""
          ] + asArguments[uArgumentIndex + 1:];
        elif sSwitchName == "offline":
          if sOfflineFolderPath is not None:
            oConsole.fPrint(ERROR, "- Superflous ", ERROR_INFO, "--", sSwitchName, ERROR, " arguments:");
            oConsole.fPrint(ERROR, "  ", ERROR_INFO, sOfflineFolderPath);
            oConsole.fPrint(ERROR, "  ", ERROR_INFO, sSwitchValue);
            oConsole.fPrint(ERROR, "  You can only provide this argument once.");
            sys.exit(1);
          if not sSwitchValue:
            oConsole.fPrint(ERROR, "- Invalid ", ERROR_INFO, "--", sSwitchName, ERROR, "argument:");
            oConsole.fPrint(ERROR, "  You must provide a value for this argument.");
            sys.exit(1);
          sOfflineFolderPath = sSwitchValue;
        elif sSwitchName == "apply-sharepoint-hacks":
          if sSwitchValue:
            oConsole.fPrint(ERROR, "- Invalid ", ERROR_INFO, "--", sSwitchName, ERROR, " argument value:");
            oConsole.fPrint(ERROR, "  ", ERROR_INFO, sSwitchValue);
            oConsole.fPrint(ERROR, "  You cannot provide a value for this argument.");
            sys.exit(1);
          bApplySharePointHacks = True;
        elif sSwitchName == "http-direct":
          if sSwitchValue:
            oConsole.fPrint(ERROR, "- Invalid ", ERROR_INFO, "--", sSwitchName, ERROR, " argument value:");
            oConsole.fPrint(ERROR, "  ", ERROR_INFO, sSwitchValue);
            oConsole.fPrint(ERROR, "  You cannot provide a value for this argument.");
            sys.exit(1);
          aoHTTPClients.append(mHTTP.cHTTPClient(nzTransactionTimeoutInSeconds = nzHTTPRequestTimeoutInSeconds));
        elif sSwitchName == "http-proxy":
          if not sSwitchValue:
            oConsole.fPrint(ERROR, "- Invalid ", ERROR_INFO, "--", sSwitchName, ERROR, " argument:");
            oConsole.fPrint(ERROR, "  You must provide a value for this argument.");
            sys.exit(1);
          tsHostnameAndPort = sSwitchValue.split(":") if sSwitchValue else [];
          sHostname = tsHostnameAndPort[0] if len(tsHostnameAndPort) == 2 else None;
          try:
            uPort = int(tsHostnameAndPort[1]) if len(tsHostnameAndPort) == 2 else 0;
          except:
            uPort = 0;
          if uPort <= 0:
            oConsole.fPrint(ERROR, "- Invalid ", ERROR_INFO, "--", sSwitchName, ERROR, " argument:");
            oConsole.fPrint(ERROR, "  ", ERROR_INFO, sSwitchValue);
            oConsole.fPrint(ERROR, "  You must provide a valid 'hostname:port' value for the http proxy.");
            sys.exit(1);
          oProxyServerURL = mHTTP.cURL("http", sHostname, uPort);
          aoHTTPClients.append(mHTTP.cHTTPClientUsingProxyServer(oProxyServerURL, nzTransactionTimeoutInSeconds = nzHTTPRequestTimeoutInSeconds));
        elif sSwitchName == "http-timeout":
          if not sSwitchValue:
            oConsole.fPrint(ERROR, "- Invalid ", ERROR_INFO, "--", sSwitchName, ERROR, "argument:");
            oConsole.fPrint(ERROR, "  You must provide a numeric value for this argument.");
            sys.exit(1);
          try:
            nzHTTPRequestTimeoutInSeconds = float(sSwitchValue);
            if nzHTTPRequestTimeoutInSeconds < 0:
              raise ValueError();
          except ValueError:
            oConsole.fPrint(ERROR, "- Invalid ", ERROR_INFO, "--", sSwitchName, ERROR, "argument:");
            oConsole.fPrint(ERROR, "  You must provide a numeric value for this argument.");
            sys.exit(1);
          if nzHTTPRequestTimeoutInSeconds == 0:
            nzHTTPRequestTimeoutInSeconds = None;
        else:
          oConsole.fPrint(ERROR, "- Unknown ", ERROR_INFO, "--", sSwitchName, ERROR, " argument.");
          sys.exit(1);
      uArgumentIndex += 1;

    oRootFolderFileSystemItem = cFileSystemItem(sBaseFolderPath or os.getcwd());
    if not oRootFolderFileSystemItem.fbIsFolder(bThrowErrors = bDebug):
      oConsole.fPrint(ERROR, "- Root folder %s is not a folder" % oRootFolderFileSystemItem.sPath);
      sys.exit(1);
    oRootFileSystemTreeNode = cFileSystemTreeNode(oRootFolderFileSystemItem, bOpened = True);

    sTitle = oRootFolderFileSystemItem.sName if sOfflineFolderPath else oRootFolderFileSystemItem.sPath;
    oTreeServer = cTreeServer(sTitle, bOffline = sOfflineFolderPath is not None);
    oTreeServer.fAppendChild(oRootFileSystemTreeNode);
    if sOfflineFolderPath is None:
      oConsole.fPrint("* Server running @ ", INFO, str(oTreeServer.oURL), NORMAL, ".");
    try:
      oConsole.fStatus("* Reading folder tree for ", INFO, oRootFolderFileSystemItem.sPath, NORMAL, "...");
      def fRefreshTreeProgressCallback(oFileSystemTreeNode):
        oConsole.fStatus("* Reading folder tree for ", INFO, oFileSystemTreeNode.oFileSystemItem.sPath, NORMAL, "...");
      oRootFileSystemTreeNode.fRefreshTree(oTreeServer, aoHTTPClients, bThrowErrors = bDebug, fProgressCallback = fRefreshTreeProgressCallback);
      oConsole.fPrint("* Folder tree complete for ", INFO, oRootFolderFileSystemItem.sPath, NORMAL, ".");
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
        if bApplySharePointHacks:
          oConsole.fStatus("* Applying SharePoint hacks to offline files...");
          # rename dxTreeData.json because SharePoint does not allow files with .json extension.
          dxOfflineFileOrData_by_sRelativePath["dxTreeData_json"] = \
              dxOfflineFileOrData_by_sRelativePath["dxTreeData.json"];
          del dxOfflineFileOrData_by_sRelativePath["dxTreeData.json"];
          # Read index.html and update to refer to renamed dxTreeData.json.
          sIndexHTMLData = dxOfflineFileOrData_by_sRelativePath["index.html"].fsRead();
          dxOfflineFileOrData_by_sRelativePath["index.html"] = \
              sIndexHTMLData.replace("dxTreeData.json", "dxTreeData_json");
          asRelativePathsWithIllegalFileExtensions = [];
          asRelativePathsWithIllegalFileNameCharacters = [];
          for sRelativePath in dxOfflineFileOrData_by_sRelativePath:
            if "&" in sRelativePath or "#" in sRelativePath:
              asRelativePathsWithIllegalFileNameCharacters.append(sRelativePath);
            if sRelativePath.lower().split(".")[-1] in ("exe",):
              asRelativePathsWithIllegalFileExtensions.append(sRelativePath);
          if asRelativePathsWithIllegalFileExtensions:
            oConsole.fOutput(ERROR, "  - The following files have extensions that are not allowed:");
            for sRelativePath in asRelativePathsWithIllegalFileExtensions:
              oConsole.fOutput(ERROR, "    - ", ERROR_INFO, sRelativePath);
          if asRelativePathsWithIllegalFileNameCharacters:
            oConsole.fOutput(ERROR, "  - The following file names have characters that are not allowed ('#' '&'):");
            for sRelativePath in asRelativePathsWithIllegalFileNameCharacters:
              oConsole.fOutput(ERROR, "    - ", ERROR_INFO, sRelativePath);
          if asRelativePathsWithIllegalFileExtensions or asRelativePathsWithIllegalFileExtensions:
            oConsole.fOutput(ERROR, "    Please remove these files or store them inside a .zip file before trying again.");
            sys.exit(1);
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
          dxOfflineFileOrData_by_sRelativePath.keys()
          + doExistingOfflineFileOrFolder_by_sRelativePath.keys()
        ));
        fPrintOrStatus = oConsole.fPrint if bDebug else oConsole.fStatus;
        for sRelativePath in sorted(asExistingAndNewOfflineFileRelativePaths, key=lambda sString: sString.lower()):
          xOfflineFileOrData = dxOfflineFileOrData_by_sRelativePath.get(sRelativePath);
          szData = xOfflineFileOrData.fsRead(bThrowErrors = bDebug) if isinstance(xOfflineFileOrData, cFileSystemItem) \
              else xOfflineFileOrData;
          oExistingOfflineFileOrFolder = doExistingOfflineFileOrFolder_by_sRelativePath.get(sRelativePath);
          if oExistingOfflineFileOrFolder:
            if oExistingOfflineFileOrFolder.fbIsFolder(bThrowErrors = bDebug):
              if szData is not None:
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
                  oConsole.fPrint(ERROR, "- Cannot delete folder ", ERROR_INFO, oExistingOfflineFileOrFolder.sPath, ERROR, "!");
                  sys.exit(1);
                oExistingOfflineFileOrFolder = None;
              else:
                fPrintOrStatus("  = Keeping ", INFO, sRelativePath, "\\", NORMAL, " (folder exists and is needed)");
            elif szData is None:
              # This file may be part of a folder that was deleted, so it may no longer exist.
              if oExistingOfflineFileOrFolder.fbExists():
                fPrintOrStatus("  ~ Deleting ", INFO, sRelativePath, NORMAL, " (file no longer needed)");
                if not oExistingOfflineFileOrFolder.fbDelete(bThrowErrors = bDebug):
                  oConsole.fPrint(ERROR, "- Cannot delete file ", ERROR_INFO, oExistingOfflineFileOrFolder.sPath, ERROR, "!");
                  sys.exit(1);
            elif oExistingOfflineFileOrFolder.fsRead(bThrowErrors = bDebug) == szData:
              if bDebug:
                fPrintOrStatus("  = Keeping ", INFO, sRelativePath, NORMAL, " (file was not modified)");
            else:
              fPrintOrStatus("  * Saving ", INFO, sRelativePath, NORMAL, " (file is modified)");
              if not oExistingOfflineFileOrFolder.fbWrite(szData, bThrowErrors = bDebug):
                oConsole.fPrint(ERROR, "- Cannot write ", ERROR_INFO, str(len(szData)), ERROR, " bytes to ", ERROR_INFO, oExistingOfflineFileOrFolder.sPath, ERROR, "!");
                sys.exit(1);
          else:
            assert szData is not None, \
                "File or folder %s does not exist but there is also no data for it!?" % sRelativePath;
            oOfflineFile = oOfflineFolder.foGetDescendant(sRelativePath, bThrowErrors = bDebug);
            fPrintOrStatus("  + Saving ", INFO, sRelativePath, NORMAL, " (new file)");
            if not oOfflineFile.fbCreateAsFile(szData, bCreateParents = True, bParseZipFiles = False, bThrowErrors = bDebug):
              oConsole.fPrint(ERROR, "- Cannot write ", ERROR_INFO, str(len(szData)), ERROR, " bytes to ", ERROR_INFO, oOfflineFile.sPath, ERROR, "!");
              sys.exit(1);
      else:
        oConsole.fStatus("* Waiting for server to terminate...");
        oTreeServer.fWait();
        oConsole.fPrint("* Server terminated.");
    except:
      if sOfflineFolderPath is None:
        oTreeServer.fTerminate();
      raise;
    oConsole.fPrint("* Done.");
except Exception as oException:
  if fTerminateWithException:
    fTerminateWithException(oException);
  raise;