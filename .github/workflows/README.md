# GitHub Actions Workflows

This directory contains comprehensive CI/CD workflows for the Audio Archive Bot project.

## Workflows Overview

### 1. CI Workflow (`ci.yml`)

**Purpose:** Continuous Integration testing on every push and pull request.

**Triggers:**
- Push to `main` branch
- Pull requests to `main` branch

**Jobs:**
- **Lint:** Code quality checks (Black, isort, Flake8)
- **Test Python:** Test across Python 3.8, 3.9, 3.10, 3.11, 3.12
- **Test Node.js:** Test across Node.js 16, 18, 20
- **Integration Test:** Test Python + Node.js together
- **Security Scan:** Trivy vulnerability scanning

**Features:**
- Parallel test execution for faster feedback
- Caching for pip and npm dependencies
- FFmpeg installation and testing
- System-level integration tests
- Security vulnerability scanning

---

### 2. Build Workflow (`build.yml`)

**Purpose:** Validate package builds and installation across platforms.

**Triggers:**
- Pull requests to `main` branch
- Push to `main` branch

**Jobs:**
- **Build Package:** Create Python wheel and source distribution
- **Test Installation:** Install and test on Ubuntu, Windows, macOS
- **Build Docker:** Build and test Docker container
- **Validate Scripts:** ShellCheck validation for all shell scripts

**Features:**
- Multi-platform testing (Linux, Windows, macOS)
- Docker image validation
- Package integrity checks with Twine
- Shell script linting with ShellCheck

---

### 3. Release Workflow (`release.yml`)

**Purpose:** Automated releases to PyPI and GitHub when tags are pushed.

**Triggers:**
- Push tags matching `v*.*.*` (e.g., `v1.0.0`, `v2.1.3`)

**Jobs:**
- **Build:** Create release packages
- **Test Package:** Verify package installation
- **Publish PyPI:** Upload to PyPI (production)
- **Publish TestPyPI:** Upload to TestPyPI (for release candidates)
- **Create GitHub Release:** Generate release notes and attach artifacts
- **Build Docker Release:** Push Docker image to Docker Hub

**Features:**
- Automatic version extraction from git tags
- Changelog integration
- PyPI and TestPyPI publishing
- GitHub release with auto-generated notes
- Docker image publishing with semantic versioning
- Prerelease detection (for -rc, -beta, -alpha tags)

**Required Secrets:**
- `PYPI_API_TOKEN`: PyPI API token for publishing
- `TEST_PYPI_API_TOKEN`: TestPyPI API token (optional)
- `DOCKER_USERNAME`: Docker Hub username (optional)
- `DOCKER_PASSWORD`: Docker Hub password/token (optional)

---

### 4. Dependency Check Workflow (`dependency-check.yml`)

**Purpose:** Regular security scanning of dependencies and license compliance.

**Triggers:**
- Weekly schedule (Mondays at 9 AM UTC)
- Pull requests to `main` branch
- Manual dispatch (workflow_dispatch)

**Jobs:**
- **Python Security:** Safety, pip-audit, Bandit scans
- **Node.js Security:** npm audit and outdated package checks
- **Dependency Review:** Review dependency changes in PRs
- **Trivy Scan:** Comprehensive vulnerability scanning
- **Snyk Security:** Commercial security scanning (optional)
- **CodeQL Analysis:** GitHub's semantic code analysis
- **License Check:** License compliance for Python and Node.js
- **Create Security Issue:** Auto-create issues when vulnerabilities found

**Features:**
- Multiple security scanning tools
- License compliance checking
- Automated issue creation for vulnerabilities
- Security reports as artifacts
- SARIF upload to GitHub Security tab

**Optional Secrets:**
- `SNYK_TOKEN`: Snyk API token for enhanced security scanning

---

## Required GitHub Secrets

Configure these secrets in GitHub repository settings:

### Required for Release
- `PYPI_API_TOKEN`: Required for PyPI publishing
  - Get from: https://pypi.org/manage/account/token/

### Optional but Recommended
- `TEST_PYPI_API_TOKEN`: For testing releases on TestPyPI
  - Get from: https://test.pypi.org/manage/account/token/
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub access token
  - Get from: https://hub.docker.com/settings/security
- `SNYK_TOKEN`: Snyk security scanning token
  - Get from: https://snyk.io/account/

---

## How to Configure Secrets

1. Go to your GitHub repository
2. Click **Settings** > **Secrets and variables** > **Actions**
3. Click **New repository secret**
4. Add each required secret:
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI API token
5. Repeat for other secrets

