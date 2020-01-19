# Itemet

Itemet is a flexible database to create linked markdown documents with YAML front matter.
This database represents any linked data in a format of documents.
All data can be imported and exported from or to
a CSV-file (using 'csvdoc' package).
Each document will be saved for further processing as a

+ '.md'-file and
+ '.json'-file

after editing via form show view.

A document or an item can have a state and a type.
All documents of the same type have
the same data points in the YAML front matter.
The type also defines the possible connections to other documents.
Further information can be found in './doc/'.

## Typical Usage

Because this software is (shall be) universal, you can use it how you want.
Potential applications are:

+ Resource Planning
+ Requirements Management

## Known Issues

+ Change of datetime format leads to errors


## Setup and Run

Setup a virtual environment and install dependencies:

```
make install
```

Run application:

```
make run
```

## Configure

Copy 'config.py' from 'app' directory to
the location where you want to store your data and make your changes.
Then provide the path to this configuration as an environment variable.

```
export ITEMET_CONFIG=/path/to/config.py
make install
```

```
export ITEMET_CONFIG=/path/to/config.py
make run
```

Please ensure that the paths in your own configuration
are relative to the execution path ('itemet')
or even better, use absolute paths.

Also make sure that you delete all your date before reinstallation.
