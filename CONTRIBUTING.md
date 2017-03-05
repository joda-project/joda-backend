# How to contribute to joda-backend

Joda Backend is part of the Joda Project backend. General feature requests and bug reports
should be opened at the [main Joda repository](https://github.com/joda-project/joda).
Read more [here](https://github.com/joda-project/joda/blob/master/CONTRIBUTING.md) for details.

## Pull Requests
To ease the pull request merge into mainline, please follow these requirements:
- The pull request title and message should be meaningful enough that reading
  the code is not necessary.
- Use similar coding style as you see in existing code.
- **One pull request per feature**. If you want to do more than one thing, send
  multiple pull requests. You should create a separate branch for each one.
- Make sure each individual commit in your pull request is meaningful.
  If you had to make multiple intermediate commits while developing, please
  squash them before sending them to us.
- Use git's [interactive rebase](https://help.github.com/articles/interactive-rebase)
  feature to tidy up your commits before submitting the pull request.
- Tests needs to be written for new features. Code coverage should never decrease.
- Your PRs must pass build tests on Travis.
