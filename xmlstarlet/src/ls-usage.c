#include <stdio.h>
#include <libxml/xmlversion.h>
static const char ls_usage[] = {
'X','M','L','S','t','a','r','l','e','t',' ','T','o','o','l','k','i','t',':',' ','L','i','s','t',' ','d','i','r','e','c','t','o','r','y',' ','a','s',' ','X','M','L','\n',
'U','s','a','g','e',':',' ','%','s',' ','l','s',' ','[',' ','<','d','i','r','>',' ','|',' ','-','-','h','e','l','p',' ',']','\n',
'L','i','s','t','s',' ','c','u','r','r','e','n','t',' ','d','i','r','e','c','t','o','r','y',' ','i','n',' ','X','M','L',' ','f','o','r','m','a','t','.','\n',
'T','i','m','e',' ','i','s',' ','s','h','o','w','n',' ','p','e','r',' ','I','S','O',' ','8','6','0','1',' ','s','p','e','c','.','\n',
'\n',
0 };
void fprint_ls_usage(FILE* out, const char* argv0) {
  fprintf(out, ls_usage, argv0);
}
