import base64;

import mWindowsAPI;

from gsPowershellBinaryFilePath import gsPowershellBinaryFilePath;

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
  sEncodedLinkPath = '"%s"' % str(base64.b64encode(oLinkFile.sPath.encode("utf-8")), "ascii", "strict");
  sPowershellScript = gsPowershellScriptTemplateToExtractTargetFromLinkFile % sEncodedLinkPath;
  oPowerShellProcess = mWindowsAPI.cConsoleProcess.foCreateForBinaryPathAndArguments(
    sBinaryPath = gsPowershellBinaryFilePath,
    asArguments = ["-Command", "&", "{%s}" % sPowershellScript],
    bRedirectStdOut = True,
    bRedirectStdErr = True,
  );
  sbStdOut = oPowerShellProcess.oStdOutPipe.fsbReadBytes();
  assert oPowerShellProcess.fbWait(), \
      "Could not wait for PowerShell to terminate!?";
  sbStdErr = oPowerShellProcess.oStdErrPipe.fsbReadBytes();
  assert sbStdErr == b"" and oPowerShellProcess.uExitCode == 0, \
      "Powershell terminated with exit code %d.\n  command = %s\n  stdout = %s\n  stderr = %s" % (oPowerShellProcess.uExitCode, repr(sPowershellScript), repr(sbStdOut), repr(sbStdErr));
  sbEncodedPath = sbStdOut.strip();
  return base64.b64decode(sbEncodedPath).decode("utf-8") if sbEncodedPath else None;

