import re;

grbEMailAddress = re.compile(
  b"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\x22(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\x22)"
  b"@"
  b"(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
);

class cMailToURL(object):
  sbProtocol = b"mailto";
  @classmethod
  def fbIsValidMailToURL(cClass, sbMailToURL):
    return sbMailToURL.lower().startswith(b"%s:" % cClass.sbProtocol) and cClass.fbIsValidEMailAddress(sbMailToURL[len(cClass.sbProtocol) + 1:]);
  
  @staticmethod
  def fbIsValidEMailAddress(sbEMailAddress):
    return grbEMailAddress.match(sbEMailAddress) is not None;
  
  @classmethod
  def foFromBytesString(cClass, sbMailToURL):
    assert cClass.fbIsValidMailToURL(sbMailToURL), \
        "%s is not a valid %s: URL" % (repr(sbMailToURL), str(sbProtocol, "ascii", "strict"));
    return cClass(sbMailToURL[len(cClass.sbProtocol) + 1:]);
  
  def __init__(oSelf, sbEMailAddress):
    oSelf.sbEMailAddress = sbEMailAddress;
  
  @property
  def sbEMailAddress(oSelf):
    return oSelf.__sbEMailAddress;
  
  @sbEMailAddress.setter
  def sbEMailAddress(oSelf, sbEMailAddress):
    assert oSelf.fbIsValidEMailAddress(sbEMailAddress), \
        "Invalid email address %s" % repr(sbEMailAddress);
    oSelf.__sbEMailAddress = sbEMailAddress;
  
  def fsToString(oSelf):
    return "%s{%s}" % (oSelf.__class__.__name__, oSelf.__sbEMailAddress);
  
  def __str__(oSelf):
    return str("%s:%s" % (oSelf.sbProtocol, oSelf.sbEMailAddress), "ascii", "strict");
