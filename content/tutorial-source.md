# CIS-1160 Git Practice Tutorial
## Content and Build Specification

**Course:** CIS-1160 Introduction to Information Systems  
**Purpose:** Source content and design specification for a self-hosted Git tutorial  
**Audience:** First-year Computer Networking Technology students  
**Primary environment:** Git for Windows using Git Bash  

---

# 1. Purpose

This tutorial provides a focused introduction to Git for CIS-1160. It is designed to replace the portions of Git Immersion currently used in the course while removing unrelated programming dependencies and topics that are not required by the course outcomes.

The tutorial should be:

- self-contained
- beginner-friendly
- usable on a new computer without previous lab files
- focused on Git rather than programming
- based on simple text files relevant to technical/support work
- suitable for guided classroom use and independent distance learning
- easy to resume from checkpoints if a repository becomes unusable

Students should not need Ruby, Rake, or programming knowledge.

---

# 2. Learning Outcomes Supported

The tutorial supports the CIS-1160 Git-related outcomes currently addressed through M2 and M3:

- Explain the purpose of version control
- Create and manage a local Git repository
- Save and manage changes using Git
- Inspect repository status and history
- Create and manage branches
- Merge changes between branches
- Identify and resolve a merge conflict
- Explain how branching and merging support collaborative work

The tutorial should teach concepts before requiring students to demonstrate them.

---

# 3. Design Principles

## 3.1 Guided to Independent

Activities should progress from:

1. Guided setup
2. Simple commands with explanation
3. Repeated practice
4. Independent application
5. Evidence of completed work

## 3.2 Git, Not Programming

Use plain-text and Markdown files rather than source code.

Suggested repository:

```text
support-tools/
├── README.md
└── network-checklist.txt
```

Students should be able to understand every file they edit without programming knowledge.

## 3.3 Explain What Commands Do

Do not present commands as sequences to copy blindly.

Each important command should answer:

- What does this command do?
- What changed?
- Where is that change now?
- How can I verify it?

## 3.4 Make Repository State Visible

Frequently use:

```bash
git status
git log --oneline
git branch
git log --graph --oneline --all
```

Students should develop the habit of checking repository state rather than guessing.

## 3.5 Avoid Unnecessary Complexity

The core tutorial should not require:

- Ruby
- Rake
- programming
- custom Git aliases
- tags
- Git object/database internals
- detached HEAD exercises
- rebasing
- Git server administration
- manual editing of `.gitconfig`

Undo/reset/revert/amend can be developed later as optional material if required.

---

# 4. Suggested Website Structure

## Part 1: Git Fundamentals

1. Git Setup
2. Create Your First Repository
3. Check Repository Status
4. Make Your First Commit
5. Make and Inspect a Change
6. Stage a Change
7. Commit the Change
8. Staged vs. Unstaged Changes
9. View Repository History
10. M2 Checkpoint

## Part 2: Branching and Merging

11. Understanding Branches
12. Create a Branch
13. Work on a Branch
14. Switch Between Branches
15. Create Diverging Work
16. View Branch History
17. Merge Branches
18. Create a Merge Conflict
19. Resolve a Merge Conflict
20. M3 Checkpoint

Each page should use a predictable structure:

- Goal
- Why this matters
- Starting point
- Instructions
- Commands
- What to notice
- Check your work
- Next

---

# 5. Part 1: Git Fundamentals

# Lab 1: Git Setup

## Goal

Install Git and confirm that it is ready to use.

## Install Git

Install the standard version of Git for Windows.

Open **Git Bash** after installation.

Verify Git:

```bash
git --version
```

A Git version number should appear.

## Configure Your Identity

Replace the example information with your own:

```bash
git config --global user.name "First Last"
git config --global user.email "you@example.com"
```

For the CIS-1160 lab environment, use:

```bash
git config --global core.autocrlf false
```

## Verify Configuration

```bash
git config --global --list
```

## What to Notice

Git stores information about who creates each commit.

The `--global` option applies the setting to repositories used by your Windows user account.

You do not need to manually edit `.gitconfig`.

## Check Your Work

You should be able to run:

```bash
git --version
git config --global --list
```

without errors.

---

