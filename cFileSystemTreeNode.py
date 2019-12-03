import codecs, os, re;
from cTreeServer import cTreeServer;
from cFileSystemItem import cFileSystemItem;
import mHTTP, mWindowsAPI;
from oConsole import oConsole;
from mColors import *;

from foGetFavIconURLForHTTPClientsAndURL import foGetFavIconURLForHTTPClientsAndURL;

grEMailAddress = re.compile(
  "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\x22(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\x22)"
  "@"
  "(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
);
goIconsFolder = cFileSystemItem(__file__).oParent.foGetChild("icons", bMustBeFolder = True);

goAudioFileIconFile = goIconsFolder.foGetChild("file-audio.png", bMustBeFile = True);
goBadZipFileIconFile = goIconsFolder.foGetChild("file-zip-bad.png", bMustBeFile = True);
goBinaryFileIconFile = goIconsFolder.foGetChild("file-binary.png", bMustBeFile = True);
goBrokenLinkIconFile = goIconsFolder.foGetChild("link-broken.png", bMustBeFile = True);
goDocumentFileIconFile = goIconsFolder.foGetChild("file-document.png", bMustBeFile = True);
goFileIconFile = goIconsFolder.foGetChild("file.png", bMustBeFile = True);
goFolderEmptyIconFile = goIconsFolder.foGetChild("folder-empty.png", bMustBeFile = True);
goFolderEmptyWithIndexIconFile = goIconsFolder.foGetChild("folder-empty-with-index.png", bMustBeFile = True);
goFolderWithContentIconFile = goIconsFolder.foGetChild("folder-with-content.png", bMustBeFile = True);
goFolderWithContentAndIndexIconFile = goIconsFolder.foGetChild("folder-with-content-and-index.png", bMustBeFile = True);
goImageFileIconFile = goIconsFolder.foGetChild("file-image.png", bMustBeFile = True);
goLinkIconFile = goIconsFolder.foGetChild("link.png", bMustBeFile = True);
goLinkToWebSiteIconFile = goIconsFolder.foGetChild("link-to-website.png", bMustBeFile = True);
goLinkToSecureWebSiteIconFile = goIconsFolder.foGetChild("link-to-secure-website.png", bMustBeFile = True);
goLinkToEmailIconFile = goIconsFolder.foGetChild("email.png", bMustBeFile = True);
goLinkToInternalFileIconFile = goIconsFolder.foGetChild("link-to-file.png", bMustBeFile = True);
goLinkToInternalFolderIconFile = goIconsFolder.foGetChild("link-to-folder.png", bMustBeFile = True);
goNotFoundIconFile = goIconsFolder.foGetChild("not-found.png", bMustBeFile = True);
goPresentationFileIconFile = goIconsFolder.foGetChild("file-presentation.png", bMustBeFile = True);
goSourceFileIconFile = goIconsFolder.foGetChild("file-source.png", bMustBeFile = True);
goSpreadsheetFileIconFile = goIconsFolder.foGetChild("file-spreadsheet.png", bMustBeFile = True);
goTextFileIconFile = goIconsFolder.foGetChild("file-text.png", bMustBeFile = True);
goUnknownFileIconFile = goIconsFolder.foGetChild("file-unknown.png", bMustBeFile = True);
goUnknownFolderIconFile = goIconsFolder.foGetChild("folder-unknown.png", bMustBeFile = True);
goUnknownIconFile = goIconsFolder.foGetChild("unknown.png", bMustBeFile = True);
goValidZipFileIconFile = goIconsFolder.foGetChild("file-zip.png", bMustBeFile = True);
goVideoFileIconFile = goIconsFolder.foGetChild("file-video.png", bMustBeFile = True);
goVisualStudioFileIconFile = goIconsFolder.foGetChild("file-visual-studio.png", bMustBeFile = True);

