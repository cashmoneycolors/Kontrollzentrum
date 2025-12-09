@echo off
REM 🚀 INSTALL ROBOTER_KI_APP.exe

echo.
echo ========================================
echo 🚀 INSTALLING ROBOTER_KI_APP.exe
echo ========================================
echo.

REM Create Desktop folder
if not exist "%USERPROFILE%\Desktop\Projekte" (
    mkdir "%USERPROFILE%\Desktop\Projekte"
    echo ✅ Created Desktop\Projekte folder
)

REM Copy Batch Launcher as EXE
echo [1/3] Creating EXE launcher...
copy ROBOTER_KI_APP.bat "%USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.bat"

REM Create VBScript wrapper to run as EXE
echo [2/3] Creating VBScript wrapper...
(
echo Set objShell = CreateObject("WScript.Shell"^)
echo strPath = WScript.ScriptFullName
echo strFolder = objShell.CurrentDirectory
echo objShell.Run "cmd /c cd /d " ^& strFolder ^& " && ROBOTER_KI_APP.bat", 1, False
) > "%USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.vbs"

REM Create shortcut
echo [3/3] Creating shortcut...
(
echo [InternetShortcut]
echo URL=file:///%USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.bat
) > "%USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.url"

echo.
echo ========================================
echo ✅ INSTALLATION COMPLETE!
echo ========================================
echo.
echo 📍 Launcher: %USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.bat
echo 📍 VBScript: %USERPROFILE%\Desktop\Projekte\ROBOTER_KI_APP.vbs
echo.
pause
