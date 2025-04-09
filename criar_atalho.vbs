Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
Set oShellLink = WshShell.CreateShortcut(strDesktop & "\PsiCollab Server.lnk")
oShellLink.TargetPath = WScript.CreateObject("WScript.Shell").CurrentDirectory & "\iniciar_psicollab.bat"
oShellLink.WorkingDirectory = WScript.CreateObject("WScript.Shell").CurrentDirectory
oShellLink.Save 