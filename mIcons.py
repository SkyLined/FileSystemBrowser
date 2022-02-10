from mFileSystemItem import cFileSystemItem;

goIconsFolder = cFileSystemItem(__file__).o0Parent.foGetChild("icons").foMustBeFolder();
goAudioFileIconFile = goIconsFolder.foGetChild("file-audio.png").foMustBeFile();
goBadZipFileIconFile = goIconsFolder.foGetChild("file-zip-bad.png").foMustBeFile();
goBinaryFileIconFile = goIconsFolder.foGetChild("file-binary.png").foMustBeFile();
goBrokenLinkIconFile = goIconsFolder.foGetChild("link-broken.png").foMustBeFile();
goDocumentFileIconFile = goIconsFolder.foGetChild("file-document.png").foMustBeFile();
goFileIconFile = goIconsFolder.foGetChild("file.png").foMustBeFile();
goFolderEmptyIconFile = goIconsFolder.foGetChild("folder-empty.png").foMustBeFile();
goFolderEmptyWithIndexIconFile = goIconsFolder.foGetChild("folder-empty-with-index.png").foMustBeFile();
goFolderWithContentIconFile = goIconsFolder.foGetChild("folder-with-content.png").foMustBeFile();
goFolderWithContentAndIndexIconFile = goIconsFolder.foGetChild("folder-with-content-and-index.png").foMustBeFile();
goGitFileIconFile = goIconsFolder.foGetChild("file-git.png").foMustBeFile();
goImageFileIconFile = goIconsFolder.foGetChild("file-image.png").foMustBeFile();
goLinkIconFile = goIconsFolder.foGetChild("link.png").foMustBeFile();
goLinkToWebSiteIconFile = goIconsFolder.foGetChild("link-to-website.png").foMustBeFile();
goLinkToSecureWebSiteIconFile = goIconsFolder.foGetChild("link-to-secure-website.png").foMustBeFile();
goLinkToEmailIconFile = goIconsFolder.foGetChild("email.png").foMustBeFile();
goLinkToInternalFileIconFile = goIconsFolder.foGetChild("link-to-file.png").foMustBeFile();
goLinkToInternalFolderIconFile = goIconsFolder.foGetChild("link-to-folder.png").foMustBeFile();
goLinkToExternalFolderIconFile = goIconsFolder.foGetChild("folder-link.png").foMustBeFile();
goNotFoundIconFile = goIconsFolder.foGetChild("not-found.png").foMustBeFile();
goPresentationFileIconFile = goIconsFolder.foGetChild("file-presentation.png").foMustBeFile();
goSourceFileIconFile = goIconsFolder.foGetChild("file-source.png").foMustBeFile();
goSpreadsheetFileIconFile = goIconsFolder.foGetChild("file-spreadsheet.png").foMustBeFile();
goTextFileIconFile = goIconsFolder.foGetChild("file-text.png").foMustBeFile();
goUnknownFileIconFile = goIconsFolder.foGetChild("file-unknown.png").foMustBeFile();
goUnknownFolderIconFile = goIconsFolder.foGetChild("folder-unknown.png").foMustBeFile();
goUnknownIconFile = goIconsFolder.foGetChild("unknown.png").foMustBeFile();
goValidZipFileIconFile = goIconsFolder.foGetChild("file-zip.png").foMustBeFile();
goVideoFileIconFile = goIconsFolder.foGetChild("file-video.png").foMustBeFile();
goVisualStudioFileIconFile = goIconsFolder.foGetChild("file-visual-studio.png").foMustBeFile();

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
