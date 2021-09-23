import codecs, os;

from mTreeServer import cTreeServer;
import mHTTPProtocol;
from mConsole import oConsole;

from cMailToURL import cMailToURL;
from fbSetLNKFileTarget import fbSetLNKFileTarget;
from foGetFavIconURLForHTTPClientsAndURL import foGetFavIconURLForHTTPClientsAndURL;
from foGetLinkFileTargetFileSystemItem import foGetLinkFileTargetFileSystemItem;
from fo0GetLinkFileTargetURL import fo0GetLinkFileTargetURL;
from fs0GetLinkFileTarget import fs0GetLinkFileTarget;
from mColorsAndChars import *;
from mIcons import *;

gdsTextNodeType_by_sFileExtension = {
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
gdsNodeType_by_sMediaTypeType = {
  b"video": "video",
  b"audio": "audio",
  b"image": "image",
  b"text": "text",
};

class cFileSystemTreeNode(cTreeServer.cTreeNode):
  sNamespace = "cFileSystemTreeNode";
  oIconsFolder = goIconsFolder;
  def __init__(oSelf,
    oFileSystemItem,
    oRootFileSystemItem = None,
    sId = None,
    bOpened = None,
    bDisabled = None,
    bSelected = None,
    aoHTTPClients = None
  ):
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
      s0Extension = oSelf.oFileSystemItem.s0Extension;
      oSelf.oIconFile = goUnknownFileIconFile;
      if not s0Extension:
        # No extension
        oIconFile = goFileIconFile;
        aoChildFileSystemItems = None;
      elif s0Extension.lower() == "zip":
        if oSelf.oFileSystemItem.fbIsValidZipFile(bThrowErrors = bThrowErrors):
          # Let's keep this zip file open while we are done.
          oIconFile = goValidZipFileIconFile;
          oSelf.oIconFile = goUnknownFolderIconFile;
          aoChildFileSystemItems = oSelf.oFileSystemItem.faoGetChildren(bThrowErrors = bThrowErrors) or [];
        else:
          # .zip extension but not a valid zip file (or it would have been handles in the code above).
          oIconFile = goBadZipFileIconFile;
          aoChildFileSystemItems = None;
      elif s0Extension.lower() == "lnk":
        oLNKFileTarget = foGetLinkFileTargetFileSystemItem(oSelf.oFileSystemItem);
        if oLNKFileTarget is None:
          oConsole.fOutput(
            COLOR_ERROR, CHAR_ERROR,
            COLOR_NORMAL, " Link file: ",
            COLOR_INFO, oSelf.oFileSystemItem.sPath,
            COLOR_NORMAL, " is broken!",
          );
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
            oConsole.fOutput(
              COLOR_WARNING, CHAR_WARNING,
              COLOR_NORMAL, " Link file ",
              COLOR_INFO, oSelf.oFileSystemItem.sPath,
              COLOR_NORMAL,
              " links to a file or folder outside of the visible tree" if sRelativeTargetPath is None else "a missing file or folder",
              " (",
              COLOR_INFO, oLNKFileTarget.sPath,
              COLOR_NORMAL, ")!",
            );
            oConsole.fStatus(
              COLOR_BUSY, CHAR_BUSY,
              COLOR_NORMAL, " Attempting to fix link ...",
            );
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
                  oConsole.fOutput(
                    "  ",
                    COLOR_ERROR, CHAR_ERROR,
                    COLOR_NORMAL, " Cannot redirect the link to ",
                    COLOR_INFO, oLNKFileTarget.sPath,
                    COLOR_NORMAL, ".",
                  );
                else:
                  oConsole.fOutput(
                    "  ",
                    COLOR_WARNING, CHAR_WARNING,
                    COLOR_NORMAL, " The link has been redirected to ",
                    COLOR_INFO, oLNKFileTarget.sPath,
                    COLOR_NORMAL, ".",
                  );
                break;
              sPotentialRelativeTargetPath = oPotentialTargetOriginalParent.sName + os.sep + sPotentialRelativeTargetPath;
              oPotentialTargetOriginalParent = oPotentialTargetOriginalParent.oParent;
            else:
              oConsole.fOutput(
                "  ",
                COLOR_ERROR, CHAR_ERROR,
                COLOR_NORMAL, " The link cannot be fixed!",
              );
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
      elif s0Extension.lower() == "url":
        o0URLFileTarget = fo0GetLinkFileTargetURL(oSelf.oFileSystemItem);
        if o0URLFileTarget is None:
          oIconFile = goBrokenLinkIconFile;
        else:
          if len(aoHTTPClients) > 0 and isinstance(o0URLFileTarget, mHTTPProtocol.cURL):
            oFavIconURL = foGetFavIconURLForHTTPClientsAndURL(aoHTTPClients, o0URLFileTarget);
            oSelf.sIconURL = str(oFavIconURL) if oFavIconURL else None;
          oIconFile = gdoLinkIconFile_by_sbProtocolHeader.get(o0URLFileTarget.sbProtocol, goLinkIconFile);
          oSelf.sName = oSelf.sName[:-4]; # remove ".url";
          sLinkURL = str(o0URLFileTarget);
          oSelf.sToolTip = sLinkURL;
          oSelf.fLinkToURL(sLinkURL);
        aoChildFileSystemItems = None;
      else:
        sExtension = s0Extension; # Never None at this point.
        # Convert extension to media type, if any, then get the "type" part of the media type, if any:
        sb0MediaType = mHTTPProtocol.fsb0GetMediaTypeForExtension(s0Extension);
        sb0MediaTypeType = sb0MediaType.split(b"/", 1)[0] if sb0MediaType else None;
        oIconFile = (
          # If we have an icon for this specifc extension, use that:
          gdoIconFile_by_sFileExtension.get(sExtension.lower())
          # Otherwise, if we have an icon for the "type" part of the media type
          # associated with the extension, use that:
          or gdoIconFile_by_sbMediaTypeType.get(sb0MediaTypeType)
          # Otherwise use a default icon
          or goFileIconFile
        );
        s0TextNodeType = gdsTextNodeType_by_sFileExtension.get(sExtension.lower());
        
        if s0TextNodeType:
          # This is not just a random file, it has a special meaning.
          # Read the file data.
          sb0FileData = oSelf.oFileSystemItem.fsbRead(bThrowErrors = bThrowErrors);
          if sb0FileData is not None:
            sbFileData = sb0FileData;
            if b"\0" in sbFileData:
              # This file does not appear to have text content; treat it as a regular file.
              s0TextNodeType = None;
            else:
              # This is supposed to be a text file; if there is a BOM, try to decode based on that:
              s0Encoding = (
                "utf-8-sig" if sbFileData.startswith(codecs.BOM_UTF8) else \
                "utf-16" if sbFileData.startswith(codecs.BOM_UTF16_LE) or sbFileData.startswith(codecs.BOM_UTF16_BE) else \
                "utf-32" if sbFileData.startswith(codecs.BOM_UTF32_LE) or sbFileData.startswith(codecs.BOM_UTF32_BE) else \
                None
              );
              if s0Encoding:
                try:
                  sFileData = str(sbFileData, s0Encoding);
                except UnicodeError:
                  s0TextNodeType = None;
              else:
                # Otherwise, try utf-8 first, then cp1252. If noth fail, assume it is not a text file.
                try:
                  sFileData = str(sbFileData, "utf-8");
                except UnicodeDecodeError:
                  try:
                    sFileData = str(sbFileData, "cp1252");
                  except UnicodeDecodeError:
                    # This file does not appear to have text content that we can decode; treat it as a regular file.
                    s0TextNodeType = None;
              if s0TextNodeType:
                # Make sure the data can be utf-8 encoded
                try:
                  bytes(sFileData, "utf-8");
                except UnicodeError as oException:
                  oConsole.fOutput(
                    COLOR_ERROR, CHAR_ERROR,
                    COLOR_NORMAL, " Text encoding problem in ",
                    COLOR_INFO, oSelf.oFileSystemItem.sPath,
                    COLOR_NORMAL, "!",
                  );
                  oConsole.fOutput(
                    "  ",
                    COLOR_INFO, str(oException),
                  );
                  raise;
        if s0TextNodeType:
          oSelf.sType = s0TextNodeType;
          oSelf.xData = sFileData;
        else:
          if oSelf.oRootFileSystemItem != oSelf.oFileSystemItem:
            sRelativePath = oSelf.oRootFileSystemItem.fsGetRelativePathTo( \
                oSelf.oFileSystemItem, bThrowErrors = bThrowErrors);
          else:
            sRelativePath = oSelf.oRootFileSystemItem.sName;
          sRelativeURL = "/files/%s" % sRelativePath.replace(os.sep, "/");
          oTreeServer.doFile_by_sRelativeURL[sRelativeURL] = oSelf.oFileSystemItem;
          oSelf.sType = gdsNodeType_by_sMediaTypeType.get(sb0MediaTypeType, "iframe");
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
      asSortedNames = list(doChildFileSystemItem_by_sName.keys());
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
