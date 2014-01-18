AutoWrap
========

A Git Commit hook for automatically wrapping all commit messages to 72 characters

Step 1) Copy the script auto-wrap-72-char.py to <Your Git Repo>/.git/hooks
Step 2) Add the following lines to <Your Git Repo>/.git/hooks/commit-msg.sample:

```bash
if [ "$GITAUTOWRAP" = "true" ]; then
	exec < /dev/tty
	.git/hooks/auto-wrap-72-char.py $1
fi
```

Step 3) Rename this file to commit-msg to enable the hook.

Step 4) Add an environment variable called GITAUTOWRAP and set its value to "true". 

Voilà! Now your commit messages will be automatically formatted such that no line exceeds 72 characters. Exception: URLs or other long strings that are more than 72 characters wide (since these cannot be broken up)

Existing line breaks are left as-is, as are any lines that are less than 72 characters long.

To find out more about why you may want to format your Git commit messages in this way, check out this blog post: http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html

Find a concise introduction to Git hooks here: http://git-scm.com/book/ch7-3.html
