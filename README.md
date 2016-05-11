pytools
=============
Useful generic python scripts for working with log files from the command line.

The base directory contains many of the most useful scripts. Most are pretty self documenting. The subdirectories contain more domain specific scripts for performing tasks relevant to those domains. I still actively contribute scripts, so expect to see more.

Examples:
* To create a empirical cummulative distribution function from column X (zero-based indexing) in a log file:
```
	<file ./ecdf.py -c X
```
* You can filter the log file to only the rows where column Y matches a criteria with:
```
	<file ./where.py -n "c[Y] > 100 or c[Y] == 1" | ./ecdf.py -c X
```
* Most of the scripts support grouping. This command will count the unique entries in column X per group in column Y:
```
	<file ./unique.py -g Y -c X
```
* The result can then be piped to determine what fraction of the total each group represents:
```
	<file ./unique.py -g Y -c X | ./fraction.py -a -c 1
```
* To compute the 5th, median, and 95th percentiles per group in the log, you could use:
```
	<file ./percentile.py -g Y -c X -p 0.05 0.5 0.95
```
* Not satisfied with just numbers? Plot the data with:
```
	<file ./mode.py -g Y -c X | ./plot/plot.py --geom line --mapping x=0 y=1
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

