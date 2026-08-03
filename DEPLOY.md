Deployment
----------

This repository contains a web client under the `javascript/` directory. The repository includes a GitHub Actions workflow that publishes the contents of `javascript/` to the `gh-pages` branch on every push to `main`.

How it works
- The workflow `.github/workflows/gh-pages.yml` runs on push to `main`.
- It uses `peaceiris/actions-gh-pages` to publish `./javascript` to the `gh-pages` branch.

After the workflow runs, your site will be available at:

- https://<username>.github.io/<repository>

Notes
- If Pages isn't already enabled, visit the repository Settings → Pages and ensure the Site is served from the `gh-pages` branch.
- If you prefer to serve from the `docs/` folder on `main`, I can instead copy the site into `docs/` and switch the workflow.
