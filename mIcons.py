from mFileSystemItem import cFileSystemItem;

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

# Media types consist of a "type" and a "subtype". We assign icons based on the "type" part.
gdoIconFile_by_sbMediaTypeType = {
  b"application": goBinaryFileIconFile,
  b"video": goVideoFileIconFile,
  b"audio": goAudioFileIconFile,
  b"image": goImageFileIconFile,
  b"text": goTextFileIconFile,
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
gdoLinkIconFile_by_sbProtocolHeader = {
  b"mailto:": goLinkToEmailIconFile,
  b"http://": goLinkToWebSiteIconFile,
  b"https://": goLinkToSecureWebSiteIconFile,
};
