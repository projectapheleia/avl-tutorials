# AVL Tutorials - Apheleia Verification Library Training Tutorials

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)


AVL Tutorials is a free to use library of training tutorials to help learn the basics of AVL.

---

## 📦 Installation

### Install from Source

To create a [virtual environment](https://docs.python.org/3/library/venv.html) rather than install globally a script is provided. This will install, with edit privileges to local virtual environment.

This script assumes you have  [Verilator](https://www.veripool.org/verilator/) installed, so all examples will build out of the box.


```sh
git clone https://github.com/projectapheleia/avl-tutorials.git
cd avl-tutorials
source avl-tutorials.sh
```

## Documentation

Both Powerpoint presentations are available in the doc directory:

* Setup - Details on how to install the tools / libraries required
* Intro - Introduction to AVL. Key concepts and features
* Tutorials - Details on the tutorials in this library

## 🏃 Tutorials

To run a tutorial:

```sh
cd tutorials/THE TUTORIAL YOU WANT

# To run
make sim

# To clean
make clean
```

---

## 🧹 Code Style & Linting

This project uses [**Ruff**](https://docs.astral.sh/ruff/) for linting and formatting.

Check code for issues:

```sh
ruff check .
```

Automatically fix common issues:

```sh
ruff check . --fix
```

## 📧 Contact

- Email: avl@projectapheleia.net
- GitHub: [projectapheleia](https://github.com/projectapheleia)
