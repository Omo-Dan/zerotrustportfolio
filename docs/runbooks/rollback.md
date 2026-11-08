# Rollback runbook

Requirements: HE-06 (any release can be rolled back to the previous version quickly), AC-15 (a broken release is restored from the pipeline within minutes). Threat: T-21.

A rollback restores the last known-good release. It is deliberately boring: the steps are short, and the decision to roll back does not wait for a diagnosis.

## When to roll back

Roll back first and investigate afterwards if a release is live and any of these is true:

- `/healthz` fails, or `/version` does not answer after a deploy has finished.
- A page returns an error or renders visibly broken.
- A security header has disappeared from the responses.
- A secret or a private detail has been published. A rollback removes it from the live site but does not undo the exposure, so rotate the secret as well.

A rollback costs minutes. Debugging a fault on the live site costs more, and visitors see it the whole time.

## Standard path

This is the default. It goes through the pipeline, so the protections on `main` stay in force and the rollback is recorded like any other change.

1. Find the bad commit on `main`: `git switch main && git pull`, then `git log --oneline`.
2. Create a branch: `git switch -c revert/<short-description>`.
3. Revert the commit with a signed commit: `git revert -S <commit>`. If the commit is a merge commit, add `-m 1`.
4. Push the branch and open a pull request. Cite HE-06 and AC-15. All six required checks run on it.
5. Merge when the checks are green. The deploy workflow deploys the result and polls `/version` until it shows the new commit.

The time this takes is mostly the time the checks take. The drill log below records the measured figure.

Note that `/version` will show the revert commit, not the original one. The content matches the previous release, but the commit id is new.

## Fast path

Use this only when waiting for the checks would cost more than skipping them.

1. In the Render dashboard, open the service and its Deploys page.
2. Find the last successful deploy that was known to be good and choose Rollback, then confirm.
3. Render starts a new deploy from the stored build of that release. It skips the build step, so it finishes sooner than a normal deploy.

What this changes, and what it does not:

- It bypasses the pull request and the required checks. Record the reason in the incident notes.
- A rollback from the dashboard turns off autodeploys for the service, so a new commit cannot bring the fault back.
- `main` still contains the bad commit. Follow with a revert through the standard path straight away so that the repository matches production.
- After the fix has merged, re-enable autodeploys in the service settings if they were on.
- Rollback depends on Render still holding the build of the earlier deploy. Check the Deploys page before relying on this path.

After a fast rollback, `/version` shows the older commit id.

## Verify

A rollback is finished when production is checked, not when the button is pressed.

1. `curl -sS https://zerotrustportfolio.onrender.com/version` shows the expected commit. After a standard rollback that is the revert commit. After a fast rollback it is the older release.
2. `curl -sS https://zerotrustportfolio.onrender.com/healthz` returns a healthy response.
3. Open Home, About, Projects, Skills and Certifications and check that each loads with its styles.
4. Check the security headers are present: `curl -sI https://zerotrustportfolio.onrender.com/`.

The service can sleep when idle. Allow up to about 90 seconds for the first request after a deploy.

## Drill log

Each drill is recorded here: the date, the path used, what was shipped, how long it took from the decision to roll back until `/version` and `/healthz` were healthy, and anything that went wrong.

| Date | Path | Scenario | Time to healthy | Notes |
| --- | --- | --- | --- | --- |