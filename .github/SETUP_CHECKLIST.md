# GitHub Actions Setup Checklist

Complete this checklist to set up CI/CD for the Audio Archive Bot.

## Prerequisites

- [ ] Repository hosted on GitHub
- [ ] Admin access to repository settings
- [ ] PyPI account (for releases)
- [ ] Docker Hub account (optional, for container releases)

---

## Step 1: Verify Workflow Files

Ensure these files exist in `.github/workflows/`:

- [ ] `ci.yml` - Main CI workflow
- [ ] `build.yml` - Package build validation
- [ ] `release.yml` - Automated releases
- [ ] `dependency-check.yml` - Security scanning
- [ ] `README.md` - Workflow documentation

---

## Step 2: Configure Required Secrets

### PyPI Token (Required for releases)

- [ ] Create PyPI account at https://pypi.org
- [ ] Create API token at https://pypi.org/manage/account/token/
  - Token scope: "Entire account" or specific to `audio-archive-bot`
- [ ] Add to GitHub:
  - GitHub repository → Settings → Secrets and variables → Actions
  - New repository secret
  - Name: `PYPI_API_TOKEN`
  - Value: `pypi-...` (paste token)

### TestPyPI Token (Optional, for testing)

- [ ] Create TestPyPI account at https://test.pypi.org
- [ ] Create API token at https://test.pypi.org/manage/account/token/
- [ ] Add to GitHub:
  - Name: `TEST_PYPI_API_TOKEN`
  - Value: Paste token

### Docker Hub (Optional, for container releases)

- [ ] Create Docker Hub account at https://hub.docker.com
- [ ] Create access token at https://hub.docker.com/settings/security
- [ ] Add to GitHub (2 secrets):
  - Name: `DOCKER_USERNAME`, Value: Your Docker Hub username
  - Name: `DOCKER_PASSWORD`, Value: Access token

### Snyk (Optional, for enhanced security scanning)

- [ ] Sign up at https://snyk.io
- [ ] Get API token from account settings
- [ ] Add to GitHub:
  - Name: `SNYK_TOKEN`
  - Value: Your Snyk API token

---

## Step 3: Enable GitHub Features

### Security Features

- [ ] Enable Dependabot alerts
  - Settings → Security → Code security and analysis
  - Enable "Dependency graph"
  - Enable "Dependabot alerts"
  - Enable "Dependabot security updates"

- [ ] Enable Code scanning
  - Settings → Security → Code security and analysis
  - Enable "CodeQL analysis"

- [ ] Enable Secret scanning
  - Settings → Security → Code security and analysis
  - Enable "Secret scanning"

### Branch Protection (Recommended)

- [ ] Configure main branch protection
  - Settings → Branches → Add rule
  - Branch name pattern: `main`
  - Check: "Require status checks to pass before merging"
  - Select: CI, Build workflows
  - Check: "Require branches to be up to date before merging"

### Repository Settings

- [ ] Enable Issues (for security alerts)
- [ ] Enable Actions (should be enabled by default)
- [ ] Set Actions permissions:
  - Settings → Actions → General
  - Allow all actions and reusable workflows
  - Workflow permissions: Read and write permissions

---

## Step 4: Test Workflows

### Test CI Workflow

- [ ] Create a feature branch
  ```bash
  git checkout -b test-ci
  ```

- [ ] Make a small change (e.g., add comment to README)

- [ ] Commit and push
  ```bash
  git add .
  git commit -m "Test CI workflow"
  git push origin test-ci
  ```

- [ ] Create Pull Request on GitHub

- [ ] Verify CI workflow runs automatically

- [ ] Check all jobs pass (Lint, Test Python, Test Node.js, etc.)

- [ ] Close PR or merge if tests pass

### Test Build Workflow

- [ ] Build workflow should run automatically with CI

- [ ] Verify package builds successfully

- [ ] Check cross-platform tests pass

- [ ] Download and inspect artifacts

### Test Dependency Check

- [ ] Manually trigger workflow
  - Actions → Dependency Security Check → Run workflow

- [ ] Wait for completion

- [ ] Review security reports in artifacts

- [ ] Check Security tab for findings

### Test Local CI

- [ ] Run local test script
  ```bash
  ./dev_tools/test_ci_locally.sh
  ```

- [ ] Fix any failures

- [ ] Verify all tests pass locally

