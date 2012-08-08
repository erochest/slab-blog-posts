<div style="float:right;"><a href="http://www.flickr.com/photos/wwarby/3297205226/" title="Stopwatch by wwarby, on Flickr"><img src="http://farm4.staticflickr.com/3443/3297205226_a12b175d49_n.jpg" width="320" height="240" alt="Stopwatch"></a></div>
One of the fundamental tensions in programming is balancing the program's
requirements for time (programmer time and running time) against its space
requirements (disk space and memory space). Optimizing---looking for ways to
shift that balance, usually to have the program run faster---is a common task.

Recently, I've had to speed up requests on a couple of different websites I've
worked on: [Neatline][neatline] and a small, personal work-in-progress I call
[What is DH?][whatisdh].

Of course, optimizing programs too early can turn your program into an
unreadable mess and waste your time to boot. ([The Wikipedia page on Program
Optmization][progopt] has a good overview of the issues and trade-offs.) The
rule is: in general, don't optimize. But if you need to, do it right. That's
where this post comes in.

# Lather, Rinse, Repeat

A typical work flow when optimizing a program goes something like this:

1. Measure how long it takes or now much memory it takes right now.
2. If it's good enough, stop; otherwise, keep going.
3. Change something.
4. Go back to #1.

That seems simple enough, but it's really quite complicated. For example, in a
web app, many things could be making a request slow:

* One slow database query.
* Too many database queries.
* Pulling in too much unused data from the database.
* One intensive computation.
* A bunch of small computations.

I'm leaving out maybe one or two things, but you get the idea.

The timings are also complicated by a number of factors:

* The interpreter needs to allocate a bunch of memory (instead of using
  pre-allocated memory), which is relatively slow.
* The interpreter executing your program could decide to [take out the
  garbage][gc] during the run, effectively tying up your program.
* Your computer/OS may suddenly decide that it has to do some intensive
  computation *right now*, 'cause, well, you know, computers are helpful like
  that.
* A bunch of small tasks may start up, creating a smaller performance hit.

You have no control over any of this, and they will all throw off the timings.
Generally, I've learned to take a number of measurements (3--5, say), and take
the *lowest*. Not the average. The lowest will be the time of the processing,
with the least about of other things interfering.

# You're Wrong!

There's one complication I haven't mentioned yet. The biggest problem with
optimizing code is this.

> Your intuitions about what is so slow are **wrong**.

Maybe not always, but often enough that you shouldn't trust them.

Or to put it another way:

> "Bottlenecks occur in surprising places, so don't try to second guess and put
> in a speed hack until you have proven that's where the bottleneck is." ---
> Rob Pike

(And to be fair, the tool I'm getting ready to describe, timr, doesn't help you
identify which part of your code is taking so much time, but it will tell you
whether what you changed helped or not.)

# My Kingdom for Some Data

Because you're going to be wrong, optimization is largely a data-driven task.
What data, you ask?

1. Multiple timings for each small change you make. You probably only want to
   look at each group of timings in aggregate, however.
2. The return value of each web request. Whatever you changes you make, you
   probably don't want this to change.

*Data* is just another word for *lots and lots of bookkeeping*, which is
another way of saying *boring and error-prone*. Often, software developers hate
*boring and error-prone*, and I'm no exception. As I was working on optimizing
an AJAX call in Neatline, I created a small script to help me keep track of the
data I was accumulating. I call this [timr][timr], because leaving out vowels
is always a good idea.

# Installing

timr requires Python, and if you have [Python][python] and [Pip][pip], you can
install it with:

```bash
pip install timr
```

# Using

timr is a command-line tool, and once it's installed, using it is pretty
straight-forward (I hope).

## Configuration Files

Generally, the easiest way to use it is to gather all the command-line
arguments for a project into an ad hoc configuration file.

For example, save this as `fetch.conf`. It will time a POST request with my
name, and it will send the output to `fetch-output.csv`:

    --method
    POST
    --url
    http://whatever.com/resource/
    --header
    Accept: application/json
    --data
    first_name=Eric
    --data
    surname=Rochester
    --output
    fetch-output.csv

> *NB: Ignore the extra lines around the URL. For some reason, WordPress adds
> those in, but they shouldn't be there.*

These won't change between runs, so this provides both consistency and
documentation.

## Fetch

