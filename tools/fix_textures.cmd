@echo off
REM One-click repair for all item textures of kaleidoscope_snack.
REM Pipeline: 512px originals -> 16x16 sharp downscale for ALL items,
REM then a hand-crafted fix for cooked_sausage only (blunt top + wood
REM skewer). potato_chunks uses the plain sharp downscale (user's choice).
REM Run this whenever the textures folder was overwritten/restored.
REM Originals are backed up in hd_texture_backup\item (never delete that).

set PY=C:\Users\Ctoy\.workbuddy\binaries\python\envs\default\Scripts\python.exe
cd /d "%~dp0.."

echo [1/2] Downscaling all textures to 16x16 (sharp mode)...
"%PY%" tools\downscale_textures.py --mode sharp || goto :error

echo [2/2] Re-applying cooked_sausage fix...
"%PY%" .workbuddy\fix_sausage_top.py --apply || goto :error

echo.
echo Done. All textures repaired.
exit /b 0

:error
echo.
echo FAILED with error code %errorlevel%.
exit /b 1
