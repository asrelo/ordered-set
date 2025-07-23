# asrelo-ordered-set

An ordered set is a set that remembers the order of its elements (which may be the order of insertion or a custom order). It is implemented in by maintaining a `set` and a `list` objects in sync.

This implementation is thread-safe and covered with comprehensive tests (100% coverage as of version 0.1.0).

An ordered set can also be thought of as a sequence of unique elements with some operations (like membership testing) having been optimized and extra set-like features provided.

One special feature is how an ordered set is updated with new elements. A rule of thumb for most operations: whenever an attempt is made to add a new element into an ordered set, this element is brought to the end of the sequence (whether it's already present in the set, whether it's a singular or a batch update). Some, but not all, of relevant methods also have alternatives that don't move present elements to the end.

## Developer documentation

See `docs/dev/README.md`.

## License

This software is currently distributed under the terms of the LGPL v3.0 (or later).

This license might be changed to a more permissive one in the future. Contact [@asrelo](https://github.com/asrelo) if you are interested in using this software under a permissive license.