---

## Workflow Trigger Methods

### Automatic Triggers

**CI Workflow:**
```bash
# Triggers automatically on:
git push origin main
git push origin feature-branch  # If PR exists
```

**Build Workflow:**
```bash
# Triggers automatically on:
git push origin main
# Or when creating/updating a PR
```

**Release Workflow:**
```bash
# Create and push a version tag:
git tag v1.0.0
git push origin v1.0.0

# For release candidates:
git tag v1.0.0-rc1
git push origin v1.0.0-rc1
```

**Dependency Check:**
```bash
# Runs automatically every Monday at 9 AM UTC
# Or triggered by PRs
```

### Manual Triggers

**Dependency Check (Manual):**
1. Go to **Actions** tab in GitHub
2. Select **Dependency Security Check**
3. Click **Run workflow**
4. Select branch and click **Run workflow**

---

## Local Testing

Before pushing, you can test locally:

### Run Linting
```bash
pip install black flake8 isort
black --check .
isort --check .
flake8 .
```

### Run Tests
```bash
# Install dependencies
pip install -r requirements.txt
npm ci

# Run Python tests
python test_hybrid_system.py

# Check JavaScript syntax
node --check voice_recorder.js
```

### Test Package Build
```bash
pip install build twine
python -m build
twine check dist/*
```

### Test Docker Build
```bash
docker build -t audio-archive-bot:test .
docker run --rm audio-archive-bot:test python3 --version
```

---

## Workflow Optimization Features

### Caching
- **pip cache:** Python dependencies cached per OS/Python version
- **npm cache:** Node.js dependencies cached per OS/Node version
- **Docker cache:** Layer caching with GitHub Actions cache

### Parallel Execution
- Multiple Python/Node.js versions tested in parallel
- Independent jobs run concurrently
- Matrix builds for cross-platform testing

### Concurrency Control
- Automatic cancellation of outdated workflow runs
- Prevents resource waste on superseded commits

### Fail-Fast Strategy
- `fail-fast: false` allows all matrix jobs to complete
- Provides comprehensive test results even if some fail

---

## Monitoring and Debugging

### View Workflow Runs
1. Go to **Actions** tab in your repository
2. Select the workflow to view
3. Click on a specific run to see details
4. Expand job steps to see logs

### Download Artifacts
- Security reports
- Test coverage reports
- Build packages
- License reports

### Security Alerts
- Check **Security** tab for CodeQL findings
- Review Trivy SARIF uploads
- Monitor dependency alerts

---

## Best Practices

### Before Committing
1. Run linters locally
2. Test code with `test_hybrid_system.py`
3. Ensure all shell scripts are executable
4. Update CHANGELOG.md for releases

### Creating Releases
1. Update version in relevant files
2. Update CHANGELOG.md with changes
3. Create and push tag: `git tag v1.0.0 && git push origin v1.0.0`
4. Monitor release workflow
5. Verify PyPI upload and GitHub release

### Security Updates
1. Review weekly security scan results
2. Update vulnerable dependencies promptly
3. Test after dependency updates
4. Close security issues after resolution

---

## Troubleshooting

### CI Failures

**Python Import Errors:**
- Check requirements.txt is up to date
- Verify Python version compatibility

**Node.js Errors:**
- Ensure package.json dependencies are correct
- Check Node.js version compatibility

**FFmpeg Errors:**
- Verify FFmpeg is installed in CI environment
- Check FFmpeg commands in scripts

### Build Failures

**Package Build Errors:**
- Ensure setup.py has correct metadata
- Verify all required files are included
- Check MANIFEST.in if custom files needed

**Docker Build Errors:**
- Check Dockerfile syntax
- Verify base image availability
- Ensure all COPY paths are correct

### Release Failures

**PyPI Upload Errors:**
- Verify PYPI_API_TOKEN is set correctly
- Check version doesn't already exist on PyPI
- Ensure package name is available

**Tag Issues:**
- Use semantic versioning: `v1.2.3`
- Don't reuse tags
- Push tags explicitly: `git push origin --tags`

---

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## Maintenance

### Regular Tasks
- Review security scan results weekly
- Update dependencies quarterly
- Review and update workflow syntax annually
- Monitor GitHub Actions usage/costs

### Workflow Updates
When updating workflows:
1. Test in a fork or feature branch first
2. Review GitHub Actions changelog for deprecations
3. Update action versions (e.g., `@v4` to `@v5`)
4. Document changes in commit messages

---

For questions or issues with workflows, please open an issue in the repository.
