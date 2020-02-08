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
For screenshots please navigate to './doc/assets/'.

## Typical Usage

Because this software is (shall be) universal, you can use it how you want.
Potential applications are:

+ Resource Planning
+ Requirements Management
+ Document Management System (very limited)
+ Office Automation (via additional apps through plugin interface)

## Important Hints

This program is not tested in relation to cyber security.
So it's highly recommended to use it only in secure networks.

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

Copy 'config.json' from 'app' directory to
the location where you want to store your data and make your changes.
The paths in 'config.json' have to be relative to the location of the file.
Finally you have to provide the path to your 'config.json'
as an environment variable.

```
export ITEMET_CONFIG=/path/to/config.json
make install
```

```
export ITEMET_CONFIG=/path/to/config.json
make run
```
