eunomia
=========

[![Build Status](https://travis-ci.org/sheymans/eunomia.svg)](https://travis-ci.org/sheymans/eunomia)
[![Coverage Status](https://coveralls.io/repos/sheymans/eunomia/badge.png)](https://coveralls.io/r/sheymans/eunomia)

# What is this?

This is a lightweight Datalog reasoner (pure Datalog, no extensions). Some characteristics:

- Bottom-up computation only, so mainly geared toward computing the complete
  minimal model.

- Heavily indexed data structures using lots of space for fast unification and
  resolution. The purpose being fast execution times rather than optimal space usage.

- Incremental reasoning. Once you've build a minimal model any subsequent
  additions of adding rules and facts will update the existing minimal model
  in an incremental way (no calculation from scratch).

This is in full development so I do not consider this ready for production. If
you find bugs, please submit an issue.

# Example Run

```
eunomia$ python -m shell.eis
Eunomia Interactive Shell - (C) Stijn Heymans, 2014
Type 'help' for an overview of commands. Ctrl-D exits.

(eis) load examples/path.lp
==> program loaded.

:: (command executed in 8.091927 ms)

(eis) show loaded
path(?x, ?y) :- edge(?x, ?y).
path(?x, ?z) :- edge(?x, ?y), path(?y, ?z).

(eis) add edge(a, b).
==> added  
edge(a, b).  and updated known inferences.

(eis) show inferences
You did not ask to deduce what I know. Try 'build'.

(eis) build
Building model...
==> Model built (do 'show inferences' to see all known facts)

:: (command executed in 0.565052 ms)

(eis) show inferences
path(a, b)
edge(a, b)
==>  2 facts currently known.

(eis) query path(a, ?x).
path(a, b)
==>  1 facts match query  path(a, ?x)

:: (command executed in 0.092983 ms)

(eis) add edge(b, b).

:: (command executed in 0.483990 ms)
==> added  
edge(b, b).  and updated known inferences.

(eis) query path(?x, ?x).
path(b, b)
==>  1 facts match query  path(?x, ?x)

:: (command executed in 0.113010 ms)

```

