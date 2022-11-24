## repotrack

repotrack displays the comment count of GitHub PRs and issues assigned to you on an ncurses display and keeps it updated.

It also makes a beeping sound and writes a log line in the bottom subwindow when the comment count of any of these issues or PRs change.

### Usage
Provide environment variables: `GITHUB_TOKEN`, `REPOTRACK_REPO`, `REPOTRACK_USERNAME`.

`REPOTRACK_REPO` is full name of the repository you want to track, e.g. "organization/repository"

`REPOTRACK_USERNAME` is the username of the assignee whose PRs and issues will be tracked.
