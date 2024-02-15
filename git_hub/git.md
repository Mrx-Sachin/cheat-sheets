# Git command-line interface

## Basic
- `git help <command>:` get help for a git command

- `git init:` creates a new git repo, with data stored in the .git directory

- `git status:` tells you what’s going on
- `git add <filename>:` adds files to staging area
- `git commit:` creates a new commit

    -Write good [commit messages](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)!

    -[Even more reasons to write good commit messages!](https://cbea.ms/git-commit/)
- `git log:` shows a flattened log of history
- `git log --all --graph --decorate`: visualizes history as a DAG
- `git diff <filename>:` show changes you made relative to the staging area
- `git diff <revision> <filename>: `shows differences in a file between snapshots
- `git checkout <revision>:` updates HEAD and current branch

## Branching and merging

- `git branch:` shows branches
- `git branch <name>:` creates a branch
- `git checkout -b <name>:` creates a branch and switches to it

    -same as `git branch <name>; git checkout <name>`
- `git merge <revision>:` merges into current branch
- `git mergetool:` use a fancy tool to help resolve merge conflicts
- `git rebase:` rebase set of patches onto a new base

## Remotes

- `git remote:` list remotes
- `git remote add <name> <url>:` add a remote
- `git push <remote> <local branch>:<remote branch>:` send objects to remote, and update remote reference
- `git branch --set-upstream-to=<remote>/<remote branch>:` set up correspondence between local and remote branch
- `git fetch:` retrieve objects/references from a remote
- `git pull:` same as git fetch; git merge
- `git clone:` download repository from remote
## Undo
- `git commit --amend:` edit a commit’s contents/message
- `git reset HEAD <file>:` unstage a file
- `git checkout -- <file>:` discard changes
 
# Advanced Git

- `git config:` Git is [highly customizable](https://git-scm.com/docs/git-config)
- `git clone --depth=1:` shallow clone, without entire version history
- `git add -p:` interactive staging
- `git rebase -i:` interactive rebasing
- `git blame:` show who last edited which line
- `git stash:` temporarily remove modifications to working directory
- `git bisect:` binary search history (e.g. for regressions)
- `.gitignore:` [specify](https://git-scm.com/docs/gitignore) intentionally untracked files to ignore

## Git’s data model

There are many ad-hoc approaches you could take to version control. Git has a well-thought-out model that enables all the nice features of version control, like maintaining history, supporting branches, and enabling collaboration.

Snapshots
Git models the history of a collection of files and folders within some top-level directory as a series of snapshots. In Git terminology, a file is called a “blob”, and it’s just a bunch of bytes. A directory is called a “tree”, and it maps names to blobs or trees (so directories can contain other directories). A snapshot is the top-level tree that is being tracked. For example, we might have a tree as follows:


```
<root> (tree)
|
+- foo (tree)
|  |
|  + bar.txt (blob, contents = "hello world")
|
+- baz.txt (blob, contents = "git is wonderful")
```

The top-level tree contains two elements, a tree “foo” (that itself contains one element, a blob “bar.txt”), and a blob “baz.txt”.

### Data model, as pseudocode

It may be instructive to see Git’s data model written down in pseudocode:

```
// a file is a bunch of bytes
type blob = array<byte>

// a directory contains named files and directories
type tree = map<string, tree | blob>

// a commit has parents, metadata, and the top-level tree
type commit = struct {
    parents: array<commit>
    author: string
    message: string
    snapshot: tree
}
```

### Objects and content-addressing

An “object” is a blob, tree, or commit:

In Git data store, all objects are content-addressed by their [SHA-1 hash](https://en.wikipedia.org/wiki/SHA-1).

```
type object = blob | tree | commit

objects = map<string, object>

def store(object):
    id = sha1(object)
    objects[id] = object

def load(id):
    return objects[id]
```
Blobs, trees, and commits are unified in this way: they are all objects. When they reference other objects, they don’t actually contain them in their on-disk representation, but have a reference to them by their hash.

### Staging area
This is another concept that’s orthogonal to the data model, but it’s a part of the interface to create commits.

One way you might imagine implementing snapshotting as described above is to have a `“create snapshot” `command that creates a new snapshot based on the current state of the working directory. Some version control tools work like this, but not Git. We want clean snapshots, and it might not always be ideal to make a snapshot from the current state. 

For example, imagine a scenario where you’ve implemented two separate features, and you want to create two separate commits, where the first introduces the first feature, and the next introduces the second feature. Or imagine a scenario where you have debugging print statements added all over your code, along with a bugfix; you want to commit the bugfix while discarding all the print statements.

Git accommodates such scenarios by allowing you to specify which modifications should be included in the next snapshot through a mechanism called the `“staging area”`.


## Resources

- [Websites](https://missing.csail.mit.edu/2020/version-control/) 
- Books
    - [Pro Git](https://git-scm.com/book/en/v2)
    - [Oh Shit, Git!?!](https://ohshitgit.com/)
- [Learn Git Branching](https://learngitbranching.js.org/) is a browser-based game that teaches you Git.