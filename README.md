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
/eunomia$ python -m shell.eis

Eis Interactive Shell - (C) Stijn Heymans, 2014
Type 'help' for an overview of commands. Ctrl-D exits.

(eis) load examples/path.lp
==> program loaded.

:: (command executed in 7.853031 ms)

(eis) show loaded
path(?x, ?y) :- edge(?x, ?y).
path(?x, ?z) :- edge(?x, ?y), path(?y, ?z).

(eis) add edge(a, b).
==> added  edge(a, b).  and updated known inferences.

(eis) show loaded
path(?x, ?y) :- edge(?x, ?y).
path(?x, ?z) :- edge(?x, ?y), path(?y, ?z).
edge(a, b).

(eis) build
Building model...
==> Model built (do 'show inferences' to see all known facts)

:: (command executed in 0.558138 ms)

(eis) show inferences
path(a, b)
edge(a, b)
==>  2 facts currently known.

(eis) add edge(b, c)
I'm not able to add  edge(b, c)  Is it a well-formed fact or rule?
Details:  Syntax error in input: None

(eis) add edge(b, c).

:: (command executed in 0.552177 ms)
==> added  edge(b, c).  and updated known inferences.

(eis) show inferences
edge(b, c)
path(a, c)
edge(a, b)
path(a, b)
path(b, c)
==>  5 facts currently known.
(eis) 
```

