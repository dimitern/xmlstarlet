@echo off

cd ..\src

gawk -f ..\usage2c.awk usage.txt > usage.c
gawk -f ..\usage2c.awk c14n-usage.txt > c14n-usage.c
gawk -f ..\usage2c.awk depyx-usage.txt > depyx-usage.c
gawk -f ..\usage2c.awk edit-usage.txt > edit-usage.c
gawk -f ..\usage2c.awk elem-usage.txt > elem-usage.c
gawk -f ..\usage2c.awk escape-usage.txt > escape-usage.c
gawk -f ..\usage2c.awk format-usage.txt > format-usage.c
gawk -f ..\usage2c.awk pyx-usage.txt > pyx-usage.c
gawk -f ..\usage2c.awk select-usage.txt > select-usage.c
gawk -f ..\usage2c.awk trans-usage.txt > trans-usage.c
gawk -f ..\usage2c.awk unescape-usage.txt > unescape-usage.c
gawk -f ..\usage2c.awk validate-usage.txt > validate-usage.c

cd ..\win32