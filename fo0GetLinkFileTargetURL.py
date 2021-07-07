
import mHTTPProtocol;

from cMailToURL import cMailToURL;
from fs0GetLinkFileTarget import fs0GetLinkFileTarget;

def fo0GetLinkFileTargetURL(oLinkFile):
  s0TargetURL = fs0GetLinkFileTarget(oLinkFile);
  if not s0TargetURL:
    return None;
  sb0TargetURL = bytes(s0TargetURL, "ascii", "strict");
  return (
    cMailToURL.foFromBytesString(sb0TargetURL) if cMailToURL.fbIsValidMailToURL(sb0TargetURL) else
    mHTTPProtocol.cURL.foFromBytesString(sb0TargetURL)
  );

