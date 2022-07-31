@echo off

set PREFIX=C:\opt

if exist "C:\Program Files\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvarsall.bat" call "C:\Program Files\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvarsall.bat"
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvarsall.bat" call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvarsall.bat"

echo Building xmlstarlet...
cd xmlstarlet\win32\

cscript configure.js include=%PREFIX%\include\libxml2 prefix=%PREFIX% static=yes debug=no arch=%Platform%
nmake all
nmake install
cd ..\..
