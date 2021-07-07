
import mWindowsAPI;

from gsPowershellBinaryFilePath import gsPowershellBinaryFilePath;

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
  sbStdOut = oPowerShellProcess.oStdOutPipe.fsbReadBytes();
  assert oPowerShellProcess.fbWait(), \
      "Could not wait for PowerShell to terminate!?";
  sbStdErr = oPowerShellProcess.oStdErrPipe.fsbReadBytes();
  assert sbStdErr == b"" and oPowerShellProcess.uExitCode == 0, \
      "Powershell terminated with exit code %d.\n  stdout = %s\n  stderr = %s" % (oPowerShellProcess.uExitCode, repr(sbStdOut), repr(sbStdErr));
  return b"ok" == sbStdOut.strip();
