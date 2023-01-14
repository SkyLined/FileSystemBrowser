import os;
if os.name != "nt":
  def fo0GetLNKFileTargetURL(oLNKFile):
    return None;
else:
  import mHTTPProtocol;

  from cMailToURL import cMailToURL;
  from fs0GetLNKFileTarget import fs0GetLNKFileTarget;

  def fo0GetLNKFileTargetURL(oLNKFile):
    s0TargetURL = fs0GetLNKFileTarget(oLNKFile);
    if not s0TargetURL:
      return None;
    sb0TargetURL = bytes(s0TargetURL, "ascii", "strict");
    return (
      cMailToURL.foFromBytesString(sb0TargetURL) if cMailToURL.fbIsValidMailToURL(sb0TargetURL) else
      mHTTPProtocol.cURL.foFromBytesString(sb0TargetURL)
    );

