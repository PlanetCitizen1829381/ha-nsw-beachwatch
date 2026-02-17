# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.2.x   | :white_check_mark: |
| < 1.2   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within the NSW Beachwatch integration, please send an email to the repository owner via GitHub. All security vulnerabilities will be promptly addressed.

**Please do not open public issues for security vulnerabilities.**

### What to Include in Your Report

- **Description:** A clear description of the vulnerability
- **Steps to Reproduce:** Detailed steps to reproduce the issue
- **Impact:** What could an attacker potentially do
- **Suggested Fix:** If you have ideas on how to fix it (optional)

### Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Within 7 days
- **Fix Release:** Depends on severity (critical issues within 24-48 hours)

### After the Fix

Once the vulnerability is fixed:
1. We will release a new version with the security patch
2. We will publish a security advisory on GitHub
3. We will credit you in the release notes (unless you prefer to remain anonymous)

## Security Best Practices for Users

When using this integration:

1. **Keep Updated:** Always use the latest version available in HACS
2. **Monitor Releases:** Watch the repository for security updates
3. **Review Logs:** Check Home Assistant logs for any unusual API activity
4. **Network Security:** Ensure your Home Assistant instance is properly secured

## Data Privacy

This integration:
- Only communicates with the official NSW Beachwatch API
- Does not store or transmit any personal data
- Does not require authentication or API keys
- All communication is read-only (no data is sent to the API)

## Third-Party Dependencies

This integration uses the following dependencies:
- Home Assistant Core (minimum version 2024.1.0)
- Python standard library only

Dependencies are managed through Home Assistant's manifest.json and are regularly reviewed for security updates.

## Contact

For security concerns, please use GitHub's private security advisory feature or email the repository owner directly through GitHub.

For general issues (non-security), please use the [GitHub Issues](https://github.com/PlanetCitizen1829381/ha-nsw-beachwatch/issues) page.