Now, call `timr fetch` with the arguments from the configuration file, plus the
message that you want attached to the timing group (in this case, "initial
timings").

```bash
timr fetch @fetch.conf -m "initial timings"
```

This executes the POST request multiple times (4 times, by default) and write
the resulting times out to a CSV file.

## Report

Looking at the raw output isn't that helpful, however. Instead, you want to
aggregate the timing sessions.

Most of the time, I just dump the aggregate data out to the screen:

```bash
timr report --input=fetch-output.csv
```

But sometimes I want a pretty chart or graph. Timr doesn't do visualizations,
but you can send the CSV to a file. This way you could pull it into Excel or
something that does do visualizations.

```bash
timr report --input=fetch-output.csv --output=report-output.csv
```

That's really all there is to it.

## E.G.

For example, let's see how fast a Google search for "timr" is over a couple of sessions.

First, we'll create a configuration file named `google.conf`:

    --method
    GET
    --url
    http://www.google.com
    --data
    q=timr
    --output
    google-timr.csv

Now run it a couple of times:

```bash
timr fetch @google.conf -m "initial search"
timr fetch @google.conf -m "another session"
```

> *This doesn't actually pull up the search results. Instead, it goes to the
> page that looks like it should have results, but only has the search
> suggestion drop-down at the top of the page. I'm not going to worry about
> that right now. After all, trying to optimize Google search results isn't
> very useful unless you work at Google.*

Let's see what this outputs:

<div style="width: 100%; overflow-x: scroll; overflow-y: hidden; white-space: nowrap;"><div style="width: 1200px;"><pre><code>
2012-08-07 10:13:08.871731,03a227c0-e09a-11e1-ad5b-c82a1417b0e9,initial search,02a0f14a92b4e0070ee17275f1d78c3a7db1ba68,955,0.141083955765
2012-08-07 10:13:08.871731,03a227c0-e09a-11e1-ad5b-c82a1417b0e9,initial search,02a0f14a92b4e0070ee17275f1d78c3a7db1ba68,955,0.0433859825134
2012-08-07 10:13:08.871731,03a227c0-e09a-11e1-ad5b-c82a1417b0e9,initial search,02a0f14a92b4e0070ee17275f1d78c3a7db1ba68,955,0.0436539649963
2012-08-07 10:13:08.871731,03a227c0-e09a-11e1-ad5b-c82a1417b0e9,initial search,02a0f14a92b4e0070ee17275f1d78c3a7db1ba68,955,0.044303894043
2012-08-07 10:14:03.237169,240e6f5c-e09a-11e1-962c-c82a1417b0e9,another session,02a0f14a92b4e0070ee17275f1d78c3a7db1ba68,955,0.389742851257
2012-08-07 10:14:03.237169,240e6f5c-e09a-11e1-962c-c82a1417b0e9,another session,02a0f14a92b4e0070ee17275f1d78c3a7db1ba68,955,0.0447700023651
2012-08-07 10:14:03.237169,240e6f5c-e09a-11e1-962c-c82a1417b0e9,another session,02a0f14a92b4e0070ee17275f1d78c3a7db1ba68,955,0.0436999797821
2012-08-07 10:14:03.237169,240e6f5c-e09a-11e1-962c-c82a1417b0e9,another session,02a0f14a92b4e0070ee17275f1d78c3a7db1ba68,955,0.0441081523895
</code></pre></div></div>

The fields here are a timestamp for the run, a unique identifier hash for the
session, the session message, a SHA hash of the results, the number of bytes
returned, and the elapsed seconds for the request.

Now let's generate the report, dumping it to a file:

```bash
timr report --input=google-timr.csv --output=google-report.csv
```

And this outputs:

<div style="width: 100%; overflow-x: scroll; overflow-y: hidden; white-space: nowrap;"><div style="width: 1200px;"><pre><code>
03a227c0-e09a-11e1-ad5b-c82a1417b0e9,initial search,0.0433859825134,0.141083955765,0.0681069493294,0.0486528640897
240e6f5c-e09a-11e1-962c-c82a1417b0e9,another session,0.0436999797821,0.389742851257,0.130580246448,0.172775632452
</code></pre></div></div>

The fields here are the session identifier, the session message, and some
summary statistics on the timings (minimum time, maximum time, mean time, and
standard deviation).

From this we can see several things:

* The minimum times are very close (0.0433 and 0.434).
* There's a lot more variance in the maximum times (0.141 and 0.390). This is
  probably caused by network latency or other issues and doesn't accurately
  reflect the time it took Google to process the query. Actually, looking at
  the first outputs, the first request takes the longest, and that could be
  because the Python VM is warming up.
* The added time of the first request throws off the mean and standard
  deviation, so they're not that useful either.

## More Information and Feedback

For more information about timr, see [the readme][readme].

Timr is a very new tool, and there are lots of missing features or even bugs.
If you have a feature request or encounter a problem, please [create a new
Github issue][newissue].

For example, I could imagine that throwing out the longest or first timing when
generating the report would be helpful. What do you think?

[newissue]: https://github.com/erochest/timr/issues/new                        "New Issue"
[neatline]: http://neatline.scholarslab.org/                                   "Neatline"
[whatisdh]: http://whatisdh.herokuapp.com/                                     "What is DH?"
[gc]:       http://en.wikipedia.org/wiki/Garbage_collection_(computer_science) "Garbage Collection"
[timr]:     https://github.com/erochest/timr                                   "erochest/timr"
[python]:   http://python.org/                                                 "Python"
[pip]:      http://pypi.python.org/pypi/pip/                                   "Pip"
[progopt]:  http://en.wikipedia.org/wiki/Program_optimization                  "Wikipedia: Program Optimization"
[readme]:   https://github.com/erochest/timr#readme                            "timr README"
