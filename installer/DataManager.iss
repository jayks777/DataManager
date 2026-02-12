[Setup]
AppName=DataManager
AppVersion=1.0.0
AppPublisher=Jayks né vida
AppPublisherURL=https://github.com/jayks777
AppSupportURL=https://github.com/jayks777/DataManager
AppUpdatesURL=https://github.com/jayks777/DataManager/releases
DefaultDirName={pf}\DataManager
DefaultGroupName=DataManager
OutputDir=output
OutputBaseFilename=DataManagerSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\DataManager.exe
SetupIconFile=..\datamanager_app\assets\icons\app.ico
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
LicenseFile=..\LICENSE

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "..\dist\DataManager.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DataManager"; Filename: "{app}\DataManager.exe"
Name: "{commondesktop}\DataManager"; Filename: "{app}\DataManager.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na area de trabalho"; GroupDescription: "Atalhos:"
