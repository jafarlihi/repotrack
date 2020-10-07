import os
import curses
import time
import math
from github import Github


def beep():
    os.system('speaker-test -l 1 -t sine >/dev/null 2>&1')


def main(stdscr):
    curses.use_default_colors()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    overview_window = curses.newwin(math.floor(curses.LINES * 0.75), curses.COLS)
    log_window = curses.newwin(math.floor(curses.LINES * 0.25),
                               curses.COLS,
                               math.floor(curses.LINES * 0.75),
                               0)
    log_window.addstr("Log:\n")
    log_window.refresh()

    github = Github(os.getenv('GITHUB_TOKEN'))
    repo = github.get_repo(os.getenv('REPOTRACK_REPO'))

    issues = {}
    prs = {}

    while True:
        _issues = repo.get_issues(assignee=os.getenv('REPOTRACK_USERNAME'))
        for issue in _issues:
            if issue.pull_request is None:
                comment_count = issue.comments
                issue.comment_count = comment_count
                if issue.id in issues and issues[issue.id].comment_count != comment_count:
                    changed_by = comment_count - issues[issue.id].comment_count
                    log_window.addstr('"' + issue.title + '" issue comment count changed by ' + str(changed_by) + '\n')
                    log_window.refresh()
                    beep()
                issues[issue.id] = issue

        _prs = repo.get_pulls()
        for pr in _prs:
            if pr.assignee.login == os.getenv('REPOTRACK_USERNAME'):
                comment_count = pr.comments + pr.review_comments
                pr.comment_count = comment_count
                if pr.id in prs and prs[pr.id].comment_count != comment_count:
                    changed_by = comment_count - prs[pr.id].comment_count
                    log_window.addstr('"' + pr.title + '" PR comment count changed by ' + str(changed_by) + '\n')
                    log_window.refresh()
                    beep()
                prs[pr.id] = pr

        overview_window.erase()

        overview_window.addstr('Issues\n')
        for issue in issues.values():
            overview_window.addstr(issue.title + ' - ' + str(issue.comment_count) + '\n')
        overview_window.addstr('\n')

        overview_window.addstr('PRs\n')
        for pr in prs.values():
            overview_window.addstr(pr.title + ' - ' + str(pr.comment_count) + '\n')

        overview_window.refresh()

        time.sleep(30)


if __name__ == '__main__':
    curses.wrapper(main)
