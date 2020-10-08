import os
import curses
import time
import math
import pickle
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
    
    try:
        issues = pickle.load(open(os.getenv('REPOTRACK_REPO').replace('/', '-') + '-issues.p', 'rb'))
    except:
        issues = {}

    try:
        prs = pickle.load(open(os.getenv('REPOTRACK_REPO').replace('/', '-') + '-prs.p', 'rb'))
    except:
        prs = {}

    while True:
        seen_issues = []
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
                seen_issues.append(issue.id)
                pickle.dump(issues, open(os.getenv('REPOTRACK_REPO').replace('/', '-') + '-issues.p', 'wb+'))

        issue_keys_to_delete = []
        for issue_key in issues.keys():
            if issue_key not in seen_issues:
                issue_keys_to_delete.append(issue_key)

        for issue_key in issue_keys_to_delete:
            issues.pop(issue_key, None)
            pickle.dump(issues, open(os.getenv('REPOTRACK_REPO').replace('/', '-') + '-issues.p', 'wb+'))

        seen_prs = []
        _prs = repo.get_pulls()
        for pr in _prs:
            if pr.assignee is not None and pr.assignee.login == os.getenv('REPOTRACK_USERNAME'):
                comment_count = pr.comments + pr.review_comments
                pr.comment_count = comment_count
                if pr.id in prs and prs[pr.id].comment_count != comment_count:
                    changed_by = comment_count - prs[pr.id].comment_count
                    log_window.addstr('"' + pr.title + '" PR comment count changed by ' + str(changed_by) + '\n')
                    log_window.refresh()
                    beep()
                prs[pr.id] = pr
                seen_prs.append(pr.id)
                pickle.dump(prs, open(os.getenv('REPOTRACK_REPO').replace('/', '-') + '-prs.p', 'wb+'))

        pr_keys_to_delete = []
        for pr_key in prs.keys():
            if pr_key not in seen_prs:
                pr_keys_to_delete.append(pr_key)

        for pr_key in pr_keys_to_delete:
            prs.pop(pr_key, None)
            pickle.dump(prs, open(os.getenv('REPOTRACK_REPO').replace('/', '-') + '-prs.p', 'wb+'))

        overview_window.erase()

        overview_window.addstr('Issues\n')
        for issue in issues.values():
            overview_window.addstr(str(issue.comment_count) + ' - ' + issue.title + '\n')
        overview_window.addstr('\n')

        overview_window.addstr('PRs\n')
        for pr in prs.values():
            overview_window.addstr(str(pr.comment_count) + ' - ' + pr.title + '\n')

        overview_window.refresh()

        time.sleep(30)


if __name__ == '__main__':
    curses.wrapper(main)
