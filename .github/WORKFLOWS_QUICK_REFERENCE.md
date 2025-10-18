# GitHub Actions Quick Reference

## Quick Commands

### Create a Release
```bash
# 1. Update CHANGELOG.md with release notes
# 2. Create and push a version tag
git tag v1.0.0
git push origin v1.0.0

# For release candidates:
git tag v1.0.0-rc1
git push origin v1.0.0-rc1
```

### Test Locally Before Push
```bash
# Run the local CI test script
./dev_tools/test_ci_locally.sh

# Or test individual components:
black --check .
isort --check .
flake8 .
python test_hybrid_system.py
npm audit
```

### Manual Security Scan
```bash
# Navigate to GitHub Actions
# → Dependency Security Check
# → Run workflow
```

---

## Workflow Status Badges

Add these to your README.md:

```markdown
![CI](https://github.com/YOUR_USERNAME/audio_archive_bot/workflows/CI/badge.svg)
![Build](https://github.com/YOUR_USERNAME/audio_archive_bot/workflows/Build%20%26%20Package%20Validation/badge.svg)
![Security](https://github.com/YOUR_USERNAME/audio_archive_bot/workflows/Dependency%20Security%20Check/badge.svg)
```

---

## Required Secrets Setup

### PyPI Token (Required for releases)
1. Go to https://pypi.org/manage/account/token/
2. Create token with scope: "Entire account"
3. Copy token
4. GitHub → Settings → Secrets → New secret
5. Name: `PYPI_API_TOKEN`
6. Value: Paste token

### Docker Hub (Optional)
1. Go to https://hub.docker.com/settings/security
2. Create new access token
3. GitHub → Settings → Secrets → New secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: The access token

### Snyk (Optional)
1. Sign up at https://snyk.io
2. Get API token from account settings
3. GitHub → Settings → Secrets → New secret
4. Name: `SNYK_TOKEN`
5. Value: Your Snyk API token

---

## Workflow Triggers

| Workflow | Auto Trigger | Manual | Scheduled |
|----------|-------------|---------|-----------|
| CI | Push, PR to main | No | No |
| Build | Push, PR to main | No | No |
| Release | Tag push (v*.*.*) | No | No |
| Dependency Check | PR to main | Yes | Weekly (Mon 9AM UTC) |

---

## Common Tasks

### Fix Linting Errors
```bash
# Auto-fix with Black
black .

# Auto-fix with isort
isort .

# View Flake8 issues
flake8 .
```

### Update Dependencies
```bash
# Python
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt

# Node.js
npm update
npm audit fix
```

### Build Package Locally
```bash
pip install build twine
python -m build
twine check dist/*

# Test installation
pip install dist/*.whl
```

### Build Docker Locally
```bash
docker build -t audio-archive-bot:local .
docker run --rm audio-archive-bot:local python3 --version
docker run --rm audio-archive-bot:local node --version
```

---

## Troubleshooting

### "Workflow not found" Error
- Ensure workflows are in `.github/workflows/` directory
- Check YAML syntax with: `yamllint .github/workflows/`
- Verify files have `.yml` extension

### Release Not Publishing
- Check `PYPI_API_TOKEN` is set correctly
- Verify tag format: `v1.2.3` (lowercase 'v')
- Ensure version doesn't exist on PyPI
- Check workflow logs for detailed errors

### CI Failing on Dependencies
- Update `requirements.txt` and `package.json`
- Check Python/Node version compatibility
- Verify FFmpeg is available in CI environment

### Security Scan False Positives
- Review vulnerability details carefully
- Check if vulnerability applies to your usage
- Consider using `# nosec` comments for Bandit
- Update to newer package versions

---

## Performance Tips

### Speed Up CI
- Caching is enabled automatically
- Use `fail-fast: false` for complete test coverage
- Run independent jobs in parallel
- Minimize dependencies in each job

### Reduce Costs
- Cancel redundant workflow runs (enabled by default)
- Use `if` conditions to skip unnecessary jobs
- Optimize Docker layer caching
- Use self-hosted runners for heavy workloads (advanced)

---

## Advanced Usage

### Run Specific Workflow Manually
```bash
# Using GitHub CLI
gh workflow run ci.yml

gh workflow run dependency-check.yml
```

### View Workflow Logs
```bash
# Using GitHub CLI
gh run list
gh run view <run-id> --log
```

### Download Artifacts
```bash
# Using GitHub CLI
gh run download <run-id>

# Or download from:
# GitHub → Actions → Workflow Run → Artifacts
```

---

## Resources

- [Full Workflow Documentation](.github/workflows/README.md)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [GitHub CLI](https://cli.github.com/)
- [PyPI Publishing](https://packaging.python.org/)

---

**Need Help?** Open an issue in the repository or check the workflow logs for detailed error messages.
