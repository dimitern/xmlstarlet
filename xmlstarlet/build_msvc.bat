@echo off

choco install -y -r tartool wget sed gawk

set XML2_URL=https://download.gnome.org/sources/libxml2/2.9/
set XSLT_URL=https://download.gnome.org/sources/libxslt/1.1/
set XML2_TARBALL=libxml2-2.9.1.tar.xz
set XSLT_TARBALL=libxslt-1.1.28.tar.xz

set PREFIX=C:\opt

if exist %PREFIX% rd /q /s %PREFIX%

if exist _build rd /q /s _build
md _build

rem Kill Git's link.exe which shadows MSVC's link.exe
if exist "C:\Program Files\Git\usr\bin\link.exe" del "C:\Program Files\Git\usr\bin\link.exe"
if exist "C:\Program Files (x86)\Git\usr\bin\link.exe" del "C:\Program Files (x86)\Git\usr\bin\link.exe"

echo Fetching sources for dependencies...
cd _build\

wget --output-document=%XML2_TARBALL% %XML2_URL%%XML2_TARBALL%
tar -xf %XML2_TARBALL%

wget --output-document=%XSLT_TARBALL% %XSLT_URL%%XSLT_TARBALL%
tar -xf %XSLT_TARBALL%

echo Building libxml2...
cd libxml2-2.9.1\win32

cscript configure.js debug=no static=yes compiler=msvc iconv=no python=no prefix=%PREFIX%

rem Patch the win32config.h / config.h to make it compatible with VS 2015+ (libxml2)
type ..\include\win32config.h | sed -e "s/#define snprintf _snprintf//g" > ..\include\win32config.h.patch
copy ..\include\win32config.h.patch ..\include\win32config.h
del ..\include\win32config.h.patch

type ..\config.h | sed -e "s/#define snprintf _snprintf//g" > ..\config.h.patch
copy ..\config.h.patch ..\config.h
del ..\config.h.patch

nmake all
nmake install
cd ..\..

echo Building libxslt...
cd libxslt-1.1.28\win32

cscript configure.js debug=no static=yes compiler=msvc iconv=no debugger=no include=%PREFIX%\include\libxml2 lib=%PREFIX%\lib prefix=%PREFIX%

rem Patch the win32config.h to make it compatible with VS 2015+ (libxslt)
type ..\libxslt\win32config.h | sed -e "s/#define snprintf _snprintf//g" > ..\libxslt\win32config.h.patch
copy ..\libxslt\win32config.h.patch ..\libxslt\win32config.h
del ..\libxslt\win32config.h.patch

rem Patch the Makefile to exclude unsupported /OPT:NOWIN98 link.exe option
type Makefile | sed -e "s/LDFLAGS = .*OPT:NOWIN98//g" > Makefile.patch
copy Makefile.patch Makefile
del Makefile.patch

nmake all
nmake install
cd ..\..\..

echo Building xmlstarlet...
cd xmlstarlet\win32\

cscript configure.js include=%PREFIX%\include\libxml2 prefix=%PREFIX% static=yes debug=no arch=%Platform%
nmake all
nmake install
cd ..\..
