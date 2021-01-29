import base64, codecs, os, re;

from cTreeServer import cTreeServer;
from cFileSystemItem import cFileSystemItem;
import mHTTP, mWindowsAPI;
from oConsole import oConsole;

from foGetFavIconURLForHTTPClientsAndURL import foGetFavIconURLForHTTPClientsAndURL;
from mColors import *;

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
goGitFileIconFile = goIconsFolder.foGetChild("file-git.png", bMustBeFile = True);
goImageFileIconFile = goIconsFolder.foGetChild("file-image.png", bMustBeFile = True);
goLinkIconFile = goIconsFolder.foGetChild("link.png", bMustBeFile = True);
goLinkToWebSiteIconFile = goIconsFolder.foGetChild("link-to-website.png", bMustBeFile = True);
goLinkToSecureWebSiteIconFile = goIconsFolder.foGetChild("link-to-secure-website.png", bMustBeFile = True);
goLinkToEmailIconFile = goIconsFolder.foGetChild("email.png", bMustBeFile = True);
goLinkToInternalFileIconFile = goIconsFolder.foGetChild("link-to-file.png", bMustBeFile = True);
goLinkToInternalFolderIconFile = goIconsFolder.foGetChild("link-to-folder.png", bMustBeFile = True);
goLinkToExternalFolderIconFile = goIconsFolder.foGetChild("folder-link.png", bMustBeFile = True);
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

gsPowershellBinaryFilePath = os.path.join(os.getenv("WinDir"), r"System32\WindowsPowerShell\v1.0\powershell.exe");
gsPowershellBinaryFilePath = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe";
gsPowershellScriptTemplateToExtractTargetFromLinkFile = (
  "Write-Output ("
    "[System.Convert]::ToBase64String("
      "[System.Text.Encoding]::UTF8.GetBytes("
        "("
          "New-Object -ComObject WScript.Shell"
        ").CreateShortcut("
          "[System.Text.Encoding]::UTF8.GetString("
            "[System.Convert]::FromBase64String("
              "%s"
            ")"
          ")"
        ").TargetPath"
      ")"
    ")"
  ");"
);
def fs0GetLinkFileTarget(oLinkFile):
  # This should work for .LNK and .URL files.
  sEncodedLinkPath = '"%s"' % base64.b64encode(unicode(oLinkFile.sPath).encode("utf-8"));
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
  sEncodedPath = sStdOut.strip();
  return base64.b64decode(sEncodedPath).decode("utf-8") if sEncodedPath else None;

def foGetLinkFileTargetFileSystemItem(oLinkFile):
  # This should work for .LNK and .URL files.
  s0TargetPath = fs0GetLinkFileTarget(oLinkFile);
  return cFileSystemItem(s0TargetPath) if s0TargetPath else None;

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

def fo0GetLinkFileTargetURL(oLinkFile):
  s0TargetURL = fs0GetLinkFileTarget(oLinkFile);
  return (cMailToURL.fo0FromString(s0TargetURL) or mHTTP.cURL.foFromString(s0TargetURL)) \
      if s0TargetURL else None;

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

