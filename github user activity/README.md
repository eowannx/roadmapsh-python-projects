# GitHub User Activity CLI

A command-line tool to fetch and display recent GitHub activity for any user, built with Python.

## Requirements

- Python 3.6+
- Terminal
- Internet connection

## Setup

This project is part of a larger repository with multiple projects. Clone the whole repo and navigate to this folder:

```bash
git clone https://github.com/eowannx/roadmapsh-python-projects.git
cd github-user-activity
```

## Usage

```bash
python github_activity.py <username>
```

## Examples

```bash
python github_activity.py eowannx
```

```
- PublicEvent in eowannx/roadmapsh-python-projects
- Created a repository eowannx/roadmapsh-python-projects
```

## How it works

The tool fetches the last 30 public events from the [GitHub Events API](https://docs.github.com/en/rest/activity/events) and displays them in a readable format. No authentication is required.

Supported event types:

- `PushEvent` — pushed commits to a repository
- `IssuesEvent` — opened or closed an issue
- `IssueCommentEvent` — commented on an issue
- `PullRequestEvent` — opened, closed or merged a pull request
- `PullRequestReviewEvent` — reviewed a pull request
- `WatchEvent` — starred a repository
- `ForkEvent` — forked a repository
- `CreateEvent` — created a repository
- `DeleteEvent` — deleted a branch or tag
- `ReleaseEvent` — published a release

## Project Source

This project is based on the [GitHub User Activity](https://roadmap.sh/projects/github-user-activity) challenge from [roadmap.sh](https://roadmap.sh).