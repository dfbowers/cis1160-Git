# CIS-1160 Git Practice Tutorial

A beginner-focused static tutorial for Git fundamentals, branching, merging, and conflict resolution. It uses plain-text support documentation and is designed for Git Bash on Windows.

## Preview locally

Open `index.html` in a browser. The site has no build-time dependencies and can be hosted directly from a static web server.

## GitHub Pages

The repository is structured for GitHub Pages. In the repository settings, enable Pages and select the `main` branch with the repository root as the publishing source. The entry page is `index.html`.

## Contents

- `index.html`: course overview and lab directory
- `labs/`: one HTML page per lab
- `checkpoints/`: downloadable starting repositories for each activity
- `content/tutorial-source.md`: source specification used to build the tutorial
- `scripts/`: scripts that generate the pages and checkpoint archives
- `assets/`: responsive styling and small interaction helpers

The tutorial content follows the CIS-1160 Git tutorial specification. The build scripts use Python's standard library; students do not need Python, Ruby, Rake, or a programming runtime.
