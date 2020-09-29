/* Configure script for xmlstarlet, specific for Windows with Scripting Host.
 * 
 * Based on configure.js script by Igor Zlatkovic used in libxslt\win32.
 *
 * This script will configure the xmlstarlet build process and create necessary files.
 * Run it with an 'help', or an invalid option and it will tell you what options
 * it accepts.
 *
 * March 2002, Igor Zlatkovic <igor@zlatkovic.com>
 * October 2020,  Dimiter Naydenov <dimiter@naydenov.net>
 */

/* The source directory, relative to the one where this file resides. */
var baseDir = "..";
var srcDir = baseDir + "\\src";
/* The directory where we put the binaries after compilation. */
var binDir = "binaries";
/* Base name of what we are building. */
var baseName = "xmlstarlet";
/* Configure file which contains the version and the output file where
   we can store our build configuration. */
var configFile = baseDir + "\\configure.ac";
var versionFile = ".\\config.msvc";
/* Settings for the binary distribution. Will be filled later 
   in the code. */
var packageBugReport;
var packageName;
var packageString;
var packageTarName;
var packageUrl;
var packageVersion;
/* Xmlstarlet features. */
var withIconv = false;
var withZlib = false;
/* Win32 build options. */
var dirSep = "\\";
var compiler = "msvc";
var cruntime = "/MD";
var vcmanifest = false;
var buildDebug = 0;
var buildStatic = true;
var buildPrefix = ".";
var buildBinPrefix = "";
var buildIncPrefix = "";
var buildLibPrefix = "";
var buildSoPrefix = "";
var buildInclude = ".";
var buildLib = ".";
/* Local stuff */
var error = 0;

/* Helper function, transforms the option variable into the 'Enabled'
   or 'Disabled' string. */
function boolToStr(opt)
{
	if (opt == false)
		return "no";
	else if (opt == true)
		return "yes";
	error = 1;
	return "*** undefined ***";
}

/* Helper function, transforms the argument string into the boolean
   value. */
function strToBool(opt)
{
	if (opt == "0" || opt == "no")
		return false;
	else if (opt == "1" || opt == "yes")
		return true;
	error = 1;
	return false;
}

/* Displays the details about how to use this script. */
function usage()
{
	var txt;
	txt = "Usage:\n";
	txt += "  cscript " + WScript.ScriptName + " <options>\n";
	txt += "  cscript " + WScript.ScriptName + " help\n\n";
	txt += "Options can be specified in the form <option>=<value>, where the value is\n";
	txt += "either 'yes' or 'no'.\n\n";
	txt += "xmlstarlet processor options, default value given in parentheses:\n\n";
	txt += "  iconv:      Use iconv library (" + (withIconv? "yes" : "no")  + ")\n";
	txt += "  zlib:       Use zlib library (" + (withZlib? "yes" : "no") + ")\n";
	txt += "\nWin32 build options, default value given in parentheses:\n\n";
	txt += "  compiler:   Compiler to be used [msvc] (" + compiler + ")\n";
	txt += "  cruntime:   C-runtime compiler option (only msvc) (" + cruntime + ")\n";
	txt += "  vcmanifest: Embed VC manifest (only msvc) (" + (vcmanifest? "yes" : "no") + ")\n";
	txt += "  debug:      Build unoptimised debug executables (" + (buildDebug? "yes" : "no")  + ")\n";
	txt += "  static:     Link xmlstarlet statically to libxml2, libxslt (" + (buildStatic? "yes" : "no")  + ")\n";
	txt += "              Note: automatically enabled if cruntime is not /MD or /MDd\n";
	txt += "  prefix:     Base directory for the installation (" + buildPrefix + ")\n";
	txt += "  bindir:     Directory where xml.exe should be installed\n";
	txt += "              (" + buildBinPrefix + ")\n";
	txt += "  incdir:     Directory where headers should be installed\n";
	txt += "              (" + buildIncPrefix + ")\n";
	txt += "  libdir:     Directory where static and import libraries should be\n";
	txt += "              installed (" + buildLibPrefix + ")\n";
	txt += "  sodir:      Directory where shared libraries should be installed\n"; 
	txt += "              (" + buildSoPrefix + ")\n";
	txt += "  include:    Additional search path for the compiler, particularily\n";
	txt += "              where libxml / libxslt headers can be found (" + buildInclude + ")\n";
	txt += "  lib:        Additional search path for the linker, particularily\n";
	txt += "              where libxml / libxslt libraries can be found (" + buildLib + ")\n";
	WScript.Echo(txt);
}