# Lab 2: Create Your First Repository

## Goal

Create a folder and turn it into a Git repository.

## Create the Project

Choose a location where you can easily find your course work.

In Git Bash:

```bash
mkdir support-tools
cd support-tools
```

Initialize Git and standardize the branch name:

```bash
git init
git branch -M main
```

Check the repository:

```bash
git status
git branch
```

## What Just Happened?

`git init` created a Git repository inside the `support-tools` folder.

Git created a hidden `.git` directory that stores repository information and history.

Do not manually edit files inside `.git`.

## What to Notice

The repository has no commits yet. `git status` confirms that its branch name is `main`. Renaming it here means everyone uses the same branch name in the later activities.

## Check Your Work

Run:

```bash
git status
```

The status should say you are on branch `main` and that there are no commits yet.

---

# Lab 3: Create a Project File

## Goal

See how Git reacts when a new file appears in the working directory.

Create:

```text
network-checklist.txt
```

Add the following content:

```text
Network Troubleshooting Checklist

1. Confirm the physical connection.
2. Check link status.
3. Verify the IP configuration.
```

Save the file.

Now run:

```bash
git status
```

## What to Notice

Git sees the file, but it is **untracked**.

The file exists in your working directory, but Git is not yet including it in a commit.

This introduces three important areas:

```text
Working Directory → Staging Area → Repository History
```

---

# Lab 4: Stage Your First File

## Goal

Prepare a file to be included in a commit.

Run:

```bash
git add network-checklist.txt
```

Then:

```bash
git status
```

## What to Notice

The file has moved from **untracked** to **staged**.

`git add` does not permanently save a version to repository history.

It tells Git:

> Include this version of the file in my next commit.

---

# Lab 5: Make Your First Commit

## Goal

Create the first saved point in repository history.

Run:

```bash
git commit -m "Add initial network checklist"
```

Then:

```bash
git status
```

## What to Notice

The working tree should now be clean.

View the history:

```bash
git log --oneline
```

You should see your first commit.

## Mental Model

```text
Edit file
   ↓
git add
   ↓
Staging area
   ↓
git commit
   ↓
Repository history
```

---

# Lab 6: Make and Inspect a Change

## Goal

See how Git detects changes to a tracked file.

Open `network-checklist.txt` and add:

```text
4. Test the default gateway.
```

Save the file.

Run:

```bash
git status
```

Then inspect the change:

```bash
git diff
```

## What to Notice

`git status` tells you that the file has changed.

`git diff` shows the actual content that changed.

At this point the change is in the working directory but has not been staged.

---

# Lab 7: Stage and Commit the Change

Stage the modified file:

```bash
git add network-checklist.txt
```

Check:

```bash
git status
```

Commit:

```bash
git commit -m "Add gateway test"
```

View the history:

```bash
git log --oneline
```

## What to Notice

You now have at least two commits.

Each commit represents a point in the history of the project.

---

# Lab 8: Staged vs. Unstaged Changes

## Goal

See that a file can contain both staged and unstaged work.

Add this line:

```text
5. Test DNS resolution.
```

Save.

Stage it:

```bash
git add network-checklist.txt
```

Now add another line:

```text
6. Document the results.
```

Save again.

Run:

```bash
git status
```

Then:

```bash
git diff
```

and:

```bash
git diff --staged
```

## What to Notice

The same file can contain:

- a version already staged for the next commit
- additional changes that are still only in the working directory

`git diff` shows unstaged changes.

`git diff --staged` shows changes currently staged for the next commit.

## Finish the Exercise

Stage the latest version:

```bash
git add network-checklist.txt
```

Commit:

```bash
git commit -m "Expand troubleshooting checklist"
```

---

# Lab 9: Add a README

## Goal

Practise adding another file to an existing repository.

Create:

```text
README.md
```

Add:

```markdown
# Support Tools

Practice repository for CIS-1160 Git activities.

This repository contains simple technical support documentation used to practise version control.
```

Save it.

Check:

```bash
git status
```

Stage and commit:

```bash
git add README.md
git commit -m "Add project README"
```

---

# Lab 10: Inspect Repository History

## Goal

Review the history you have created.

Run:

```bash
git log --oneline
```

Try:

```bash
git log --stat
```

Then:

```bash
git status
```

## What to Notice

Your repository now contains several commits representing changes made over time.

The exact commit identifiers will differ between students.

## M2 Evidence

Save the evidence one folder above `support-tools` so the evidence file does not appear as an untracked project file. From inside the repository, run:

```bash
git log --oneline > ../Firstname_Lastname_M2_log.txt
```

The evidence file will be in the folder that contains `support-tools`. Students may submit the resulting text file or a screenshot showing equivalent evidence.

The log should show several commits created during the fundamentals activities.

---

# 6. Part 2: Branching and Merging

# Lab 11: Understanding Branches

## Goal

Understand what a branch represents before creating one.

Up to this point, the repository history has followed one line:

```text
A → B → C → D
```

A branch allows another line of work to begin from an existing point:

```text
A → B → C → D   main
             \
              E → F   troubleshooting
```

Branches are useful when:

- developing a feature
- fixing a problem
- experimenting
- allowing different work to happen independently

A branch is not a separate repository.

It is another line of development inside the same repository.

## Know Where You Are

Run:

```bash
git branch
```

The `*` identifies the branch you are currently using.

Also run:

```bash
git status
```

Get into the habit of asking:

> What branch am I on?

before committing or merging.

---

# Lab 12: Create a Branch

## Goal

Create a separate line of work.

Make sure you are on `main`:

```bash
git switch main
```

Create and switch to a new branch:

```bash
git switch -c troubleshooting
```

Check:

```bash
git branch
```

and:

```bash
git status
```

## What to Notice

You should now be on:

```text
troubleshooting
```

The repository still contains the same files.

Creating a branch did not create another project folder.

---

# Lab 13: Work on a Branch

## Goal

Make commits that belong to the new branch.

Open:

```text
network-checklist.txt
```

Add:

```text
7. Ping a known external IP address.
```

Save.

Run:

```bash
git status
git diff
```

Then:

```bash
git add network-checklist.txt
git commit -m "Add external connectivity test"
```

Add another line:

```text
8. Record any packet loss or unusual latency.
```

Save and commit:

```bash
git add network-checklist.txt
git commit -m "Add packet loss check"
```

View the history:

```bash
git log --oneline
```

## What to Notice

These commits were created while you were on the `troubleshooting` branch.

---

# Lab 14: Switch Between Branches

## Goal

See that branches can contain different versions of files.

Check your current branch:

```bash
git branch
```

Switch to `main`:

```bash
git switch main
```

Open `network-checklist.txt`.

## What to Notice

The changes made on `troubleshooting` are not present on `main`.

Nothing has been deleted.

Git changed the working files to match the branch you selected.

Switch back:

```bash
git switch troubleshooting
```

Inspect the file again.

Then return to:

```bash
git switch main
```

---

# Lab 15: Create Diverging Work

## Goal

Create a different change on `main` so that `main` and `troubleshooting` contain independent work.

## Instructions

You should currently be on `main`. Verify the current branch:

```bash
git branch
```

The `*` should be beside `main`.

Open `README.md` and add:

```markdown
## Purpose

These files support a repeatable network troubleshooting process.
```

Save the file. Check that Git sees the change:

```bash
git status
```

Stage and commit the README change:

```bash
git add README.md
git commit -m "Document repository purpose"
```

## What to Notice

The branches now contain different commits:

- `main` contains the README change.
- `troubleshooting` contains the additional network-checklist changes.

Do not merge them yet. Lab 16 will visualize the divergence first.

## Check Your Work

Run:

```bash
git branch
git status
```

Confirm that `main` is current, `troubleshooting` still exists, and the working tree is clean.

# Lab 16: View Branch History

## Goal

Visualize how the branches have diverged.

Run:

```bash
git log --graph --oneline --all
```

## What to Notice

The graph should show separate lines of history.

Also run:

```bash
git branch
```

Remember that `*` identifies your current branch.

This graph is an important troubleshooting tool throughout the remainder of the tutorial.

---

# Lab 17: Merge Branches

## Goal

Bring work from one branch into another.

For this exercise, the goal is to bring the `troubleshooting` work into `main`.

