# CONTRIBUTING

First off, thanks for taking the time to contribute. We really appreciate your interest in this repository.

The following is a set of guidelines for contributing to the repository. These are mostly guidelines, not hard rules.

### Table of Contents

- [General](#general) (See this first!)
- [Basic](#basic)
- [Advanced](#advanced)

---

### General

This part will tell you how to go about contributing to the repository in general.  
Follow the given steps:

- Go to the issues tab in the repository and check the present issues.
- If you found a new bug/ have a enhancement in mind, check for a redundant issue and if it does not exist, create a new issue. You can also ask the core members to assign you to an existing issue.
- Wait for discussion/approval from the core/board members.
- Once approved and assigned,
  - If the issue is a bug report/ feature suggestion, your contribution ends at creating the issue.
  - If it involves changing documentation, head to [basic](#basic)
  - If it involves in fixing a bug or refactoring code or implementing a feature, head to [advanced](#advanced)

---

### Basic

This part will tell you how to make basic contributions to the repository which requires basic python or no python knowledge at all.

These contributions are of the form of changing documentation or some small non code refactors.

##### Instructions

- Having followed the general instructions, make changes on GitHub and create a pull request using the GitHub UI. (The UI guides you in creating one)

---

### Advanced

This part will tell you how to create advanced contributions to repository which requires basic knowledge of python **decorators**, **async** and the **disnake** library.  

#### Instructions

- Having followed the [general](#general) instructions, create a fork of the repository and clone it locally.
- Create a new branch as given in [naming a branch](#naming-a-branch)
- The dev setup is documented in the [README](README.md)
- Code the feature / bug fix / refactor
- Before pushing, execute all precommit hooks which includes linting and formatting. Fix all the issues that might arise from doing so.
- Push the code to your fork and open a pull request
- Wait for reviews from other contributors / core members and resolve all issues that might arise
- Once the pull request has been successfully merged, delete the branch

### Extras

#### Naming a branch

Create a branch with the following format

- `fix/[desc]` For bug fixes
- `feat/[desc]` For new features
- `docs/[desc]` For documentation
- `refactor/[desc]` For refactors

`desc` should be short and concise.