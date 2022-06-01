data_tools
=============
Useful generic python scripts for working with text files from the command line.

Working from the command line is the easiest way to explore a new dataset of text files, such as logs. However, many tasks require 
more advanced tools than are commonly available. So, I wrote a bunch of python scripts for exploring data to complement the standard command-line utilities. 
The scripts vary from general (e.g., binning log lines by a common column value or values) to domain specific (e.g., 
computing the stack distance between values in the file).

The repository installs both a library and a series of scripts. Most are pretty self documenting. I still actively contribute scripts, so expect to see more.

Examples:
* To create a empirical cummulative distribution function from column X (zero-based indexing) in a log file:
```
	<file ecdf.py -c X
```
* You can filter the log file to only the rows where column Y matches a criteria with:
```
	<file dt_where -n -e "c[Y] > 100 or c[Y] == 1" | dt_ecdf -c X
```
* Most of the scripts support grouping. This command will count the unique entries in column X per group in column Y:
```
	<file dt_unique -g Y -c X
```
* The result can then be piped to determine what fraction of the total each group represents:
```
	<file dt_unique -g Y -c X | dt_fraction -a -c 1
```
* To compute the 5th, median, and 95th percentiles per group in the log, you could use:
```
	<file dt_percentile -g Y -c X -p 0.05 0.5 0.95
```
* Not satisfied with just numbers? Plot the data with:
```
	<file dt_mode -g Y -c X | dt_plot --geom line --mapping x=0 y=1
```

Additionally, log headers are supported with the --header option. If the option is provided, then column names may be specified instead of indices.
A file with header looks like this:
```
	column_one column_two column_three
	1          2          Value
	2          3          Value2
	...
```
The delimiter between columns defaults to whitespace, but can be modified with the --delimiter option. 

Header and delimiter may also be specified with environment variables:
```
	TOOLBOX_DELIMITER=,
	TOOLBOX_HEADER=true
```

There are many more options and combinations of scripts to perform a wide variety of tasks.