gsPowershellBinaryFilePath = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
gsPowershellScriptTemplateToExtractTargetFromLinkFile = \
    "Write-Output ((New-Object -ComObject WScript.Shell).CreateShortcut(%s).TargetPath);";
def fsGetLinkFileTarget(oLinkFile):
  # This should work for .LNK and .URL files.
  sEncodedLinkPath = '"%s"' % "".join(map(lambda sChar: (
      "``" if sChar == "`" else \
      '`"' if sChar == '"' else \
      sChar if 0x20 <= ord(sChar) <= 0x7e \
      else "`u{%X}" % ord(sChar)
  ), oLinkFile.sPath));
  sPowershellScript = gsPowershellScriptTemplateToExtractTargetFromLinkFile % sEncodedLinkPath;
  oPowerShellProcess = mWindowsAPI.cConsoleProcess.foCreateForBinaryPathAndArguments(
    sBinaryPath = gsPowershellBinaryFilePath,
    asArguments = ["-Command", "&", "{%s}" % sPowershellScript],
    bRedirectStdOut = True,
    bRedirectStdErr = True,
  );
  sStdOut = oPowerShellProcess.oStdOutPipe.fsReadBytes();
  assert oPowerShellProcess.fbWait(), \
      "Could not wait for PowerShell to terminate!?";
  sStdErr = oPowerShellProcess.oStdErrPipe.fsReadBytes();
  assert sStdErr == "" and oPowerShellProcess.uExitCode == 0, \
      "Powershell terminated with exit code %d.\n  command = %s\n  stdout = %s\n  stderr = %s" % (oPowerShellProcess.uExitCode, repr(sPowershellScript), repr(sStdOut), repr(sStdErr));
  return sStdOut.strip();

def foGetLinkFileTargetFileSystemItem(oLinkFile):
  # This should work for .LNK and .URL files.
  sTargetPath = fsGetLinkFileTarget(oLinkFile);
  return cFileSystemItem(sTargetPath) if sTargetPath else None;

class cMailToURL(object):
  sProtocol = "mailto";
  @classmethod
  def fbIsValidMailToURL(cClass, sMailToURL):
    return sMailToURL.lower().startswith("%s:" % cClass.sProtocol) and cClass.fbIsValidEMailAddress(sMailToURL[7:]);
  
  @staticmethod
  def fbIsValidEMailAddress(sEMailAddress):
    return grEMailAddress.match(sEMailAddress) is not None;
  
  @classmethod
  def fo0FromString(cClass, sMailToURL):
    return cClass(sMailToURL[7:]) if cClass.fbIsValidMailToURL(sMailToURL) else None;
  
  def __init__(oSelf, sEMailAddress):
    oSelf.sEMailAddress = sEMailAddress;
  
  @property
  def sEMailAddress(oSelf):
    return oSelf.__sEMailAddress;
  
  @sEMailAddress.setter
  def sEMailAddress(oSelf, sEMailAddress):
    assert oSelf.fbIsValidEMailAddress(sEMailAddress), \
        "Invalid email address %s" % repr(sEMailAddress);
    oSelf.__sEMailAddress = sEMailAddress;
  
  def fsToString(oSelf):
    return "%s{%s}" % (oSelf.__class__.__name__, oSelf.__sEMailAddress);
    
  def __str__(oSelf):
    return "%s:%s" % (oSelf.sProtocol, oSelf.sEMailAddress);

def foGetLinkFileTargetURL(oLinkFile):
  sTargetURL = fsGetLinkFileTarget(oLinkFile);
  return (cMailToURL.fo0FromString(sTargetURL) or mHTTP.cURL.foFromString(sTargetURL)) \
      if sTargetURL else None;

gsPowershellScriptTemplateToModifyTargetInLNKFile = \
    "$oShortcut = (New-Object -ComObject WScript.Shell).CreateShortcut(\"%s\");$oShortcut.TargetPath = \"%s\";$oShortcut.Save();Write-Output (\"ok\");";