First switch to the branch that should **receive** the changes:

```bash
git switch main
```

Confirm:

```bash
git branch
```

Now merge:

```bash
git merge troubleshooting
```

View the result:

```bash
git log --graph --oneline --all
```

Open `network-checklist.txt`.

## What to Notice

The troubleshooting additions should now be available on `main`.

## Important Rule

Think:

> Switch to the branch that should receive the changes, then merge the other branch into it.

For example:

```bash
git switch main
git merge troubleshooting
```

means:

> Bring the changes from `troubleshooting` into `main`.

---

# Lab 18: Create a Merge Conflict

## Goal

Create two branches that independently modify the same line, then attempt to merge them.

## Step 1: Confirm `main`

At the end of Lab 17, `troubleshooting` has been merged into `main`. Switch to `main` and check the repository:

```bash
git switch main
git status
```

The working tree should be clean.

## Step 2: Create the Alternate Branch

Before changing `main`, create and switch to `alternate-link-check`:

```bash
git switch -c alternate-link-check
```

Open `network-checklist.txt`. Find this line:

```text
2. Check link status.
```

Change it to:

```text
2. Verify the Ethernet or Wi-Fi connection is active.
```

Save the file. Stage and commit this version:

```bash
git add network-checklist.txt
git commit -m "Revise connection check"
```

## Step 3: Make a Different Change on `main`

Switch back to `main`:

```bash
git switch main
```

Open `network-checklist.txt`. The second line should again be the original:

```text
2. Check link status.
```

Change it to:

```text
2. Check the network adapter link lights.
```

Save the file. Stage and commit this version:

```bash
git add network-checklist.txt
git commit -m "Clarify link status check"
```

## Step 4: View the Divergence

Before merging, run:

```bash
git log --graph --oneline --all
```

The `main` and `alternate-link-check` branches now contain different changes to the same original line.

## Step 5: Attempt the Merge

You should still be on `main`. Merge the alternate branch:

```bash
git merge alternate-link-check
```

Git should report a merge conflict in `network-checklist.txt`. Check the repository state:

```bash
git status
```

## What to Notice

- Nothing is broken.
- Both branches independently changed the same part of the same file.
- Git cannot safely decide which version you intend to keep.
- Git has paused the merge for a human decision.
- Lab 19 will resolve the conflict.

Do not resolve the conflict in this lab.

## Check Your Work

Run:

```bash
git status
git branch
```

You should be on `main`. `git status` should report an unresolved conflict in `network-checklist.txt`, and the file should contain conflict markers. `git branch` should list `alternate-link-check`.

# Lab 19: Resolve a Merge Conflict

## Goal

Resolve the conflict and complete the merge.

Open:

```text
network-checklist.txt
```

Git will mark the conflicting area with markers similar to:

```text
<<<<<<< HEAD
2. Check the network adapter link lights.
=======
2. Verify the Ethernet or Wi-Fi connection is active.
>>>>>>> alternate-link-check
```

## What the Markers Mean

- `<<<<<<< HEAD` begins the version from your current branch
- `=======` separates the competing versions
- `>>>>>>> alternate-link-check` ends the version from the branch being merged

Git is asking you to decide what the final file should contain.

You may:

- keep the first version
- keep the second version
- combine/rewrite the two versions

For this exercise, replace the entire conflict block with:

```text
2. Verify the network connection and check the adapter link status.
```

Make sure all conflict markers are removed.

Save the file.

Check:

```bash
git status
```

Stage the resolved file:

```bash
git add network-checklist.txt
```

Complete the merge:

```bash
git commit -m "Resolve link check conflict"
```

Check:

```bash
git status
```

Then view the final history:

```bash
git log --graph --oneline --all
```

## What to Notice

A conflict did not mean the repository was broken.

Git stopped because it needed a human decision.

The basic conflict-resolution process is:

```text
Identify conflict
      ↓
Edit final content
      ↓
Remove conflict markers
      ↓
git add
      ↓
git commit
```

## Check Your Work

Run:

```bash
git status
git branch
git log --graph --oneline --all
```

The working tree should be clean. `git branch` should still list `alternate-link-check`, and the graph should show the separate branch work and the completed merge.

