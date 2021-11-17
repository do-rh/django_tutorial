**Github Pro**

*Local Workflow*
```git
git init
git add 
git commit -m ""
git branch -D <name_of_branch> to delete branch 
```
*Team Workflow*

* git commit messages need to be professional
    * appending - "adding elie2 to instructor .txt
    you can add longer commit message to explain details" --> body of commit message
    * git log --oneline
* make commit message in txt file
    * git commit (NO -M) -> opens up terminal text editor
    * use body to explain **what and why** vs. how (in code, comments, docstrings etc.)
* more frequent commits
    * complete 2-3 tests
    * complete small feature

*Branching*

* name branches with **lower case**
* main branch is often reserved for production
* take code from main branch, make a new branch where you can work
* `git checkout -b '<id>-issue'`
* `git checkout <branch_name>`
* `git branch - a` - shows branch
* asteriks indicates which branch you are on

*Reviewing Branches*

* make a feature branch
* work on the branch
* push the branch up to github & create a **pull request**

* On current branch (change via git checkout..) `git merge main`
* delete: `git branch -D <name_of_branch>`
* fast-forward merge: git has no problem figuring out the chronological order of these commits (both branches share the same history). Adds new branch after into history. **No conflicts!** 
* if 2 branches don't have the same history ex:
    * time 1: add a.txt to branch 1
    * time 2: add b.txt to branch 2
    * time 3: add c.txt to branch 1
* needs a git commit message (mandatory)
* **recursive merge:** might run into conflicts.
    * if recursive merge fails, you get a merge conflict
    * `git status` shows unmerged paths.
    * any unmerged files, go to file and resolve the conflict in text editor
    * when working on same file as another branch, over a different course of a chronological period
    * `git merge --abort` - silences merge until next time. (procrastination command)
    * `git reset -hard` undoes last commit (or you can the git id)

**Pull Request Workflow**

* Fork or Clone repository
* Fork - working with larger open-source projects
       - copying a remote repository (don't add collaborators). cannot push to the main repo at all.
* Make a new branch - **NEVER WRITE CODE ON MAIN BRANCH!**
* submit a pull request

*Pull Requests*

* send your branch up to github via `git push origin <branch_name>`
* creates a branch on github called <branch_name> (or will overwrite the one with the same name)
* pull request allows for CR and merging of code to main branch.
* after a PR is merged, everyone else update main branch
    * when working on something unrelated, merge other branch with main branch immediately or in a little bit.
* Include **what/where/why**


**Common Problems**

* merge conflict:
    * never commit if you have unresolved conflicts
    * see what files contain and see if you can fix them yourself
    * git merge --abort if you want to postpone
    * always fix yourself!!!
* forgot to update main:
    * git pull <NAME_OF_REMOTE> <NAME_OF_BRANCH> to update your branch.
    * if you are working on an irrelevent / new feature, you won't need to stay up to date as much.
* need to pull but don't want to commit
    * need to be on clean working tree to merge
    * `git stash`
    * pull 
    * `git stash pop` to review new changes
* new branch on GitHub that I don't have locally
    * `git fetch` if you want that branch locally
    * `git checkout <NAME_OF_BRANCH>` -> creates local one that tracks the remote branch.
* undo a commit
    * git reset HEAD~1 -> moves committed files to working area (-soft flag). Remove any previous changes (-hard flag).
    * actually better to make a new commit with the fixes instead of undo a commit. Don't re-write history! 
* fix commit message **--force**
    * `git commit --amend` allows you to change the commit message in terminal text editor.
    * github will reject the push since it overwrites on github
    * `git push origin amend-message --force`
* commiteted on wrong branch
    * undo with git reset HEAD~1
    * git checkout to the desired branch and re-commit.
    
**STAY AWAY FROM REBASE**