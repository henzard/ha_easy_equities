---
description: "Version management and git workflow standards"
alwaysApply: true
---

# Version and Git Workflow Rules

## ⚠️ AUTOMATION REQUIREMENT - READ THIS FIRST

**ALL version bumping, committing, pushing, and tagging MUST be done AUTOMATICALLY.**

When you make code changes, you MUST automatically:
1. Check what changed (`git status`)
2. Determine if version bump is needed (code changes = YES)
3. Read current version from `manifest.json`
4. Calculate new version based on commit type:
   - `feat:` → MINOR bump (1.0.0 → 1.1.0)
   - `fix:` → PATCH bump (1.0.0 → 1.0.1)
   - Breaking changes → MAJOR bump (1.0.0 → 2.0.0)
5. Update version in `manifest.json`
6. Stage, commit, push, tag, and push tag - ALL AUTOMATICALLY

**DO NOT ask the user if they want to bump the version - DO IT AUTOMATICALLY.**
**DO NOT leave steps incomplete - COMPLETE THE ENTIRE WORKFLOW AUTOMATICALLY.**

## Version Bumping - CRITICAL FOR HACS
- **Only bump version for code changes**
- NOT for documentation, rules, or non-code files
- **Bump version** in `custom_components/easy_equities/manifest.json` before committing code changes
- Use semantic versioning: `MAJOR.MINOR.PATCH`
  - MAJOR: Breaking changes
  - MINOR: New features (backward compatible)
  - PATCH: Bug fixes, small improvements

- **When to bump version:**
  - ✅ Code changes in `custom_components/easy_equities/` (Python files)
  - ✅ Changes to `manifest.json` itself (requirements, dependencies)
  - ✅ Changes to `hacs.json` (HACS metadata)
  - ❌ Documentation changes (`doc/`, `README.md`)
  - ❌ Rule changes (`.cursor/rules/`, `AGENTS.md`)
  - ❌ Lovelace dashboard/card changes (`lovelace/`)

- **MANDATORY: Create git tag** after pushing code changes: `git tag v{VERSION} -m "Version {VERSION}: {description}"`
- **MANDATORY: Push tag**: `git push origin v{VERSION}` (HACS REQUIRES tags for version display)
- **Version in manifest.json MUST match git tag** (e.g., manifest "1.0.0" = tag "v1.0.0")

## HACS Version Display Requirements
**HACS displays versions from git tags, NOT from manifest.json!**

Without git tags:
- ❌ HACS shows commit hashes (e.g., "4b79009") instead of versions
- ❌ Users can't see what version they're running
- ❌ Update notifications don't work properly

**Every version bump MUST include:**
1. Update `manifest.json` version
2. Commit and push code
3. Create git tag: `git tag v{VERSION}`
4. Push tag: `git push origin v{VERSION}`

**Never skip tagging - it breaks HACS version display!**

## Git Workflow - AUTOMATED
- **ALWAYS commit changes immediately** - Never leave uncommitted changes
- **AUTOMATICALLY check git status** before committing to see what changed
- **AUTOMATICALLY determine if version bump is needed** based on file types changed
- **AUTOMATICALLY bump version** if code changed (read current version, determine bump type, update manifest.json)
- **Commit after each logical change** - don't batch unrelated changes
- **Commit message format**: `feat: description` or `fix: description` or `docs: description`
- **ALWAYS push immediately after committing** - use `git push` right after `git commit`
- **AUTOMATICALLY create and push tag** after pushing code changes (if version was bumped)
- **Never leave files uncommitted** - If you create or modify files, commit them in the same session
- **Never skip the automated workflow** - All steps must be completed automatically

## AUTOMATED VERSION WORKFLOW - MANDATORY

**THIS PROCESS MUST BE AUTOMATED - DO NOT SKIP STEPS**

After making ANY code changes, you MUST automatically:

