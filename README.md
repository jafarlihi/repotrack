## repotrack

repotrack displays comment count of your active PRs and issues on an ncurses display and keeps it updated.

It also makes a beeping sound and writes log in the bottom subwindow when comment count of any of these issues and PRs change.

### Usage
Provide environment variables: `GITHUB_TOKEN`, `REPOTRACK_REPO`, `REPOTRACK_USERNAME`.

`REPOTRACK_REPO` is full name of the repository you want to track, e.g. "organization/repository"

`REPOTRACK_USERNAME` is the username of the assignee whose PRs and issues will be tracked.
