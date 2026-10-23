# Project Guidance

## Remote web access

- Treat every HTML page, browser demo, and local web interface in this repository as a remote-accessible artifact.
- Do not rely on file URLs, a graphical desktop, localhost, or 127.0.0.1 as the only access path.
- For static content, use scripts/serve-web.sh. Its default host must remain 0.0.0.0 so the remote machine can serve pages through a reachable LAN or VPN IP.
- Document the launch command, port, and relative IP URL in the nearest relevant README. Do not hardcode an ephemeral host IP, credentials, or tokens in committed files.
- After changing a page or server entrypoint, verify that it serves an HTTP response and that its static assets resolve through the same server root.
- Binding to 0.0.0.0 does not bypass firewall, VPN, SSH forwarding, or organizational network policy; state these external requirements clearly instead of adding a workaround.
