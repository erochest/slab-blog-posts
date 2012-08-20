
I regularly have to perform a small, regular edit on a collection of files.
I imagine that if you work with computers long enough, that will be something
everyone has to do.

For this task, I usually reach for a scripting language. But often the edit is
so small that even doing this seems like overkill. Or maybe the edit is just
the wrong kind of complexity to capture easily with code. My fingers may be
able to make the change quickly and repetitively, but when I try to break down
how a script would do it, I get a headache.

Over the years, I've been confronted with this often enough that I've developed
a well-tested approach to this using [Vim][vim]. It's become one of those tools
that I don't really think about much. I just use it from time to time, and it
makes my life easier.

But earlier this week, when [Jeremy][clioweb] mentioned that he had a small
change to make to a series of files in the [NeatlineMaps][nlmaps]. Usually, he
switches to TextMate for tasks like this, but he agreed that to let me show him
how to do it in Vim.

Heh. Whenever I try to explain to someone how to do something in Vim,
I invariably sound like, "Then his *escape*, *4h*, *0*, *o*." It's kind of
funny, but it's not a lot of fun, either for me or for the person I'm reciting
keystrokes for.

But it is useful information, and it would definitely be a better blog post
than a conversation.

So here's what we did:

# The Problem

Jeremy had tried to put some Vim [mode lines][modelines] at the top of the
files. These are comments at the top of a file for setting options in Vim.
Currently, they look [like this][nlmapmode]:

```vim
/* vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4: */
```

But they weren't working. It turned out that he the colon near the end of the
line was actually a semicolon, and once that was fixed, the settings worked
fine. But at that point he needed to make that change on almost every file in
NeatlineMaps.

The process has three parts, really. Let's break them down.

# `:args`

First, we have to get the files to process. When you open Vim from the
command-line and pass in files there, the file names are stored in the argument
list. You can access the argument list inside Vim---either to set the files it
contains or to see what it says---using the `:args` command:

```vim
:args NealtineMaps/**/*.php
```

This searches for all the files in the `NeatlineMaps` directory and
subdirectories that have a `.php` extension. These files are loaded into the
argument list.

Now that they're there, we can navigate over the list using some simple
commands:

* `:rewind` Rewinds to the beginning of the list.
* `:next` Moves to the next file in the list.
* `:Next` Moves to the previous file in the list.
* `:previous` Also moves to the previous file in the list.
* `:last` Moves to the last file in the list.

They can all also be abbreviated. So for example, you can use `:n` and `:N` to
move forward and backward.

# `q`

Looking at the first file, now we make the change that we want to make on all
files. But before we do, we first start recording our keystrokes into a buffer.
For this we chose the *t* buffer. There's no reason for that particular buffer:
It was just the first letter I thought of:

```vim
qt
```

Now the bottom of the Vim screen said `recording`. At this point, we can go
ahead and make the edit.

# `:s/../../e`

What I had Jeremy do was slightly more complicated, but basically, I had him do
this:

```vim
:%s/softtabstop=4;/softtabstop=4:/e
```

This looked at the whole file (`%`) and performed a search-and-replace (`s`).
It looked for the string *softtabstop=4;* and replaced it with the same string,
except it used a colon (*softtabstop=4:*). The `e` at the end just meant that
it should ignore errors and keep chugging.

Once we've made the change, let's save it and move to the next file.

```vim
:wn
```

This combines the *w*rite command and the *n*ext command (from above).

That's what we want to save. Now hit *q* to stop recording:

```vim
q
```

You can replay that now by pressing `@t`. Jeremy and I did that a few times to
make sure it was doing what we wanted and wasn't chewing up the files.

# *n*`@`

Once we felt that everything was safe, we moved on to working on the rest of
the files. Most commands in Vim can take a number before, which tells how many
times to perform the command. For example, *j* moves down one line, and *10j*
moves down 10 lines.

In this case, we told it to play the recorded keystrokes 100 times:

```vim
100@t
```

And Vim went to work. It stopped on the first error, which happened when
`:next` reached the last file in the argument list and wasn't able to move to
the next file.

# Solved

And that's it. It seems more complicated than it actually is, and once you've
been through it a few times, you can do this very quickly. Vim's ability to
record and replay keystrokes, combined with its commands to navigate in and
across files, make an incredibly powerful combination.


[clioweb]: https://twitter.com/clioweb "Jeremy Boggs"
[nlmaps]: https://github.com/scholarslab/NeatlineMaps "NeatlineMaps"
[vim]: http://www.vim.org/ "Vim"
[modelines]: http://vim.wikia.com/wiki/Modeline_magic "Modeline magic"
[nlmapmode]: https://github.com/scholarslab/NeatlineMaps/blob/master/NeatlineMapsPlugin.php#L2
[args]: http://vimdoc.sourceforge.net/htmldoc/editing.html#:args
[q]: http://vimdoc.sourceforge.net/htmldoc/repeat.html#q
[s]: http://vimdoc.sourceforge.net/htmldoc/change.html#:s

