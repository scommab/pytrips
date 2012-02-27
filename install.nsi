; example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "pyTrips"

; The file to write
OutFile "pyTrips.exe"

; The default installation directory
InstallDir $PROGRAMFILES\pyTrips

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\NSIS_pyTrips" "Install_Dir"

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "pyTrips (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File "MSVCR71.dll"
  File "_controls_.pyd"
  File "_core_.pyd"
  File "_gdi_.pyd"
  File "_misc_.pyd"
  File "_windows_.pyd"
  File "_xrc.pyd"
  File "bz2.pyd"
  File "library.zip"
  File "main.exe"
  File "python24.dll"
  File "unicodedata.pyd"
  File "w9xpopen.exe"
  File "wxmsw26h_vc.dll"
  File "zlib.pyd"
  File "card.bmp"
  File "resources.xrc"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\NSIS_pyTrips "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyTrips" "DisplayName" "NSIS pyTrips"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyTrips" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyTrips" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyTrips" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\pyTrips"
  CreateShortCut "$SMPROGRAMS\pyTrips\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\pyTrips\pyTrips.lnk" "$INSTDIR\main.exe" "" "$INSTDIR\main.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\pyTrips"
  DeleteRegKey HKLM SOFTWARE\NSIS_pyTrips

  ; Remove files and uninstaller
  Delete "$INSTDIR\*.*"
  Delete $INSTDIR\uninstall.exe
  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\pyTrips\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\pyTrips"
  RMDir "$INSTDIR"

SectionEnd
