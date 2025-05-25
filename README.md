# cookiecutter-robust-python

A Python project template robust enough to follow up [cookiecutter-hypermodern-python]

# Caveat
I really believe this idea has a lot of good ideas and best practices, however creating it is a ton of work.

There is definitely a lot left to do before this project is truly a daily driver, but I think there are just a few more pieces missing from this being at least useful in many cases.

If you have any interest in this project please don't hesitate to reach out!
Any and all advice, support, PR's, etc are welcome and would be greatly appreciated.


# Why does this project exist?
Unfortunately, the [Hypermodern Python Cookiecutter] is no longer maintained nor modern.
While it will always have a place in my heart, there have been far too many improvements in Python tooling to keep using it as is.

For a while I maintained [a personal fork](https://github.com/56kyle/cookiecutter-hypermodern-python) that I would update, however when it came time to switch
to new tooling such as [ruff], [uv], [maturin], etc, I found the process of updating the existing tooling to be extremly painful.

The [Hypermodern Python Cookiecutter] remains as a fantastic sendoff point for devs interested in building a 2021 style Python Package, but there were
a handfull of issues with it that prevented it from being able to adapt to new Python developments over the years.

# Okay, so what's different this time?
The [Robust Python Cookiecutter] exists to solve a few main concerns
- [Template Update Propagation](#template-update-propagation)
- [Project Domain Expansion](#project-domain-expansion)
- [Documenting Tooling Decisions](#documenting-tooling-decisions)
- [CI/CD Vendor Lock](#cicd-vendor-lock)
- [Project Neglect](#project-neglect)


## Template Update Propogation
One of the main issues I encountered with [my personal fork] of the [Hypermodern Python Cookiecutter] was that any change
I made to my repos would mean a later conflict if I tried to rerun [cookiecutter] to sync a change from a different project.

Thankfully, [cruft] exists specifically to help with this issue. It enables us to periodically create PR's to add in any fixes
the [Robust Python Cookiecutter] may have added.

Additionally, extra care is put in to use tooling specific config files whenever possible to help reduce merge conflicts occurring
in the pyproject.toml.


## Project Domain Expansion
Now, I'm not one to advocate for mixing languages together in a project. However, there is a really unique case that has arisen with the creation of [maturin].

There are a plethora of great projects such as [ruff], [uv], [polars], [just], etc all making use of [maturin] to get the performance improvements of [rust] while
submitting their package to both pypi and crates.io

Now, this definitely is not required by any means to make a good Python package, however this pattern only seems to be picking up momentum and has honestly been a massive boon
to Python's ecosystem overall.

That being said, it's generally good practice to avoid the complexity of this dual language system unless you actually need the performance bump for your use case. However knowing ahead of time if performance
will be an issue is rather tricky, and a much easier route is to just prepare as though you *might* swap to it some day.

The [Robust Python Cookiecutter] includes a `include_rust_extensions` flag that not only toggles [maturin] vs a traditional Python package,
but that can be used in combination with [cruft] to swap to [maturin] at any time with just about no risk to CI/CD / etc.

Additionally, the [Robust Python Cookiecutter] is designed with both normal and [monorepos] in mind. So whether you need to just add
a quick [rust] module for performance or you are trying to publish a series of crates and packages, either case will be handled using a setup inspired by [polars].





## Documenting Tooling Decisions
One of the really stand out features of the [Hypermodern Python Cookiecutter] was its incredibly detailed documentation.
It did a pretty great job of describing the tooling to use, but there was a distinct lack of ***why*** these decisions were made.

It may seem like a small detail, but detailing why a decision was made has an incredibly important effect on the maintainablity of the template.
#### **It allows maintainers to check if a decision should change in one click.**
Rather than having to go through a mini crusade to determine whether we use [poetry] or [uv], we can just point to the
[existing reasoning](https://cookiecutter-robust-python.readthedocs.io/en/latest/topics/02_dependency_management.md#option-2--term--poetry) to see if it still is true or not.

Overall it's rather rare that people debate over tooling for no reason. Most things have merit in some cases, and a large goal of this template is identifying the tools that have the most merit in almost all cases.

## CI/CD Vendor Lock
Now don't get me wrong, I love [github-actions] and do pretty much everything in my power to avoid [bitbucket-pipelines].
However, not all jobs have the luxury of github, and I would love to be able to just use the same template for both my personal and professional projects.

The [Robust Python Cookiecutter] focuses on being as modular as possible for areas that connect to the CI/CD pipeline. Additionally, there will always be either alternative
CI/CD options or at a minimum basic examples of what the translated CI/CD pipeline would look like.

Finally, the main reason that this task is even possible is that the [Robust Python Cookiecutter] mirrors all of the CI/CD steps in it's local dev tooling.
The local [noxfile] is designed to match up directly with the CI/CD each step of the way.

The [Hypermodern Python Cookiecutter] did this where it could afford to also, however the lack of [uv] meant it would significantly increase CI/CD times if done everywhere.
Thankfully now we can spin up a venv with a tiny fraction of the overhead that used to exist.


## Project Neglect
This is most certainly not a knock against claudio. The work they did on [cookiecutter-hypermodern-python] laid the way for countless other devs to start
implementing best practices in their python packages.

However, Open Source work is draining, and is especially so for a project template including metacode.

I can guarantee that if the [Robust Python Cookiecutter] ever sees any amount of users I will immediately transfer it to an organization to enable at least a handful
of trusted individuals to ensure the project is taken care of.

[bitbucket-pipelines]: https://support.atlassian.com/bitbucket-cloud/docs/write-a-pipe-for-bitbucket-pipelines/
[cookiecutter]: https://cookiecutter.readthedocs.io/en/stable/
[cookiecutter-hypermodern-python]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[cookiecutter-robust-python]: https://github.com/56kyle/cookiecutter-robust-python
[cruft]: https://cruft.github.io/cruft/
[github-actions]: https://docs.github.com/en/actions
[Hypermodern Python Cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[just]: https://github.com/casey/just?tab=readme-ov-fil
[maturin]: https://github.com/PyO3/maturin
[noxfile]: https://github.com/56kyle/cookiecutter-robust-python/blob/main/%7B%7Bcookiecutter.project_name%7D%7D/noxfile.py
[poetry]: https://python-poetry.org/docs/
[polars]: https://github.com/pola-rs/polars
[Robust Python Cookiecutter]: https://github.com/56kyle/cookiecutter-robust-python
[ruff]: https://docs.astral.sh/ruff/
[rust]: https://www.rust-lang.org/learn
[Rye]: https://rye.astral.sh/
[uv]: https://docs.astral.sh/uv/