---

## Step 5: Create First Release (Optional)

- [ ] Update CHANGELOG.md with release notes

- [ ] Verify all tests pass on main branch

- [ ] Create version tag
  ```bash
  git checkout main
  git pull
  git tag v1.0.0
  git push origin v1.0.0
  ```

- [ ] Monitor release workflow
  - Actions → Release & Publish

- [ ] Verify package published to PyPI
  - Check https://pypi.org/project/audio-archive-bot/

- [ ] Verify GitHub release created
  - Releases → Should see v1.0.0

- [ ] Test installation from PyPI
  ```bash
  pip install audio-archive-bot==1.0.0
  ```

---

## Step 6: Add Status Badges to README

- [ ] Get badge URLs (replace YOUR_USERNAME)
  ```markdown
  ![CI](https://github.com/YOUR_USERNAME/audio_archive_bot/workflows/CI/badge.svg)
  ![Build](https://github.com/YOUR_USERNAME/audio_archive_bot/workflows/Build%20%26%20Package%20Validation/badge.svg)
  ![Security](https://github.com/YOUR_USERNAME/audio_archive_bot/workflows/Dependency%20Security%20Check/badge.svg)
  ```

- [ ] Add badges to top of README.md

- [ ] Commit and push changes

---

## Step 7: Configure Notifications (Optional)

### Email Notifications

- [ ] GitHub → Settings (user settings, not repo)
- [ ] Notifications → Email notification preferences
- [ ] Enable "Actions workflow runs"

### Slack/Discord Notifications

- [ ] Set up webhook integration in Slack/Discord
- [ ] Add webhook URL as secret
- [ ] Create notification job in workflows (see GitHub Actions docs)

---

## Step 8: Ongoing Maintenance

### Weekly Tasks

- [ ] Review security scan results (automated on Mondays)
- [ ] Check for dependency updates
- [ ] Review any security issues created automatically

### Monthly Tasks

- [ ] Review workflow performance/costs
- [ ] Update action versions (e.g., `@v4` to `@v5`)
- [ ] Check for new GitHub Actions features

### Before Each Release

- [ ] Update CHANGELOG.md
- [ ] Run local CI tests
- [ ] Verify all workflows pass
- [ ] Test installation in clean environment
- [ ] Update version numbers if needed

---

## Troubleshooting

### Workflows Not Running

**Problem:** Workflows don't trigger on push/PR

**Solutions:**
- [ ] Check Actions are enabled: Settings → Actions → General
- [ ] Verify workflow files are in `.github/workflows/`
- [ ] Check YAML syntax: `yamllint .github/workflows/*.yml`
- [ ] Review workflow trigger conditions

### Secret Not Found

**Problem:** Workflow fails with "secret not found"

**Solutions:**
- [ ] Verify secret name matches exactly (case-sensitive)
- [ ] Check secret is set in repository (not organization)
- [ ] For forked repos, secrets don't transfer (add manually)
- [ ] Secrets are not available in pull requests from forks

### PyPI Upload Fails

**Problem:** Release workflow fails to upload to PyPI

**Solutions:**
- [ ] Verify `PYPI_API_TOKEN` is valid
- [ ] Check package name is available on PyPI
- [ ] Ensure version number is unique (not already released)
- [ ] Try uploading to TestPyPI first for testing

### Docker Build Fails

**Problem:** Docker image build fails

**Solutions:**
- [ ] Test Docker build locally first
- [ ] Check Dockerfile syntax
- [ ] Verify all COPY paths exist
- [ ] Review Docker build logs for specific errors

---

## Verification

Once setup is complete, you should have:

- [x] ✅ All 4 workflow files in `.github/workflows/`
- [x] ✅ CI runs automatically on push/PR
- [x] ✅ Security scans run weekly
- [x] ✅ Secrets configured for releases
- [x] ✅ Branch protection enabled
- [x] ✅ Status badges in README
- [x] ✅ At least one successful workflow run

---

## Resources

- [Workflow Documentation](.github/workflows/README.md)
- [Quick Reference](.github/WORKFLOWS_QUICK_REFERENCE.md)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Project README](../README.md)

---

**Setup Complete?** Start developing with confidence! All changes will be automatically tested and validated.

**Need Help?** Open an issue or consult the [troubleshooting section](.github/workflows/README.md#troubleshooting).
