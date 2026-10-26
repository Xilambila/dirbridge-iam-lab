# DirBridge IAM Lab

A local Flask prototype for previewing identity provisioning requests, with a documented security review and regression tests.

**Status:** runnable lab. It does not provision accounts, connect to Active Directory or Microsoft Entra ID, assign licenses, or generate passwords. Use synthetic data only.

## Security engineering showcase

This repository demonstrates reviewing an existing prototype, identifying risk, reducing the attack surface, and proving specific fixes with tests. It is relevant to IAM, secure automation, vulnerability remediation, and security engineering.

| Reviewed behavior | Change | Evidence |
|---|---|---|
| Password derived from names and employee ID, then displayed | Removed credential generation and display | Preview regression test; code review |
| Form values interpolated into raw HTML | Jinja HTML templates with escaping and input validation | Markup rejection and quote escaping tests |
| Missing fields could raise exceptions | Explicit validation with a generic 400 response | Missing, oversized and invalid input tests |
| Production capabilities implied by README | Current behavior and integration gaps stated explicitly | This README and threat model |
| No request size or host constraints | Small request limits, trusted local hosts, restrictive response headers | Body limit, host and header tests |

See the [case study](docs/iam-security-review.md) for scope, decisions, limitations, and verification commands. These are lab changes; no production deployment or business outcome is claimed.

## Run locally

Python 3.11 or newer:

```sh
git clone https://github.com/Xilambila/dirbridge-iam-lab.git
cd dirbridge-iam-lab
python -m venv .venv
```

Activate with `.venv\Scripts\Activate.ps1` on Windows or `source .venv/bin/activate` on Linux/macOS, then:

```sh
python -m pip install -r requirements.txt
python -m flask --app app.app run --host localhost --port 5000
```

Open `http://localhost:5000`. Example input: `Demo`, `User`, `LAB-001`. The optional address ends in `example.invalid`. Debug mode is not required. The development server is for local lab use.

```sh
python -m unittest discover -s tests -v
```

## Repository structure

```text
app/app.py                 Request validation and preview only
app/templates/             Escaped HTML presentation
docs/iam-security-review.md Findings, controls and production gaps
tests/test_security.py     Security regression tests
requirements.txt           Direct dependency version
```

The original empty `Dockerfile` and `run.sh` are retained as placeholders; container execution is not implemented.

## Before any real integration

Authentication, authorization, approval workflow, identity matching, collision handling, idempotency, directory permission scoping, protected audit events, secret storage, lifecycle reversal, transport protection, and operational monitoring must be designed and tested. No domain admin permission should be granted to this preview application. See [SECURITY.md](SECURITY.md).

Dependency note: the direct Flask version is pinned; transitive dependencies are not a complete locked or audited software bill of materials.