def fbSetLNKFileTarget(oLNKFile, oNewTarget):
  sPowershellScript = gsPowershellScriptTemplateToModifyTargetInLNKFile % (oLNKFile.sPath, oNewTarget.sPath);
  oPowerShellProcess = mWindowsAPI.cConsoleProcess.foCreateForBinaryPathAndArguments(
    sBinaryPath = gsPowershellBinaryFilePath,
    asArguments = ["-Command", "& {%s}" % sPowershellScript],
    bRedirectStdOut = True,
    bRedirectStdErr = True,
  );
  sStdOut = oPowerShellProcess.oStdOutPipe.fsReadBytes();
  assert oPowerShellProcess.fbWait(), \
      "Could not wait for PowerShell to terminate!?";
  sStdErr = oPowerShellProcess.oStdErrPipe.fsReadBytes();
  assert sStdErr == "" and oPowerShellProcess.uExitCode == 0, \
      "Powershell terminated with exit code %d.\n  stdout = %s\n  stderr = %s" % (oPowerShellProcess.uExitCode, repr(sStdOut), repr(sStdErr));
  return "ok" == sStdOut.strip();


gdoIconFile_by_sMainType = {
  "application": goBinaryFileIconFile,
  "video": goVideoFileIconFile,
  "audio": goAudioFileIconFile,
  "image": goImageFileIconFile,
  "text": goTextFileIconFile,
};
gdoIconFile_by_sFileExtension = {
  "c":    goSourceFileIconFile,
  "cmd":  goSourceFileIconFile,
  "cpp":  goSourceFileIconFile,
  "css":  goSourceFileIconFile,
  "cxx":  goSourceFileIconFile,
  "doc":  goDocumentFileIconFile,
  "docx": goDocumentFileIconFile,
  "java": goSourceFileIconFile,
  "js":   goSourceFileIconFile,
  "json": goSourceFileIconFile,
  "h":    goSourceFileIconFile,
  "htm":  goDocumentFileIconFile,
  "html": goDocumentFileIconFile,
  "hxx":  goSourceFileIconFile,
  "md":   goDocumentFileIconFile,
  "pdf":  goDocumentFileIconFile,
  "ppt":  goPresentationFileIconFile,
  "pptx": goPresentationFileIconFile,
  "ps1":  goSourceFileIconFile,
  "py":   goSourceFileIconFile,
  "rtf":  goDocumentFileIconFile,
  "sln":  goVisualStudioFileIconFile,
  "svg":  goImageFileIconFile,
  "txt":  goTextFileIconFile,
  "vbs":  goSourceFileIconFile,
  "xls":  goSpreadsheetFileIconFile,
  "xlsx": goSpreadsheetFileIconFile,
};
gdsNodeType_by_sFileExtension = {
  "c":    "text",
  "cmd":  "text",
  "cpp":  "text",
  "css":  "text",
  "cxx":  "text",
  "java": "text",
  "js":   "text",
  "json": "text",
  "h":    "text",
  "htm":  "html",
  "html": "html",
  "hxx":  "text",
  "md":   "markdown",
  "ps1":  "text",
  "py":   "text",
  "rtf":  "text",
  "svg":  "html",
  "txt":  "text",
  "vbs":  "text",
};
gdoLinkIconFile_by_sProtocolHeader = {
  "mailto:": goLinkToEmailIconFile,
  "http://": goLinkToWebSiteIconFile,
  "https://": goLinkToSecureWebSiteIconFile,
};