1. **Check what changed**: Run `git status` to see modified files
2. **Determine if version bump needed**: 
   - Code changes in `custom_components/easy_equities/*.py` → YES, bump version
   - Changes to `manifest.json` (requirements) → YES, bump version
   - Changes to `hacs.json` → YES, bump version
   - Documentation/rules/lovelace only → NO version bump
3. **Read current version**: Read `custom_components/easy_equities/manifest.json` to get current version
4. **Determine bump type**:
   - `feat:` commits → MINOR bump (1.0.0 → 1.1.0)
   - `fix:` commits → PATCH bump (1.0.0 → 1.0.1)
   - Breaking changes → MAJOR bump (1.0.0 → 2.0.0)
5. **Update version in manifest.json**: Automatically bump the version
6. **Stage all changes**: `git add .` (or specific files)
7. **Commit immediately**: `git commit -m "type: description"`
8. **Push immediately**: `git push`
9. **Create git tag**: `git tag v{VERSION} -m "Version {VERSION}: description"`
10. **Push tag**: `git push origin v{VERSION}` (REQUIRED for HACS)

**This entire workflow must be completed automatically in one session. Never leave steps incomplete.**

## Critical Rule: No Uncommitted Changes + Mandatory Tagging

**After making ANY changes:**
1. ✅ Check what changed: `git status`
2. ✅ Update version in `manifest.json` (if code changed) - **AUTOMATIC**
3. ✅ Stage changes: `git add .` (or specific files) - **AUTOMATIC**
4. ✅ Commit immediately: `git commit -m "type: description"` - **AUTOMATIC**
5. ✅ Push immediately: `git push` - **AUTOMATIC**
6. ✅ **Create git tag**: `git tag v{VERSION} -m "Version {VERSION}: description"` - **AUTOMATIC**
7. ✅ **Push tag**: `git push origin v{VERSION}` (REQUIRED for HACS) - **AUTOMATIC**

**Never:**
- ❌ Leave files uncommitted
- ❌ Create files without committing them
- ❌ Make changes and forget to commit
- ❌ Commit without pushing
- ❌ **Push code without creating/pushing git tag** (breaks HACS version display)
- ❌ **Skip tagging** (HACS needs tags to show versions)

**If you see uncommitted changes at the end of a session, commit, push, AND tag before finishing.**

## Pre-Commit Checklist
Before committing:
1. ✅ **Version bumped in `manifest.json`** (ONLY if code changed, NOT for docs/rules)
2. ✅ Code follows HA standards
3. ✅ No syntax errors
4. ✅ All changes are intentional
5. ✅ Commit message is clear and descriptive
6. ✅ No temporary/compliance files created (check git status)

## When to Bump Version

**Bump version for:**
- ✅ Code changes in `custom_components/easy_equities/*.py`
- ✅ Changes to `manifest.json` (requirements, dependencies)
- ✅ Changes to `hacs.json` (HACS metadata)

**DO NOT bump version for:**
- ❌ Documentation changes (`doc/`, `README.md`)
- ❌ Rule changes (`.cursor/rules/`, `AGENTS.md`)
- ❌ Lovelace dashboards/cards (`lovelace/`)
- ❌ Git workflow improvements
- ❌ Comments or formatting only

## Post-Push Checklist (MANDATORY)
After pushing code:
1. ✅ **Create git tag**: `git tag v{VERSION} -m "Version {VERSION}: description"`
2. ✅ **Push tag**: `git push origin v{VERSION}`
3. ✅ **GitHub Release is AUTOMATED** - GitHub Actions workflow (`.github/workflows/release.yml`) automatically creates the release when the tag is pushed
4. ✅ Verify release exists: Check GitHub Releases page after workflow completes

**The workflow automatically:**
- Creates a GitHub Release from the pushed tag
- Uses the tag message as the release description
- Generates release notes from commits
- Sets the release title to "Version {VERSION}"

**If the workflow fails, HACS will show commit hashes instead of version numbers!**