# Media types consist of a "type" and a "subtype". We assign icons based on the "type" part.
gdoIconFile_by_sMediaTypeType = {
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
  "git":  goGitFileIconFile,
  "gitattributes": goGitFileIconFile,
  "gitignore": goGitFileIconFile,
  "gitmodules": goGitFileIconFile,
  "h":    goSourceFileIconFile,
  "htm":  goDocumentFileIconFile,
  "html": goDocumentFileIconFile,
  "hxx":  goSourceFileIconFile,
  "java": goSourceFileIconFile,
  "js":   goSourceFileIconFile,
  "json": goSourceFileIconFile,
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
  "git":  "text",
  "gitattributes": "text",
  "gitignore": "text",
  "gitmodules": "text",
  "h":    "text",
  "htm":  "html",
  "html": "html",
  "hxx":  "text",
  "java": "text",
  "js":   "text",
  "json": "text",
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
  
  def fRefreshTree(oSelf, oTreeServer, aoHTTPClients, bThrowErrors = False, fProgressCallback = None):
    oSelf.fRemoveChildren();
    # If this item is stored in a zip file, we'll open the zip file now and
    # keep it open until we are done to cache its content.
    fProgressCallback(oSelf);
    if oSelf.oFileSystemItem.fbIsFolder(bThrowErrors = bThrowErrors):
      aoChildFileSystemItems = oSelf.oFileSystemItem.faoGetChildren(bThrowErrors = bThrowErrors) or [];
      oIconFile = goFolderEmptyIconFile if len(aoChildFileSystemItems) == 0 else goFolderWithContentIconFile;
      oSelf.oIconFile = goUnknownFolderIconFile;
    elif oSelf.oFileSystemItem.fbIsFile(bThrowErrors = bThrowErrors):
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
        elif oLNKFileTarget.sPath.startswith("\\"):
          oSelf.fLinkToURL("file:%s" % oLNKFileTarget.sPath.replace("\\", "/"));
          oSelf.sToolTip = oLNKFileTarget.sPath;
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
            oSelf.sName = oSelf.sName[:-4]; # remove ".lnk";
            oSelf.sToolTip = "Link to %s" % sRelativeTargetPath;
            oSelf.fLinkToNodeId(os.sep + sRelativeTargetPath);
            if oLNKFileTarget.fbIsFile():
              oIconFile = goLinkToInternalFileIconFile 
              aoChildFileSystemItems = None;
            else:
              oIconFile = goLinkToInternalFolderIconFile;
              aoChildFileSystemItems = [];
      elif sExtension.lower() == "url":
        o0URLFileTarget = fo0GetLinkFileTargetURL(oSelf.oFileSystemItem);
        if o0URLFileTarget is None:
          oIconFile = goBrokenLinkIconFile;
        else:
          if len(aoHTTPClients) > 0 and isinstance(o0URLFileTarget, mHTTP.cURL):
            oFavIconURL = foGetFavIconURLForHTTPClientsAndURL(aoHTTPClients, o0URLFileTarget);
            oSelf.sIconURL = str(oFavIconURL) if oFavIconURL else None;
          oIconFile = gdoLinkIconFile_by_sProtocolHeader.get(o0URLFileTarget.sProtocol, goLinkIconFile);
          oSelf.sName = oSelf.sName[:-4]; # remove ".url";
          sLinkURL = str(o0URLFileTarget);
          oSelf.sToolTip = sLinkURL;
          oSelf.fLinkToURL(sLinkURL);
        aoChildFileSystemItems = None;
      else:
        # Convert extension to media type, if any, then get the "type" part of the media type, if any:
        s0MediaType = mHTTP.fs0GetMediaTypeForExtension(sExtension) if sExtension else None;
        s0MediaTypeType = s0MediaType[:s0MediaType.find("/")] if s0MediaType else None;
        oIconFile = (
          # If we have an icon for this specifc extension, use that:
          gdoIconFile_by_sFileExtension.get(sExtension.lower())
          # Otherwise, if we have an icon for the "type" part of the media type
          # associated with the extension, use that:
          or gdoIconFile_by_sMediaTypeType.get(s0MediaTypeType)
          # Otherwise use a default icon
          or goFileIconFile
        );
        sNodeType = gdsNodeType_by_sFileExtension.get(sExtension.lower());
        if sNodeType:
          # This is not just a random file, it has a special meaning.
          # Read the file data.
          sFileData = oSelf.oFileSystemItem.fsRead(bThrowErrors = bThrowErrors);
          if sFileData is None:
            sNodeType = None; # Cannot read file data.
          elif "\0" in sFileData:
            # This file does not appear to have text content; treat it as a regular file.
            sNodeType = None;
          else:
            # This is supposed to be a text file: see if we can decode this:
            sEncoding = (
              "utf-8-sig" if sFileData.startswith(codecs.BOM_UTF8) else \
              "utf-16" if sFileData.startswith(codecs.BOM_UTF16_LE) or sFileData.startswith(codecs.BOM_UTF16_BE) else \
              "utf-32" if sFileData.startswith(codecs.BOM_UTF32_LE) or sFileData.startswith(codecs.BOM_UTF32_BE) else \
              "utf-8"
            );
            try:
              sFileData = sFileData.decode(sEncoding);
            except UnicodeError:
              try:
                sFileData = sFileData.decode("cp1252");
              except UnicodeDecodeError:
                # This file does not appear to have text content that we can decode; treat it as a regular file.
                sNodeType = None;
        if sNodeType:
          # Make sure the data can be utf-8 encoded
          try:
            sFileData.encode("utf-8");
          except UnicodeError as oException:
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
          sRelativeURL = "/files/%s" % sRelativePath.replace(os.sep, "/");
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
        oChildFileSystemTreeNode.fRefreshTree(oTreeServer, aoHTTPClients, bThrowErrors = bThrowErrors, fProgressCallback = fProgressCallback);
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
