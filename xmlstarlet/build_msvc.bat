@echo off

set PREFIX=C:\opt

echo Building xmlstarlet...
cd xmlstarlet\win32\

cscript configure.js include=%PREFIX%\include\libxml2 prefix=%PREFIX% static=yes debug=no arch=%Platform%
nmake all
nmake install
cd ..\..
