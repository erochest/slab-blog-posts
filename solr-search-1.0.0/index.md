
The Scholars' Lab is pleased to announce the first release of the
[SolrSearch][github] [Omeka][omeka] plugin.

SolrSearch allows you to replace Omeka's default search with [Solr][solr]. Solr
is a standard, popular, open source, fast text search engine. It handles hit
highlighting, date math, numeric aggregation functions (mean, max, etc.),
replication, and many, many more things.

This plugin is one of a series of plugins that make it easier to combine Omeka
instances with the kind of computing infrastructure available to larger
libraries and institutions. Of course, with hosted Solr solutions like
[websolr][websolr] and [SolrHQ][solrhq], this isn't just for larger
institutions. Even smaller organizations can take advantage of this.

So what do you get with SolrSearch?

**Performance** Did I mention that Solr is fast? It's been optimized for
high-traffic sites, and it can easily handle much more data than MySQL full
text search can.

**Scalability** Because it's been engineered for large, high-traffic sites,
Solr can handle more data, faster than MySQL. This especially becomes an issue
when you have collections with a large number of items or items with a lot of
data attached to each.

**Configuration** The SolrSearch plugin in highly configurable. You can decide
which fields to search, which can be used for facets, and how to label them.

**Facets** [Facets][facets] slice up your items and allow users to navigate
through those slices. For example, [The Falmouth Project][falmouth] used an
early version of the SolrSearch plugin to give users not only free-text search,
but also to allow users to browse the buildings it records by neighborhood,
date, and use.

You can find the download on the [SolrSearch plugin page][plugin]. The code is
hosted on the [SolrSearch github page][github]. If you have any feedback about
the plugin, find any bugs, or want to suggest features, head over to the
[issues page][issues]. And if you have questions, feel free to post in the
[Omeka forums][forums].

As always, we look forward to seeing how you'll use this.

[facets]: http://en.wikipedia.org/wiki/Faceted_search
[falmouth]: http://falmouth.lib.virginia.edu/
[forums]: http://omeka.org/forums/
[github]: https://github.com/scholarslab/SolrSearch
[issues]: https://github.com/scholarslab/SolrSearch/issues
[omeka]: http://omeka.org/
[plugin]: http://omeka.org/add-ons/plugins/solrsearch/
[solr]: http://lucene.apache.org/solr/
[solrhq]: http://www.solrhq.com/
[websolr]: http://www.websolr.com/

