/* Special Windows-specific variant of xml_ls.c used
 * instead of the original, because `ls` and related
 * Unix-specific headers (dirent.h, unistd.h, etc.)
 * are not available.
 *
 * Author: Dimiter Naydenov
 */

#include <config.h>
#include <stdio.h>
#include "xmlstar.h"

void lsUsage(int argc, char **argv, exit_status status)
{
    FILE *o = (status == EXIT_SUCCESS)? stdout : stderr;
	fprintf(o,  "ls is not supported on Windows");
    exit(status);
}

int lsMain(int argc, char **argv) {
	printf("ls is not supported on Windows");
	return 1;
}