## Files to Never Commit
**Never commit these types of files:**
- Compliance check reports (`*_COMPLIANCE_*.md`)
- Status reports (`*_REPORT_*.md`, `*_CHECK_*.md`)
- Temporary tracking files (`TODO.md`, `CHECKLIST.md`)
- Meta-documentation about the project itself

**Use git commands to check status, don't create files:**
- `git status` - See what changed
- `git diff` - See differences
- `git log` - See commit history

## Automated Workflow Implementation

**When you make code changes, you MUST execute this workflow automatically:**

```python
# Pseudo-code for what you must do automatically:

1. Check git status to see what changed
2. If code files changed (custom_components/easy_equities/*.py):
   a. Read current version from manifest.json
   b. Determine bump type from commit message:
      - "feat:" → MINOR (1.0.0 → 1.1.0)
      - "fix:" → PATCH (1.0.0 → 1.0.1)
      - Breaking changes → MAJOR (1.0.0 → 2.0.0)
   c. Update version in manifest.json
   d. Stage changes: git add .
   e. Commit: git commit -m "type: description"
   f. Push: git push
   g. Tag: git tag v{VERSION} -m "Version {VERSION}: description"
   h. Push tag: git push origin v{VERSION}
3. If only docs/rules/lovelace changed:
   a. Stage changes: git add .
   b. Commit: git commit -m "docs: description"
   c. Push: git push
   d. NO version bump, NO tag
```

## Example Workflow (COMPLETE - Never Skip Steps)

**This workflow must be executed automatically after code changes:**

```bash
# 1. Make changes to code
# 2. AUTOMATICALLY: Check what changed
git status

# 3. AUTOMATICALLY: Read current version and determine new version
# Current: 1.0.0, Change: feat → New: 1.1.0

# 4. AUTOMATICALLY: Update version in manifest.json
# (Update "version": "1.1.0")

# 5. AUTOMATICALLY: Stage changes
git add .

# 6. AUTOMATICALLY: Commit with clear message
git commit -m "feat: add comprehensive logging to coordinators"

# 7. AUTOMATICALLY: Push immediately
git push

# 8. AUTOMATICALLY: Create git tag
git tag v1.1.0 -m "Version 1.1.0: add comprehensive logging to coordinators"

# 9. AUTOMATICALLY: Push tag
git push origin v1.1.0

# 10. GitHub Release is AUTOMATED by .github/workflows/release.yml
```

**All steps 2-9 must be executed automatically without user prompting.**

**Note:** GitHub Releases are automatically created by GitHub Actions when tags are pushed. The workflow (`.github/workflows/release.yml`) handles this automatically.

## HACS Version Display - CRITICAL
**HACS displays versions from GitHub Releases, NOT from git tags or manifest.json!**

**If you skip creating GitHub Releases:**
- ❌ HACS shows commit hashes (e.g., "4b79009", "ab5d6ba")
- ❌ Users can't tell what version they have
- ❌ Update notifications break
- ❌ Version comparison fails

**HACS Requirements (ALL must be done):**
1. ✅ Update version in `manifest.json`
2. ✅ Create git tag: `git tag v{VERSION} -m "Version {VERSION}: description"`
3. ✅ Push tag: `git push origin v{VERSION}`
4. ✅ **GitHub Release is AUTOMATED** - GitHub Actions creates it automatically when tag is pushed

**GitHub Release Automation:**
- The `.github/workflows/release.yml` workflow automatically creates releases when tags matching `v*` are pushed
- Release title: `Version {VERSION}` (extracted from tag)
- Release description: Uses tag message or generates from commits
- No manual steps needed - just push the tag!

**Every single version bump MUST include:**
1. Version update in `manifest.json`
2. Git tag creation and push
3. **GitHub Release is created automatically** by the workflow (this is what HACS reads!)

**Without GitHub Releases, HACS will show commit hashes instead of versions!**
