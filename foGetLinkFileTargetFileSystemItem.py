
from mFileSystemItem import cFileSystemItem;

from fs0GetLinkFileTarget import fs0GetLinkFileTarget;

def foGetLinkFileTargetFileSystemItem(oLinkFile):
  # This should work for .LNK and .URL files.
  s0TargetPath = fs0GetLinkFileTarget(oLinkFile);
  return cFileSystemItem(s0TargetPath) if s0TargetPath else None;