---

# Lab 20: M3 Checkpoint

## Goal

Demonstrate the branching and merging work completed in Part 2.

## Instructions

### Review the graph

Confirm that the current branch is `main` and that `alternate-link-check` is still listed:

```bash
git branch
```

Then run:

```bash
git log --graph --oneline --all
```

Inspect the separate history paths and merge before creating your evidence.

### Create M3 evidence

Create:

```bash
git log --graph --oneline --all > Firstname_Lastname_M3_log.txt
```

Students may submit:

- the resulting `.txt` file, or
- a screenshot clearly showing equivalent evidence

The evidence should show:

- commits made during the branch work
- more than one branch/history path where applicable
- merge history
- the completed conflict-resolution work

---

# 7. Checkpoint Repository Design

A major feature of the web tutorial should be the ability to recover without restarting the entire sequence.

Provide downloadable repository checkpoints at important transitions.

Suggested checkpoints:

```text
checkpoints/
├── part1-start/
├── after-first-commit/
├── m2-complete/
├── branching-start/
├── divergent-branches/
├── pre-merge/
└── conflict-start/
```

## Requirements

Each checkpoint should:

- contain a valid `.git` repository
- contain the exact files expected at that point
- contain an appropriate commit history
- use `main` consistently
- have a clean working tree unless the lesson specifically requires otherwise

## Website Recovery Feature

Each activity should include a small section:

### Repository broken?

If your repository is no longer in the expected state, download the checkpoint for this activity and continue from there.

This should be positioned as normal recovery, not failure.

---

# 8. Instructor Notes

## Common Troubleshooting Commands

When a student is stuck, begin with:

```bash
git status
```

Then:

```bash
git branch
```

If branch/history state is unclear:

```bash
git log --graph --oneline --all
```

These three commands should resolve or expose many beginner problems.

## Common Problems

### Wrong Branch

Symptom:

A student's files/history do not match the instructions.

Check:

```bash
git branch
```

The `*` identifies the current branch.

### File Was Not Saved

Symptom:

```bash
git diff
```

shows nothing after the student says they edited a file.

Confirm the file was actually saved.

### Commit Says There Is Nothing to Commit

Check:

```bash
git status
```

Determine whether:

- the file was saved
- the change was already committed
- the student is in the expected repository
- the student is on the expected branch

### Merge Performed in the Wrong Direction

Reinforce:

> Switch to the branch that should receive the changes, then merge the other branch.

### Expected Conflict Did Not Occur

Both branches must independently modify the same part of the same file after their histories diverge.

### Student Is in the Wrong Folder

Use:

```bash
pwd
```

and:

```bash
ls
```

Confirm that the student is inside the intended repository.

### Line Ending Problems

For the CIS-1160 lab environment:

```bash
git config --global core.autocrlf false
```

Do not frame this as the universal Windows Git setting. It is the configuration selected for these course activities based on observed lab behaviour.

---

# 9. Terminology to Reinforce

| Term | Student-friendly meaning |
|---|---|
| Repository | Project folder whose changes Git tracks |
| Working directory | Files currently being worked on |
| Staging area | Changes selected for the next commit |
| Commit | Saved point in repository history |
| History | Sequence of commits |
| Branch | Separate line of development within a repository |
| `main` | Primary branch used in these activities |
| Merge | Bring changes from one branch into another |
| Merge conflict | Git needs a human to decide how competing changes should be combined |
| HEAD | The commit/branch currently checked out |
| Remote | Another copy of the repository stored elsewhere |

Avoid describing a commit simply as "saving a file." The file is already saved on disk. A commit records a version in Git history.

---

# 10. Future Remote Repository Module

Do not introduce remote repositories into the fundamentals or branching activities unless needed for context.

The progression should remain:

```text
Part 1
Working files → Stage → Commit → Local history

Part 2
Local history → Branches → Merge → Conflict resolution

Future module
Local repository ↔ Remote repository
```

When remotes are introduced, clearly distinguish:

```text
git push
```

Send local commits to a remote repository.

```text
git pull
```

Bring remote changes into the local repository.

A **pull request** is not the same thing as `git pull`.