class cFileSystemTreeNode(cTreeServer.cTreeNode):
  sNamespace = "cFileSystemTreeNode";
  oIconsFolder = goIconsFolder;
  def __init__(oSelf, oFileSystemItem, oRootFileSystemItem = None, sId = None, bOpened = None, \
      bDisabled = None, bSelected = None, aoHTTPClients = None):
    cTreeServer.cTreeNode.__init__(oSelf, oFileSystemItem.sName, sId = sId, \
        oIconFile = goUnknownIconFile, bOpened = bOpened, bDisabled = bDisabled, bSelected = bSelected);
    oSelf.oFileSystemItem = oFileSystemItem;
    oSelf.oRootFileSystemItem = oRootFileSystemItem or oFileSystemItem;
    oSelf.sId = os.sep + (oRootFileSystemItem.fsGetRelativePathTo(oFileSystemItem) if oRootFileSystemItem else "");
  
  def fRefreshTree(oSelf, oTreeServer, aoHTTPClients, bThrowErrors = False):
    oSelf.fRemoveChildren();
    # If this item is stored in a zip file, we'll open the zip file now and
    # keep it open until we are done to cache its content.
    if oSelf.oFileSystemItem.fbIsFolder(bThrowErrors = bThrowErrors):
      aoChildFileSystemItems = oSelf.oFileSystemItem.faoGetChildren(bThrowErrors = bThrowErrors) or [];
      oIconFile = goFolderEmptyIconFile if len(aoChildFileSystemItems) == 0 else goFolderWithContentIconFile;
      oSelf.oIconFile = goUnknownFolderIconFile;
    else:
      if oSelf.oFileSystemItem.fbIsFile(bThrowErrors = bThrowErrors):
        sExtension = oSelf.oFileSystemItem.sExtension;
        oSelf.oIconFile = goUnknownFileIconFile;
        if not sExtension:
          # No extension
          oIconFile = goFileIconFile;
          aoChildFileSystemItems = None;
        elif sExtension.lower() == "zip":
          if oSelf.oFileSystemItem.fbIsValidZipFile(bThrowErrors = bThrowErrors):
            # Let's keep this zip file open while we are done.
            oIconFile = goValidZipFileIconFile;
            oSelf.oIconFile = goUnknownFolderIconFile;
            aoChildFileSystemItems = oSelf.oFileSystemItem.faoGetChildren(bThrowErrors = bThrowErrors) or [];
          else:
            # .zip extension but not a valid zip file (or it would have been handles in the code above).
            oIconFile = goBadZipFileIconFile;
            aoChildFileSystemItems = None;
        elif sExtension.lower() == "lnk":
          oLNKFileTarget = foGetLinkFileTargetFileSystemItem(oSelf.oFileSystemItem);
          if oLNKFileTarget is None:
            oConsole.fPrint(ERROR, "- Link file: ", ERROR_INFO, oSelf.oFileSystemItem.sPath, ERROR, " is broken!");
            oSelf.sToolTip = "Link file is broken.";
            oIconFile = goBrokenLinkIconFile;
            aoChildFileSystemItems = None;
          else:
            sRelativeTargetPath = oSelf.oRootFileSystemItem.fsGetRelativePathTo(oLNKFileTarget, bThrowErrors = False);
            bLinkIsValid = sRelativeTargetPath and oLNKFileTarget.fbExists();
            if not bLinkIsValid:
              oConsole.fPrint(WARNING, "- Link file ", WARNING_INFO, oSelf.oFileSystemItem.sPath, WARNING, " links to ",
                "a file or folder outside of the visible tree" if sRelativeTargetPath is None
                else "a missing file or folder",
                " (", WARNING_INFO, oLNKFileTarget.sPath, WARNING, ")!");
              oConsole.fStatus("* Attempting to fix link ...");
              # The target could have been moved, so try to figure out what it should be.
              sPotentialRelativeTargetPath = oLNKFileTarget.sName;
              oPotentialTargetOriginalParent = oLNKFileTarget.oParent;
              while oPotentialTargetOriginalParent:
                oPotentialTarget = oSelf.oRootFileSystemItem.foGetDescendant(sPotentialRelativeTargetPath, bParseZipFiles = False);
                if oPotentialTarget.fbExists():
                  sRelativeTargetPath = sPotentialRelativeTargetPath;
                  oLNKFileTarget = oPotentialTarget;
                  bLinkIsValid = True;
                  if not fbSetLNKFileTarget(oSelf.oFileSystemItem, oLNKFileTarget):
                    oConsole.fPrint(ERROR, "  Cannot redirect the link to ", ERROR_INFO, oLNKFileTarget.sPath, ERROR, ".");
                  else:
                    oConsole.fPrint(WARNING, "  The link has been redirected to ", WARNING_INFO, oLNKFileTarget.sPath, WARNING, ".");
                  break;
                sPotentialRelativeTargetPath = oPotentialTargetOriginalParent.sName + os.sep + sPotentialRelativeTargetPath;
                oPotentialTargetOriginalParent = oPotentialTargetOriginalParent.oParent;
              else:
                oConsole.fPrint(ERROR, "  The link cannot be fixed!");
            if not bLinkIsValid:
              oSelf.sToolTip = (
                "Link target is outside of visible tree." if sRelativeTargetPath is None
                else "Link target does not exist."
              );
              oIconFile = goBrokenLinkIconFile;
              aoChildFileSystemItems = None;
            else:
              if oLNKFileTarget.fbIsFile():
                oIconFile = goLinkToInternalFileIconFile 
                aoChildFileSystemItems = None;
              else:
                oIconFile = goLinkToInternalFolderIconFile;
                aoChildFileSystemItems = [];
              oSelf.sName = oSelf.sName[:-4]; # remove ".lnk";
              oSelf.sToolTip = "Link to %s" % sRelativeTargetPath;
              oSelf.fLinkToNodeId(os.sep + sRelativeTargetPath);
        elif sExtension.lower() == "url":
          oURLFileTarget = foGetLinkFileTargetURL(oSelf.oFileSystemItem);
          if oURLFileTarget is None:
            oIconFile = goBrokenLinkIconFile;
          else:
            if len(aoHTTPClients) > 0 and isinstance(oURLFileTarget, mHTTP.cURL):
              oFavIconURL = foGetFavIconURLForHTTPClientsAndURL(aoHTTPClients, oURLFileTarget);
              oSelf.sIconURL = str(oFavIconURL) if oFavIconURL else None;
            oIconFile = gdoLinkIconFile_by_sProtocolHeader.get(oURLFileTarget.sProtocol, goLinkIconFile);
            oSelf.sName = oSelf.sName[:-4]; # remove ".url";
            sLinkURL = str(oURLFileTarget);
            oSelf.sToolTip = sLinkURL;
            oSelf.fLinkToURL(sLinkURL);
          aoChildFileSystemItems = None;
        else:
          # icon depends on the extension or media type.
          sMediaType = mHTTP.fsGetMediaTypeForExtension(sExtension) if sExtension else None;
          sMainType = sMediaType[:sMediaType.find("/")] if sMediaType else None;
          oIconFile = (
            gdoIconFile_by_sFileExtension.get(sExtension.lower())
            or gdoIconFile_by_sMainType.get(sMainType)
            or goFileIconFile
          );
          sNodeType = gdsNodeType_by_sFileExtension.get(sExtension.lower());
          if sNodeType:
            sFileData = oSelf.oFileSystemItem.fsRead(bThrowErrors = bThrowErrors);
            if sFileData is not None:
              if sMainType == "text":
                sEncoding = (
                  "utf-8-sig" if sFileData.startswith(codecs.BOM_UTF8) else \
                  "utf-16" if sFileData.startswith(codecs.BOM_UTF16_LE) or sFileData.startswith(codecs.BOM_UTF16_BE) else \
                  "utf-32" if sFileData.startswith(codecs.BOM_UTF32_LE) or sFileData.startswith(codecs.BOM_UTF32_BE) else \
                  "utf-8"
                );
                try:
                  sFileData = sFileData.decode(sEncoding);
                except UnicodeDecodeError:
                  sFileData = sFileData.decode("cp1252");
                try:
                  sFileData.encode("utf-8");
                except Exception as oException:
                  oConsole.fPrint(ERROR, "- Text encoding problem in ", ERROR_INFO, oSelf.oFileSystemItem.sPath, ERROR, "!");
                  oConsole.fPrint(ERROR_INFO, "  ", str(oException));
                  raise;
              oSelf.sType = sNodeType;
              oSelf.xData = sFileData;
          else:
            if oSelf.oRootFileSystemItem != oSelf.oFileSystemItem:
              sRelativePath = oSelf.oRootFileSystemItem.fsGetRelativePathTo( \
                  oSelf.oFileSystemItem, bThrowErrors = bThrowErrors);
            else:
              sRelativePath = oSelf.oRootFileSystemItem.sName;
            sRelativeURL = "files/%s" % sRelativePath.replace(os.sep, "/");
            oTreeServer.doFile_by_sRelativeURL[sRelativeURL] = oSelf.oFileSystemItem;
            oSelf.sType = "iframe";
            oSelf.xData = sRelativeURL;
          aoChildFileSystemItems = None;
      else:
        oIconFile = goNotFoundIconFile;
        aoChildFileSystemItems = None;
    
    if aoChildFileSystemItems:
      # Step 1: add all child nodes alphabetically as placeholders
      doChildFileSystemItem_by_sName = dict([
        (oItem.sName, oItem) for oItem in aoChildFileSystemItems
      ]) if aoChildFileSystemItems else {};
      aoChildFileSystemTreeNodes = [];
      asSortedNames = doChildFileSystemItem_by_sName.keys();
      asSortedNames.sort();
      for sName in asSortedNames:
        oChildFileSystemItem = doChildFileSystemItem_by_sName[sName];
        oChildFileSystemTreeNode = cFileSystemTreeNode(oChildFileSystemItem, oSelf.oRootFileSystemItem);
        oSelf.fAppendChild(oChildFileSystemTreeNode);
        aoChildFileSystemTreeNodes.append(oChildFileSystemTreeNode);
      # Step 2: refresh tree for all child nodes and update their location based on the finding
      # Anything that can have children is "grouped with folders", i.e. stays near the top.
      # Anything else is moved to the bottom and grouped with files.
      aoIndexFileTreeNodes = [];
      for oChildFileSystemTreeNode in aoChildFileSystemTreeNodes:
        oChildFileSystemTreeNode.fRefreshTree(oTreeServer, aoHTTPClients, bThrowErrors = bThrowErrors);
        if not oChildFileSystemTreeNode.bGroupWithFolders:
          # Files are grouped below the folders, so move it downwards:
          oSelf.fRemoveChild(oChildFileSystemTreeNode);
          oSelf.fAppendChild(oChildFileSystemTreeNode);
          # This may be the index file.
          if oChildFileSystemTreeNode.oFileSystemItem.sName.lower().startswith("index."):
            aoIndexFileTreeNodes.append(oChildFileSystemTreeNode);
      # Step 3: If a single index file was found, use it for the folder.
      oIndexFileTreeNode = aoIndexFileTreeNodes[0] if len(aoIndexFileTreeNodes) == 1 else None;
      if oIndexFileTreeNode:
        # The index file type and data is copied to the folder and the index file is removed from the tree.
        oSelf.sType = oIndexFileTreeNode.sType;
        oSelf.xData = oIndexFileTreeNode.xData;
        oIconFile = goFolderEmptyWithIndexIconFile if len(aoChildFileSystemItems) == 1 \
            else goFolderWithContentAndIndexIconFile;
        # The child is therefore removed.
        oSelf.fRemoveChild(oIndexFileTreeNode);
    oSelf.oIconFile = oIconFile;
    oSelf.bGroupWithFolders = aoChildFileSystemItems is not None;
