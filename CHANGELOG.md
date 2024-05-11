# Changelog

<h2 id="version-0-0-6">v0.0.6</h2>

2024-05-11

* Fixed some mistakes in project documentation
* Added documentation from [v0.0.5](#version-0-0-5) changes
  * This should raise errors with static type checkers when using a non-annotated field
* Added RelaxedBuilder variant
  * Supports the old, relaxed style of builder
  * Static type support for any field name (not just the annotated ones)

<h2 id="version-0-0-5">v0.0.5</h2>

2024-05-11

* Custom defined builders now appear to NOT support getattr
  * This should raise errors with static type checkers when using a non-annotated field
* Added RelaxedBuilder variant
  * Supports the old, relaxed style of builder
  * Static type support for any field name (not just the annotated ones)

<h2 id="version-0-0-2">v0.0.2</h2>

2024-05-05

* Set up project
* Updated README.md
* Fixed compatibility issue with Python 3.8

<h2 id="version-0-0-1">v0.0.1</h2>

2024-05-05

* First release of library
* Add builder pattern to class via `pyuilder.Buildable`
* Customize object builders via `pyuilder.Builder` and `pyuilder.Setter`
