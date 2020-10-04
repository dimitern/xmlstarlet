@echo off

choco install -y -r tartool wget sed gawk

set BASE_URL=ftp://xmlsoft.org/libxml2/
set XML2_TARBALL=libxml2-2.9.3.tar.gz
set XSLT_TARBALL=libxslt-1.1.28.tar.gz

set PREFIX=C:\opt

if exist %PREFIX% rd /q /s %PREFIX%

if exist _build rd /q /s _build
md _build

echo Fetching sources for dependencies...
cd _build\

wget --output-document=%XML2_TARBALL% %BASE_URL%%XML2_TARBALL%
tar -xf %XML2_TARBALL%

wget --output-document=%XSLT_TARBALL% %BASE_URL%%XSLT_TARBALL%
tar -xf %XSLT_TARBALL%

echo Building libxml2...
cd libxml2-2.9.3\win32
cscript configure.js debug=no static=yes compiler=msvc iconv=no python=no  prefix=%PREFIX%
nmake all
nmake install
cd ..\..

echo Building libxslt...
cd libxslt-1.1.28\win32
cscript configure.js debug=no static=yes compiler=msvc iconv=no debugger=no include=%PREFIX%\include\libxml2 lib=%PREFIX%\lib prefix=%PREFIX%

rem Patch the win32config.h to make it compatible with VS 2015+
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

cscript configure.js include=%PREFIX%\include\libxml2 prefix=%PREFIX% static=yes debug=no
nmake all
nmake install
cd ..\..
