# Introduction

# Artifact Life Cycle

## Kanban

In our project, we employ a tailored agile methodology that combines the strengths of both Scrum and Kanban. This hybrid approach is designed to maximize efficiency and adaptability while ensuring continuous collaboration and transparency across teams. Key elements from Scrum that we integrate into our workflow include:

- Iterative and Incremental Development: Regularly refining and building upon our work.

- Weekly Sprints: Each week constitutes a new sprint, during which tasks are planned and defined.

- Weekly Planning Meetings: Held in our lecture sessions, these meetings focus on task concretization and detailed planning.

- Progress Reporting and Mini Retrospectives: Brief updates and reflections on progress help identify areas for improvement.

- Inter-Team Communication: Structured opportunities for exchange between teams ensure alignment and collective problem-solving.

Operationally, our sprint meetings are conducted using a Kanban-style board. During these sessions, issues are discussed in detail and moved from our general product backlog into a focused sprint backlog that outlines the tasks for the upcoming week. Throughout the process, each issue then advances through various statuses as detailed below, ensuring continuous improvement and effective inter-team collaboration.

### Workflow and Phases

The Kanban Board consists of the following lanes:

- New
- Open
- To Specify
- In Progress / To Implement
- To Verify
- Done

### New (Backlog)

The Backlog is the starting point for all tasks. The owner of this lane is the Product Owner, who defines features, ideas for features, and reports problems here. These are based on stakeholder requirements.

- **Max. number of tasks**: N/A  
- **Transition Criteria**: N/A

### Open

The Open lane contains all tasks that are planned for the current sprint. They must be thoroughly defined in cooperation between the Product Owner and the development teams. However, they do not have to be technically specified yet. The Product Owner prioritizes the tasks in this lane from highest to lowest priority.

- **Max. number of tasks**: N/A  
- **Transition Criteria**:  
  Tasks can only be moved to this lane from the Backlog during the weekly Sprint meetings.  
  Open tasks require *acceptance criteria* and must be agreed upon by both the development team and the Product Owner.

### To Specify

This lane contains tasks that a development team has decided to work on but have not yet been technically specified. Required changes need to be identified, and an initial design must be created. This usually involves identifying new or affected components and writing a short summary of what needs to be changed or added (e.g., requirements, design, or source code).

- **Max. number of tasks**: 4  
- **Transition Criteria**:  
  Development teams assign the tasks to themselves.

### In Progress / To Implement

This lane contains tasks that are currently in progress. The relevant development team commits to working on the task and implements features according to the specified solution. A "Draft" Pull Request is opened at this stage.

- **Max. number of tasks**: 8  
- **Transition Criteria**:  
  The issue has been specified sufficiently to begin work.  
  Development teams start working on the implementation.

### To Verify

This lane contains tasks that are ready for review. The relevant development team requests a review by the appropriate peer review team. The Pull Request is set to "Ready for Review".

- **Max. number of tasks**: 4  
- **Transition Criteria**:  
  All acceptance criteria must be fulfilled.  
  If this is not possible, consult with the Product Owner and proceed accordingly.

### Done

This lane contains all tasks that have been completed and successfully merged.

- **Max. number of tasks**: N/A  
- **Transition Criteria**:  
  The task was reviewed and merged into the main branch by the Maintainers.

## Working Instructions

### GitHub Issues

When creating an issue, the title must be short and precise.  
It is recommended to include a description containing any useful information relevant to the ticket.  
Do not delete any information on issues — instead, use ~~strikethrough~~ for the affected section and provide the correction below it.  
Add everyone who will be working on the issue as assignees.
All issues need to be correctly labeled and assigned to the "Project Managment" Project to allow for the tracking of the overall project progress.

#### Form/Syntax

Issues should follow the template provided in [`.github/ISSUE_TEMPLATE.md`](https://github.com/THI-CSI/project_bms_sose25/blob/main/.github/ISSUE_TEMPLATE.md)

### Git/GitHub

#### Branching

The branch name must contain the GitHub Issue number and should briefly summarize the purpose or scope of the issue.  
Use only lowercase letters and dashes (`-`) to separate words.

#### Pull Requests

We work with Pull Requests and Draft Pull Requests.  
A Draft Pull Request must be created when the issue status changes to "To Implement".  
Draft Pull Requests cannot be reviewed, to avoid unnecessary comments and commits.  
Pull Requests must be converted to open PRs once the implementation is complete and the issue moves to "To Verify".

<!-- Pull Requests require relevant documentation steps before merging. -->
<!-- Work-in-Progress PRs should be opened as drafts -->
<!-- Draft PRs cannot be reviewed to avoid unnecessary comments and commits -->

##### Form/Syntax

Pull Requests should follow the template provided in [`.github/PULL_REQUEST_TEMPLATE.md`](https://github.com/THI-CSI/project_bms_sose25/blob/main/.github/PULL_REQUEST_TEMPLATE.md)

#### Commits

There is no strict specification for how many or when commits should be made.  
They should separate different tasks that belong to the same problem.  
If there are too many commits, consider squashing them before creating your Pull Request.

Commits must include a commit message, which should be written in the imperative form.

---

**Credits:** This file was written by Pascal Esser, Berkan Erkasap and Timo Weese in equal parts.
