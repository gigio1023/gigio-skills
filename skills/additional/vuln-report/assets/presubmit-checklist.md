# Pre-submission Checklist

Walk this after `scripts/check_report.py` and before handing the package to the person who submits. A line that cannot be ticked is an open item for the user, not something to paper over.

## Venue

- [ ] The target's security policy, form, non-vulnerability list, and threat model were read today, and the report follows the channel they name (`curl-policy`, `node-security`, `kernel-policy`, `github-pvr`).
- [ ] The target's published advisories were read for conventions such as CWE choice, severity habit, range syntax, and credit style; the body sections follow the reporting form and the skeleton (`ghsa-mcp-python-sdk`, `ghsa-fastmcp`).
- [ ] The finding crosses a boundary the project defends, and the report says what the attacker gains beyond what they already had (`cert-credibility`, `google-attack-scenario`).
- [ ] Published advisories, issues, pull requests, and the prior fix were searched for duplicates (`local`).

## Claims

- [ ] The title and first block state the flaw, trigger, and demonstrated result, and claim nothing beyond the evidence (`ghsl-advisories`, `curl-h1-uaf`).
- [ ] Every present-tense capability was executed and observed; source-only claims say so in the same sentence (`ghsa-nginx-ui`, `chromium-vrp-faq`).
- [ ] Every quoted line matches the source at the pinned tag or commit, with omissions marked (`h1-curl-socks5`, `local`).
- [ ] Every number in the text matches the attachment it cites (`local`).
- [ ] Each measured result appears in the field that owns it, with the summary carrying only the headline result; each "not tested" note limits a claim the report makes and appears once; pointers name a heading (`ghsa-vllm`, `local`).
- [ ] Preconditions are listed, including whether the default configuration is affected, and what is not affected is stated (`p0-report-2026`, `ghsa-vllm`).
- [ ] Undemonstrated chains are in their own conditional sentences (`p0-report-2026`, `kernel-policy`).
- [ ] Severity follows the venue: absent when the policy says so; when given, a full vector with its version, reasons for disputable metrics, and the label reporter's estimate, never a bare number (`django-policy`, `openssf-template`, `cvss31-guide`).
- [ ] CWE is a Base or Variant entry that names the root cause and agrees with the narrative and vector (`cwe-mapping`, `ghsa-faraday`).

## Versions

- [ ] The tested release or commit and environment are exact (`kernel-policy`, `ghsa-mlflow`).
- [ ] Any proposed range is labeled an estimate, separates executed, source-compared, and unknown, and uses the venue's syntax (`github-advisory-docs`, `cve-key-details`).
- [ ] The issue was confirmed on the latest release or the development tree, at least by showing the code is unchanged (`kernel-policy`, `apple-guidelines`).

## Reproduction and evidence

- [ ] The person, or a fresh agent in the same harness with the user's approval, reproduced it from the report and attachments alone, or the open items say it was not done (`google-reproduce`, `local`).
- [ ] Any independent read through `review-panel` happened only on the user's request or agreement, after the user was told that each reviewer's model provider receives the unfixed details (`local`).
- [ ] Setup and attack steps are separate and name the identity for each (`reddit-survey`, `larson-slop-2024`).
- [ ] Controls show the boundary holds through the normal path (`h1-node-smuggling`, `ghsa-vllm`).
- [ ] Any verdict printed by a script depends on a signal only the flaw produces; generic errors count as inconclusive (`chromium-vrp-faq`, `ghsa-mlflow`).
- [ ] The PoC is minimal and harmless, and nothing touched systems or data the user is not authorized for (`node-security`, `bugcrowd-guide`).
- [ ] Each attachment is named in the text, and its SHA-256 is recorded for the bytes being sent (`local`).
- [ ] Evidence contains no home paths, user or host names, internal addresses, tokens, or other people's data (`local`, `ghsa-mlflow`).
- [ ] The checker's coverage summary shows every attached file as scanned; anything skipped, partial, or in error was unpacked, decrypted, or read by hand (`local`).
- [ ] Attachments follow the venue's packaging rule (`chromium-vrp-faq`, `kernel-policy`).
- [ ] No recording is implied unless it exists; the environment is kept for re-runs and a recording on request (`cert-credibility`, `local`).

## Disclosure and privacy

- [ ] The tooling paragraph says what tools and AI did and what the person verified, and the form's AI checkbox matches (`curl-ai-policy`, `github-pvr`).
- [ ] The person who submits has read the report and patch and run the PoC, and has rewritten the text where the policy asks for the reporter's own words, or the open items say what remains (`curl-ai-policy`, `local`).
- [ ] Nothing about the unfixed issue is in a public place, including a public pull request for the patch (`curl-policy`, `github-pvr`).
- [ ] Separate findings are not mixed into this report or its attachments (`django-policy`, `msrc-faq`).
- [ ] Credit preference and availability for questions are stated (`curl-h1-uaf`, `kernel-policy`).

## After every edit

- [ ] The checker and this list were run again on the final text, and attachments were rebuilt and re-hashed (`local`).
