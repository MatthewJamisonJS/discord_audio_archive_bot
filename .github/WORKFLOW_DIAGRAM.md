# GitHub Actions Workflow Diagram

## Visual Workflow Architecture

```
                         AUDIO ARCHIVE BOT CI/CD PIPELINE
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                           TRIGGER EVENTS                               ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
         │                    │                 │                │
    [Git Push]          [Pull Request]    [Version Tag]   [Schedule/Manual]
         │                    │                 │                │
         └──────┬─────────────┘                 │                │
                │                               │                │
                ▼                               ▼                ▼
    ┌───────────────────────┐      ┌─────────────────┐  ┌──────────────────┐
    │    CI WORKFLOW        │      │    RELEASE      │  │  DEPENDENCY      │
    │    (ci.yml)           │      │   WORKFLOW      │  │  CHECK           │
    │                       │      │  (release.yml)  │  │  (dependency-    │
    │ Runs on: push, PR     │      │                 │  │   check.yml)     │
    │ Branch: main          │      │ Runs on: tags   │  │                  │
    └───────────────────────┘      └─────────────────┘  └──────────────────┘
                │                           │                    │
                │                           │                    │
                ▼                           │                    ▼
    ┌───────────────────────┐              │          ┌──────────────────┐
    │   BUILD WORKFLOW      │              │          │  SECURITY SCANS  │
    │   (build.yml)         │              │          │                  │
    │                       │              │          │ • Safety         │
    │ Runs on: push, PR     │              │          │ • pip-audit      │
    │ Branch: main          │              │          │ • Bandit         │
    └───────────────────────┘              │          │ • npm audit      │
                                           │          │ • Trivy          │
                                           │          │ • CodeQL         │
                                           │          │ • Snyk (opt)     │
                                           │          │ • License Check  │
                                           │          └──────────────────┘


┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                        CI WORKFLOW DETAILS                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌────────────────┐
│  1. LINT JOB   │
│  Python 3.11   │
└────────────────┘
        │
        ├─► Black --check
        ├─► isort --check
        └─► Flake8
                                    ┌──────────────────────┐
┌────────────────────────────┐     │  MATRIX STRATEGY     │
│  2. TEST PYTHON (Matrix)   │◄────┤  Python: 3.8-3.12    │
│  OS: Ubuntu                │     │  OS: Ubuntu          │
└────────────────────────────┘     └──────────────────────┘
        │
        ├─► Install FFmpeg
        ├─► Install Python deps (cached)
        ├─► Verify imports
        ├─► Syntax check (.py files)
        └─► Run test_hybrid_system.py

                                    ┌──────────────────────┐
┌────────────────────────────┐     │  MATRIX STRATEGY     │
│  3. TEST NODE.JS (Matrix)  │◄────┤  Node: 16, 18, 20    │
│  OS: Ubuntu                │     │  OS: Ubuntu          │
└────────────────────────────┘     └──────────────────────┘
        │
        ├─► Install FFmpeg
        ├─► npm ci (cached)
        ├─► Syntax check (.js files)
        └─► Verify npm packages

┌────────────────────────────┐
│  4. INTEGRATION TEST       │
│  Python 3.11 + Node.js 20  │
└────────────────────────────┘
        │
        ├─► Install all dependencies
        ├─► Run hybrid system test
        ├─► Verify FFmpeg
        └─► Check directory structure

┌────────────────────────────┐
│  5. SECURITY SCAN          │
│  Trivy                     │
└────────────────────────────┘
        │
        ├─► Scan filesystem
        ├─► Generate SARIF
        └─► Upload to GitHub Security


┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                      BUILD WORKFLOW DETAILS                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌────────────────────────────┐
│  1. BUILD PACKAGE          │
│  Python 3.11               │
└────────────────────────────┘
        │
        ├─► Create setup.py
        ├─► python -m build
        ├─► twine check
        └─► Upload artifacts
                │
                ▼
                                    ┌──────────────────────────┐
┌────────────────────────────┐     │  MATRIX STRATEGY         │
│  2. TEST INSTALLATION      │◄────┤  OS: Ubuntu, Win, macOS  │
│  Multi-platform            │     │  Python: 3.8, 3.11, 3.12 │
└────────────────────────────┘     └──────────────────────────┘
        │
        ├─► Download artifacts
        ├─► Install wheel
        └─► Verify imports

┌────────────────────────────┐
│  3. BUILD DOCKER           │
│  Ubuntu                    │
└────────────────────────────┘
        │
        ├─► Create Dockerfile
        ├─► Build image (cached)
        └─► Test image

┌────────────────────────────┐
│  4. VALIDATE SCRIPTS       │
│  ShellCheck                │
└────────────────────────────┘
        │
        ├─► ShellCheck all .sh files
        └─► Bash syntax check


┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                     RELEASE WORKFLOW DETAILS                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    Tag: v1.0.0 (or v*.*.*-rc/beta/alpha)
        │
        ▼
┌────────────────────────────┐
│  1. BUILD                  │
└────────────────────────────┘
        │
        ├─► Extract version from tag
        ├─► Create setup.py (versioned)
        ├─► Build distributions
        └─► Upload artifacts
                │
                ▼
┌────────────────────────────┐
│  2. TEST PACKAGE           │
└────────────────────────────┘
        │
        ├─► Download artifacts
        ├─► Install in clean env
        └─► Verify functionality
                │
                ▼
┌────────────────────────────┐      ┌──────────────────────┐
│  3. PUBLISH PYPI           │◄─────┤ Secret:              │
│  Production                │      │ PYPI_API_TOKEN       │
└────────────────────────────┘      └──────────────────────┘
        │
        └─► pypa/gh-action-pypi-publish
                │
                ▼
┌────────────────────────────┐      (Only for -rc tags)
│  4. PUBLISH TESTPYPI       │
│  (Optional)                │
└────────────────────────────┘
                │
                ▼
┌────────────────────────────┐
│  5. CREATE GITHUB RELEASE  │
└────────────────────────────┘
        │
        ├─► Extract CHANGELOG
        ├─► Generate release notes
        ├─► Attach artifacts
        └─► Mark prerelease if needed
                │
                ▼
┌────────────────────────────┐      ┌──────────────────────┐
│  6. BUILD DOCKER RELEASE   │◄─────┤ Secrets:             │
│  Docker Hub                │      │ DOCKER_USERNAME      │
└────────────────────────────┘      │ DOCKER_PASSWORD      │
        │                            └──────────────────────┘
        ├─► Build multi-arch image
        ├─► Tag with semver
        └─► Push to Docker Hub


┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                 DEPENDENCY CHECK WORKFLOW DETAILS                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    Schedule: Weekly (Mon 9AM UTC) | PR | Manual
        │
        ├────────────┬────────────┬────────────┬─────────────┐
        ▼            ▼            ▼            ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Python   │  │ Node.js  │  │   Dep    │  │  Trivy   │  │  CodeQL  │
│ Security │  │ Security │  │  Review  │  │   Scan   │  │ Analysis │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
     │             │              │             │             │
     │             │              │             │             │
     ▼             ▼              ▼             ▼             ▼
  Safety       npm audit    Dep Review    Filesystem    Python &
pip-audit       Check        Action       Scanning      JavaScript
  Bandit      Outdated                                  Analysis
     │             │              │             │             │
     └─────────────┴──────────────┴─────────────┴─────────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
        ┌──────────────┐            ┌─────────────────┐
        │   License    │            │  Create Issue   │
        │    Check     │            │  (if failures)  │
        └──────────────┘            └─────────────────┘
                │
                ▼
        pip-licenses
      license-checker
                │
                ▼
    Upload all reports as artifacts
    Upload SARIF to Security tab


┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                          OUTPUT DESTINATIONS                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌─────────────────────────────────────────────────────────────────────┐
│  GitHub Actions Tab                                                 │
├─────────────────────────────────────────────────────────────────────┤
│  • Workflow run history                                             │
│  • Job logs and outputs                                             │
│  • Downloadable artifacts                                           │
│  • Performance metrics                                              │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  GitHub Security Tab                                                │
├─────────────────────────────────────────────────────────────────────┤
│  • CodeQL findings                                                  │
│  • Trivy SARIF uploads                                              │
│  • Dependabot alerts                                                │
│  • Secret scanning alerts                                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  PyPI (pypi.org)                                                    │
├─────────────────────────────────────────────────────────────────────┤
│  • Published packages                                               │
│  • Version history                                                  │
│  • Package metadata                                                 │
│  • Download statistics                                              │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  Docker Hub (hub.docker.com)                                        │
├─────────────────────────────────────────────────────────────────────┤
│  • Docker images                                                    │
│  • Version tags                                                     │
│  • Pull statistics                                                  │
│  • Image layers                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  GitHub Releases                                                    │
├─────────────────────────────────────────────────────────────────────┤
│  • Release notes                                                    │
│  • Changelog entries                                                │
│  • Distribution files                                               │
│  • Git tag references                                               │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  GitHub Issues                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  • Auto-created security issues                                     │
│  • Vulnerability alerts                                             │
│  • Links to workflow runs                                           │
│  • Security labels                                                  │
└─────────────────────────────────────────────────────────────────────┘


┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                        PERFORMANCE FEATURES                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Dependency     │      │  Parallel       │      │  Concurrency    │
│  Caching        │      │  Execution      │      │  Control        │
├─────────────────┤      ├─────────────────┤      ├─────────────────┤
│ • pip cache     │      │ • Matrix builds │      │ • Auto cancel   │
│ • npm cache     │      │ • Multi-OS      │      │   outdated runs │
│ • Docker layers │      │ • Independent   │      │ • Save resources│
│                 │      │   jobs          │      │                 │
└─────────────────┘      └─────────────────┘      └─────────────────┘

┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  Fail-Fast      │      │  Artifacts      │      │  SARIF          │
│  Strategy       │      │  Management     │      │  Integration    │
├─────────────────┤      ├─────────────────┤      ├─────────────────┤
│ • Complete all  │      │ • Security rpts │      │ • Security tab  │
│   matrix tests  │      │ • Build pkgs    │      │ • Trivy upload  │
│ • Full coverage │      │ • License rpts  │      │ • CodeQL upload │
│                 │      │ • 7-day retain  │      │                 │
└─────────────────┘      └─────────────────┘      └─────────────────┘


┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                        DEVELOPER WORKFLOW                              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Local Development
        │
        ├─► Write code
        ├─► Run ./dev_tools/test_ci_locally.sh
        ├─► Fix any issues
        └─► Commit
            │
            ▼
    git push origin feature-branch
            │
            ▼
    Create Pull Request
            │
            ├─► CI Workflow (auto)
            ├─► Build Workflow (auto)
            ├─► Dependency Check (auto)
            └─► Review checks
                │
                ▼
            All checks pass?
                │
            Yes │
                ▼
        Merge to main
                │
                ▼
        Ready for release?
                │
            Yes │
                ▼
    Update CHANGELOG.md
    git tag v1.0.0
    git push origin v1.0.0
                │
                ▼
        Release Workflow (auto)
                │
                ├─► Build package
                ├─► Publish to PyPI
                ├─► Create GitHub Release
                └─► Push Docker image
                        │
                        ▼
                    DEPLOYED!


┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                           KEY METRICS                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

    Workflows: 4                  Documentation: 5 files
    Jobs: 20+                     Scripts: 1
    Steps: 50+                    Total Lines: 2,115+

    Python Versions: 5            Security Tools: 10+
    Node.js Versions: 3           Platforms: 3 OS

    Triggers:                     Outputs:
    • Automatic: 4                • PyPI packages
    • Manual: 1                   • Docker images
    • Scheduled: 1                • GitHub releases
                                  • Security reports
                                  • Build artifacts
```

---

## Legend

```
┌─────┐
│ Job │  = Workflow job
└─────┘

┌──────────┐
│ Matrix   │  = Matrix strategy job (multiple instances)
└──────────┘

│
├─►  = Step or action
│
▼    = Flow direction

[Event]  = Trigger event

Secret:  = Required GitHub secret
```

---

## Quick Navigation

- [CI Workflow Details](./workflows/ci.yml)
- [Build Workflow Details](./workflows/build.yml)
- [Release Workflow Details](./workflows/release.yml)
- [Dependency Check Details](./workflows/dependency-check.yml)
- [Complete Documentation](./workflows/README.md)
- [Setup Guide](./SETUP_CHECKLIST.md)
