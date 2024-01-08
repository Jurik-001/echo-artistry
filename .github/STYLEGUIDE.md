# Style Guide for EchoArtistry Project

Welcome to the EchoArtistry project! We're excited to have you onboard. This document provides the coding conventions, styling rules, and best practices for contributing to EchoArtistry. Where not specifically mentioned, we default to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) and [Google’s Markdown Style Guide](https://google.github.io/styleguide/docguide/).

## Table of Contents

- [Python Style Guide](#python-style-guide)
  - [Code Formatting](#code-formatting)
  - [Naming Conventions](#naming-conventions)
  - [Comments and Docstrings](#comments-and-docstrings)
  - [Imports](#imports)
  - [Error Handling](#error-handling)
  - [Testing](#testing)
- [Markdown Style Guide](#markdown-style-guide)
  - [Headers](#headers)
  - [Lists](#lists)
  - [Links and Images](#links-and-images)
  - [Code](#code)
- [Commit Messages](#commit-messages)

## Python Style Guide

Adhere to these conventions for Python code in EchoArtistry. For additional details, refer to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

### Code Formatting

🛠 **Tools**: Use [Black](https://black.readthedocs.io/) for auto-formatting. Run Black before submitting your code.

📏 **Line Length**: Maximum of 90 characters.

🛠 **Indentation**: 4 spaces per indentation level.

### Naming Conventions

👔 **Follow Google's Guidelines**: Use naming conventions as per the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#316-naming).

### Comments and Docstrings

💬 **Inline Comments**: Avoid inline comments.

📜 **Docstrings**: Use docstring conventions from the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

### Imports

📥 **Order**: Standard library, third-party, then local application imports, sorted alphabetically within each group.

🚫 **Wildcard Imports**: Avoid (`from module import *`).

### Error Handling

🚫 **Specific Exceptions**: Avoid bare excepts; catch specific exceptions.

💬 **Error Messages**: Include messages in exceptions to clarify issues.

### Testing

✅ **Include Tests**: New features or changes should have corresponding tests.

✅ **pytest Framework**: Use `pytest` for writing tests.

## Markdown Style Guide

For Markdown and documentation, follow [Google’s Markdown Style Guide](https://google.github.io/styleguide/docguide/), with these specific guidelines:

### Headers

📏 **Header Formatting**: Use `#` for headers, `##` for subheaders, etc.

### Lists, Links, Images, and Code

Adhere to the standards in [Google’s Markdown Style Guide](https://google.github.io/styleguide/docguide/).

## Commit Messages

✉️ **Imperative Mood**: Write commit messages in the imperative.

📜 **Descriptive**: Clearly describe the changes in the commit.

---

This guide aims to maintain consistency and professionalism in EchoArtistry's codebase. Thank you for contributing! 🚀

---