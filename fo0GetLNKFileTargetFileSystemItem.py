import os;
if os.name != "nt":
  def fo0GetLNKFileTargetFileSystemItem(oLNKFile):
    return None;
else:
  from mFileSystemItem import cFileSystemItem;
  from fs0GetLNKFileTarget import fs0GetLNKFileTarget;

  def fo0GetLNKFileTargetFileSystemItem(oLNKFile):
    # This should work for .LNK and .URL files.
    s0TargetPath = fs0GetLNKFileTarget(oLNKFile);
    return cFileSystemItem(s0TargetPath) if s0TargetPath else None;

