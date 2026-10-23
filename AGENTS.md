# Project Guidance

## Remote web access

- Treat every HTML page, browser demo, and local web interface in this repository as a remote-accessible artifact.
- Do not rely on file URLs, a graphical desktop, localhost, or 127.0.0.1 as the only access path.
- For static content, use scripts/serve-web.sh. Its default host must remain 0.0.0.0 so the remote machine can serve pages through a reachable LAN or VPN IP.
- Document the launch command, port, and relative IP URL in the nearest relevant README. Do not hardcode an ephemeral host IP, credentials, or tokens in committed files.
- After changing a page or server entrypoint, verify that it serves an HTTP response and that its static assets resolve through the same server root.
- Binding to 0.0.0.0 does not bypass firewall, VPN, SSH forwarding, or organizational network policy; state these external requirements clearly instead of adding a workaround.

## Repository layout

- Each top-level directory is an independent learning domain. Create experiment or course directories under it following the conventions in the root README (README + notes + src + tests).
- machine-learning/ keeps the former standalone repository's internal structure, conventions, and .gitignore. Pre-rebuild history remains in the private archive; this repository starts from one reviewed source snapshot.
- Every experiment README must record learning goals, resource provenance, environment and dependencies, run commands, and conclusions or reflections.
- Reusable cross-domain helpers go to shared/; domain-specific helpers stay inside their domain (for example machine-learning/shared/).
- Do not commit sensitive data, credentials, model weights, or large generated artifacts.

## Teaching workspaces

- Each learning track is a public teaching workspace following machine-learning/deep-learning/language-modeling-from-scratch/: a generic MISSION.md, RESOURCES.md, lessons/, reference/, and hands-on project directories. Keep personal notes, progress records, private device budgets and work-project context outside the repository.
- Lessons and reference pages must stay remotely browsable (see Remote web access) and link assets with relative paths only.
- Reuse is the default: build new lessons from the root assets/ component library first; add track-specific components under the track's own assets/.
- Number lessons and learning records sequentially (0001-, 0002-, ...); never renumber or reuse numbers of existing files.
- Ground every non-trivial claim in a lesson with a citation, and record the source in the track's RESOURCES.md when first used.
