# Lessons Learned

## Workflow Automations
- **Issue:** Scheduled GitHub Action tasks (like daily cron jobs for membership updates) run unconditionally. This consumes unnecessary CI minutes and generates redundant runs when there are no new content updates to necessitate a fresh member ranking pull.
- **Solution:** Switched the `update_members.yml` workflow to be event-driven. Triggering the workflow only on `push` to `index.html` or `_posts/**` ensures that the member roster is recalculated exactly when the website content is actively changing. This saves compute resources and elegantly aligns the update cadence with the actual site activity.
