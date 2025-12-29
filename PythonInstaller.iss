; Python Installer for Professional Video Editor
; Standalone installer for Python version only

[Setup]
AppName=Professional Video Editor (Python)
AppVersion=1.0.0
AppPublisher=Robert Foster
AppPublisherURL=https://github.com/devildog5x5/Video_Editor
AppSupportURL=https://github.com/devildog5x5/Video_Editor
AppUpdatesURL=https://github.com/devildog5x5/Video_Editor
DefaultDirName={autopf}\VideoEditorPython
DefaultGroupName=Video Editor (Python)
AllowNoIcons=yes
LicenseFile=
OutputDir=installer
OutputBaseFilename=VideoEditor-Python-Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\VideoEditor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "QUICK_START.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Video Editor (Python)"; Filename: "{app}\VideoEditor.exe"; IconFilename: "{app}\icon.ico"
Name: "{autodesktop}\Video Editor (Python)"; Filename: "{app}\VideoEditor.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Video Editor (Python)"; Filename: "{app}\VideoEditor.exe"; IconFilename: "{app}\icon.ico"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\VideoEditor.exe"; Description: "{cm:LaunchProgram,Video Editor (Python)}"; Flags: nowait postinstall skipifsilent