/* Discovers the version we are working with by reading the appropriate
   configuration file. Despite its name, this also writes the configuration
   file included by our makefile. */
function discoverVersion()
{
	var fso, cf, vf, ln, s;
	fso = new ActiveXObject("Scripting.FileSystemObject");
	cf = fso.OpenTextFile(configFile, 1);
	if (compiler == "msvc")
		versionFile = ".\\config.msvc";
	vf = fso.CreateTextFile(versionFile, true);
	vf.WriteLine("# " + versionFile);
	vf.WriteLine("# This file is generated automatically by " + WScript.ScriptName + ".");
	vf.WriteBlankLines(1);
	while (cf.AtEndOfStream != true) {
		ln = cf.ReadLine();
		s = new String(ln);
		if (s.search(/^AC_INIT\(\[/) != -1) {
			packageName = s.substring(s.indexOf("[") + 1, s.length);
			packageName = packageName.substring(0, packageName.indexOf("]"));
			packageTarName = packageName.toLowerCase();
			packageVersion = "v1.6.1";
			packageString = packageName + " " + packageVersion;
			vf.WriteLine("PACKAGE_NAME=" + packageName);
			vf.WriteLine("PACKAGE_VERSION=" + packageVersion);
			vf.WriteLine("PACKAGE_STRING=" + packageString);
			vf.WriteLine("PACKAGE_TARNAME=" + packageTarName);
		} else if(s.search(/^\s*\[http:\/\/sourceforge\./) != -1) {
			packageBugReport = s.substring(s.indexOf("[") + 1, s.length);
			packageBugReport = packageBugReport.substring(0, packageBugReport.indexOf("]"));
			vf.WriteLine("PACKAGE_BUGREPORT=" + packageBugReport);
		} else if(s.search(/^\s*\[http:\/\/xmlstar\./) != -1) {
			packageUrl = s.substring(s.indexOf("[") + 1, s.length);
			packageUrl = packageUrl.substring(0, packageUrl.indexOf("]"));
			vf.WriteLine("PACKAGE_URL=" + packageUrl);
		}
	}
	cf.Close();
	vf.WriteLine("WITH_ICONV=" + (withIconv? "1" : "0"));
	vf.WriteLine("WITH_ZLIB=" + (withZlib? "1" : "0"));
	vf.WriteLine("DEBUG=" + (buildDebug? "1" : "0"));
	vf.WriteLine("STATIC=" + (buildStatic? "1" : "0"));
	vf.WriteLine("PREFIX=" + buildPrefix);
	vf.WriteLine("BINPREFIX=" + buildBinPrefix);
	vf.WriteLine("INCPREFIX=" + buildIncPrefix);
	vf.WriteLine("LIBPREFIX=" + buildLibPrefix);
	vf.WriteLine("SOPREFIX=" + buildSoPrefix);
	if (compiler == "msvc") {
		vf.WriteLine("INCLUDE=$(INCLUDE);" + buildInclude);
		vf.WriteLine("LIB=$(LIB);" + buildLib);
		vf.WriteLine("CRUNTIME=" + cruntime);
		vf.WriteLine("VCMANIFEST=" + (vcmanifest? "1" : "0"));
	}
	vf.Close();
}

/*
 * main(),
 * Execution begins here.
 */

/* Parse the command-line arguments. */
for (i = 0; (i < WScript.Arguments.length) && (error == 0); i++) {
	var arg, opt;
	arg = WScript.Arguments(i);
	opt = arg.substring(0, arg.indexOf("="));
	if (opt.length == 0)
		opt = arg.substring(0, arg.indexOf(":"));
	if (opt.length > 0) {
		if (opt == "debug")
			buildDebug = strToBool(arg.substring(opt.length + 1, arg.length));
		else if (opt == "iconv")
			withIconv = strToBool(arg.substring(opt.length + 1, arg.length));
		else if (opt == "zlib")
			withZlib  = strToBool(arg.substring(opt.length + 1, arg.length));
		else if (opt == "compiler")
			compiler = arg.substring(opt.length + 1, arg.length);
 		else if (opt == "cruntime")
 			cruntime = arg.substring(opt.length + 1, arg.length);
		else if (opt == "vcmanifest")
			vcmanifest = strToBool(arg.substring(opt.length + 1, arg.length));
		else if (opt == "static")
			buildStatic = strToBool(arg.substring(opt.length + 1, arg.length));
		else if (opt == "prefix")
			buildPrefix = arg.substring(opt.length + 1, arg.length);
		else if (opt == "incdir")
			buildIncPrefix = arg.substring(opt.length + 1, arg.length);
		else if (opt == "bindir")
			buildBinPrefix = arg.substring(opt.length + 1, arg.length);
		else if (opt == "libdir")
			buildLibPrefix = arg.substring(opt.length + 1, arg.length);
		else if (opt == "sodir")
			buildSoPrefix = arg.substring(opt.length + 1, arg.length);
		else if (opt == "incdir")
			buildIncPrefix = arg.substring(opt.length + 1, arg.length);
		else if (opt == "include")
			buildInclude = arg.substring(opt.length + 1, arg.length);
		else if (opt == "lib")
			buildLib = arg.substring(opt.length + 1, arg.length);
		else
			error = 1;
	} else if (i == 0) {
        if (arg == "help") {
			usage();
			WScript.Quit(0);
		}
	} else
		error = 1;
}
// If we have an error here, it is because the user supplied bad parameters.
if (error != 0) {
	usage();
	WScript.Quit(error);
}

// if user choses to link the c-runtime library statically into xmlstarlet
// with /MT and friends, then we need to enable static linking for xmlstarlet
if (cruntime == "/MT" || cruntime == "/MTd" ||
		cruntime == "/ML" || cruntime == "/MLd") {
	buildStatic = 1;
}

dirSep = "\\";
//if (compiler == "mingw")
//	dirSep = "/";
if (buildBinPrefix == "")
	buildBinPrefix = "$(PREFIX)" + dirSep + "bin";
if (buildIncPrefix == "")
	buildIncPrefix = "$(PREFIX)" + dirSep + "include";
if (buildLibPrefix == "")
	buildLibPrefix = "$(PREFIX)" + dirSep + "lib";
if (buildSoPrefix == "")
	buildSoPrefix = "$(PREFIX)" + dirSep + "lib";

// Discover the version.
discoverVersion();
if (error != 0) {
	WScript.Echo("Version discovery failed, aborting.");
	WScript.Quit(error);
}

WScript.Echo(packageString);

// Create the Makefile.
var fso = new ActiveXObject("Scripting.FileSystemObject");
var makefile = ".\\Makefile.msvc";
fso.CopyFile(makefile, ".\\Makefile", true);
WScript.Echo("Created Makefile.");
// Create the config.h.
var confighsrc = ".\\win32config.h";
var configh = "..\\config.h";
var f = fso.FileExists(configh);
if (f) {
	var t = fso.GetFile(configh);
	t.Attributes =0;
}
fso.CopyFile(confighsrc, configh, true);
WScript.Echo("Created config.h.");

fso.CopyFile(".\\win32_xml_ls.c", srcDir + "\\win32_xml_ls.c", true);
WScript.Echo("Created win32_xml_ls.c.");

vf = fso.CreateTextFile(baseDir + "\\version.h", true);
vf.WriteLine("#define VERSION \"" + packageString + "\"");
vf.Close();
WScript.Echo("Created version.h.");

// Display the final configuration.
var txtOut = "\nxmlstarlet configuration\n";
txtOut += "----------------------------\n";
txtOut += "         Use iconv: " + boolToStr(withIconv) + "\n";
txtOut += "         With zlib: " + boolToStr(withZlib) + "\n";
txtOut += "\n";
txtOut += "Win32 build configuration\n";
txtOut += "-------------------------\n";
txtOut += "          Compiler: " + compiler + "\n";
if (compiler == "msvc")
	txtOut += "  C-Runtime option: " + cruntime + "\n";
	txtOut += "    Embed Manifest: " + boolToStr(vcmanifest) + "\n";
txtOut += "     Debug symbols: " + boolToStr(buildDebug) + "\n";
txtOut += "      Static build: " + boolToStr(buildStatic) + "\n";
txtOut += "    Install prefix: " + buildPrefix + "\n";
txtOut += "      Put tools in: " + buildBinPrefix + "\n";
txtOut += "    Put headers in: " + buildIncPrefix + "\n";
txtOut += "Put static libs in: " + buildLibPrefix + "\n";
txtOut += "Put shared libs in: " + buildSoPrefix + "\n";
txtOut += "      Include path: " + buildInclude + "\n";
txtOut += "          Lib path: " + buildLib + "\n";
WScript.Echo(txtOut);

// Done.