A pull request is a workflow on a hosting platform such as Bitbucket or GitHub for proposing, reviewing, and ultimately merging branch changes.

---

# 11. Website Implementation Notes

The future web tutorial should prioritize clarity over visual complexity.

## Recommended Features

- one activity per page
- persistent Part 1 / Part 2 navigation
- Previous and Next buttons
- copy buttons on command blocks
- visually distinct command and expected-output areas
- simple branch diagrams
- expandable "Why?" explanations
- expandable troubleshooting help
- checkpoint download at appropriate activities
- progress indicator
- clear instructor/student separation if instructor notes are hosted

## Commands vs. Output

Never mix commands students should type with output they should expect.

Example:

### Run

```bash
git status
```

### You should see

A message identifying the current branch and repository state.

Exact output may vary.

## Avoid Over-Scripting

Do not require students to reproduce exact commit hashes or output that naturally differs between machines.

Focus checks on meaningful state:

- correct branch
- clean/modified/staged status
- expected file exists
- expected commit exists
- branch graph demonstrates the intended concept

---

# 12. Assessment Alignment

## M2 Evidence

```bash
git log --oneline > Firstname_Lastname_M2_log.txt
```

Purpose:

Demonstrates that the student created and committed multiple changes to a local repository.

## M3 Evidence

```bash
git log --graph --oneline --all > Firstname_Lastname_M3_log.txt
```

Purpose:

Demonstrates repository history involving branching and merging.

Evidence should support competency rather than reward cosmetic differences in Git output.

---

# 13. Content Intentionally Excluded

The first version of the CIS-1160 tutorial should intentionally omit:

- Ruby setup and execution
- Rake
- custom aliases required by the tutorial
- Git tags
- manual `.gitconfig` editing
- Git object database exploration
- detached HEAD exercises
- advanced reset exercises
- rebasing
- Git daemon/server setup
- programming-specific examples

These may be added later only if they directly support a CIS-1160 outcome or another course requirement.

---

# 14. Relationship to Git Immersion

Git Immersion informed the instructional progression used in the original CIS-1160 activities, particularly:

- introducing repository fundamentals through repeated small commits
- progressively exposing repository history
- creating a separate branch for new work
- allowing branch histories to diverge
- visualizing branch history
- merging branches
- deliberately producing a merge conflict
- resolving the conflict manually
- using checkpoint repositories to allow learners to enter/recover at different stages

The self-hosted CIS-1160 version should use original wording, original examples, and original project files rather than reproducing Git Immersion content.

The primary improvement is removing unrelated Ruby/Rake dependencies and aligning every activity directly with CIS-1160 learning outcomes.

---

# 15. Build Checklist for the Future Work Thread

Before publishing the web tutorial:

- [ ] Verify every command using a clean Git for Windows installation
- [ ] Test the complete Part 1 sequence from an empty folder
- [ ] Test the complete Part 2 sequence
- [ ] Confirm the conflict exercise reliably creates a conflict
- [ ] Build and test every checkpoint repository
- [ ] Confirm `main` is used consistently
- [ ] Test with `core.autocrlf false`
- [ ] Verify instructions on a standard CIS classroom computer
- [ ] Verify instructions for a distance student on a personal Windows computer
- [ ] Confirm no exercise requires Ruby, Rake, or another programming runtime
- [ ] Confirm M2 evidence works
- [ ] Confirm M3 evidence clearly demonstrates the required work
- [ ] Add screenshots/diagrams only where they improve understanding
- [ ] Conduct a final student-readability pass
- [ ] Conduct an outcome-alignment and fairness review

---

# 16. Final Design Goal

A student should be able to begin with no Git experience and progress through:

```text
Create repository
      ↓
Make changes
      ↓
Stage changes
      ↓
Commit changes
      ↓
Inspect history
      ↓
Create branch
      ↓
Work independently
      ↓
See branches diverge
      ↓
Merge
      ↓
Encounter conflict
      ↓
Resolve conflict
```

without needing to understand programming, Ruby, Rake, Git internals, or unrelated advanced Git features.

The tutorial should teach enough Git for students to understand what they are doing before CIS-1160 moves into remote repositories and collaborative workflows.
