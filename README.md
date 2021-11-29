This is a simple Python script for tournament games

Getting Started
---------------

In short, you can play your tournament game by 1) write down the description of
your tournament in a file, and 2) repeatedly runs `./tournament.py run` and
select winners until the tournament completes.  For example:

    $ echo "
    what is the best programming language?

    c
    c++
    python
    java
    javascript
    go
    rust" > description
    $ ./tournament.py run
    what is the best programming language?
    1. javascript
    2. rust
    Please select: 2

    current status:
    what is the best programming language?
    candidates: javascript, rust, python, java, c++, go, c, None
    0 round (4 matches)
    javascript vs rust (winner: rust)
    python vs java (winner: not decided yet)
    c++ vs go (winner: not decided yet)
    c vs None (winner: not decided yet)

    $ ./tournament.py run
    what is the best programming language?
    1. python
    2. java
    Please select: 1

    current status:
    what is the best programming language?
    candidates: python, c, c++, java, javascript, go, rust
    0 round (4 matches)
    javascript vs rust (winner: rust)
    python vs java (winner: python)
    c++ vs go (winner: not decided yet)
    c vs None (winner: not decided yet)


Description File
----------------

You should write down a description of the tournament in a file.  The first
line of the file should be the title of the tournament (e.g., what is the best
noodle?).  Then, players of the tournament should come one by one in each line.
Empty lines and comment lines that starts with `#` are allowed.

`tournament.py` assumes the path to the file would be `./description`.  If
that's not your case, you can specify the path to your description file via
`--description` option.


Show Status
-----------

You can show the current status of the tournament by passing `status` instead
of `run` to `tournament.py`.  For example:

    $ ./tournament.py status
    what is the best programming language?
    candidates: python, c, c++, java, javascript, go, rust
    0 round (4 matches)
    javascript vs rust (winner: rust)
    python vs java (winner: python)
    c++ vs go (winner: not decided yet)
    c vs None (winner: not decided yet)
