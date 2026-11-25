# Exemplar Catalog

Every rule in this skill names one or more source IDs. This file resolves each published source ID to its URL and records what was extracted from it; `reddit-survey` and `local` have no URL and are described in their own sections. Read it when a rule is questioned, when two rules seem to conflict, when a venue is not covered in [venue formats](venue-formats.md), or before changing a rule. All sources were read on 2026-10-14 unless an entry says otherwise. Text is paraphrased; section names, field names, and syntax are given exactly because they are identifiers.

Reading method matters for confidence. "Full text" means the raw file, an API body, or the rendered page read in a browser; "summary" means a fetch tool's model summary, confirmed by a second fetch where marked. Kind 1 to 5 follow the survey design: report originals, research-team advisories, receiving-side guidance, record formats, and accepted advisories in Python and agent tooling.

## Contents

- Report originals and near-originals
- Research-team advisories and write-ups
- Receiving-side guidance
- Record formats
- Accepted advisories in Python and agent tooling
- Community evidence
- Source disagreements
- Local decisions
- Limits of this catalog

## Report originals and near-originals

These show what a report looked like when it reached the receiver, before any publisher edited it.

### `p0-report-2026`

- **Source:** [Project Zero issue 514643907](https://project-zero.issues.chromium.org/issues/514643907), full text in a browser. Reported 2026-05-19, fixed 2026-06-09, opened after the bulletin.
- **Use for:** a long private report to a vendor that separates observation from cause.
- **Headings:** BACKGROUND, VULNERABILITY DETAILS, TECHNICAL ANALYSIS, REACHABILITY AND ATTACK VECTORS, VERSION, REPRODUCTION, IMPACT, SUGGESTED FIX, CREDIT INFORMATION, DISCLOSURE DEADLINE, with noun-phrase subheadings such as trigger conditions.
- **First block:** two or three sentences of background for a triager outside the area, then the flaw class, file, function, and missing check, contrasted with a sibling path in the same file that has the check.
- **Version:** one line under VERSION with SDK version, build, and date.
- **Reproduction:** a table of the attached PoC files, commands with actual output, repeated runs, and a controlled experiment that varies input bytes to confirm the causal chain.
- **Impact:** labeled items; demonstrated effects stated plainly, possibilities marked with may or potentially, chained effects carry their condition in the sentence.
- **Severity:** none in the body; the tracker's priority and severity fields belong to the team.
- **Fix:** options A, B, C with the root fix marked as recommended and the others as defense in depth.
- **Limits:** a list of trigger conditions that must all hold; affected and unaffected paths separated; a possible repeat of the pattern elsewhere is a suggestion to review, not a claim.

### `p0-report-2022`

- **Source:** [Project Zero issue 42451541](https://project-zero.issues.chromium.org/issues/42451541), full text in a browser. Reported 2022-12-19.
- **Use for:** the short form of a private report.
- **Shape:** three opening sentences give the flaw, that no user interaction is needed, and the device and build tested; one sentence says it did not reproduce on another device; six numbered steps, expected result, attachment, deadline notice.

### `p0-policy`

- **Source:** [disclosure policy](https://projectzero.google/vulnerability-disclosure-policy.html), [FAQ](https://projectzero.google/vulnerability-disclosure-faq.html), [reporting transparency](https://projectzero.google/reporting-transparency.html), summaries.
- **Use for:** deadline conventions. Disclosure 90 days after report, or 30 days after a patch ships; 7 days for bugs exploited in the wild; a 14-day grace period. The initial report carries the technical detail and the deadline notice.

### `curl-h1-uaf`

- **Source:** [HackerOne report 4030333](https://hackerone.com/reports/4030333), full text in a browser; [project lead's post on it](https://daniel.haxx.se/blog/2026/10/14/a-uaf-turned-rce/). Submitted 2026-09-15, disclosed 2026-10-14.
- **Use for:** a reporter-written OSS report whose severity the maintainer corrected.
- **Headings:** Summary, Affected version, Steps To Reproduce, Appendix, Impact; attachments were a server script, a video, and an archive with a Docker build and a proposed patch.
- **First block:** the behavior, then the result, then preconditions split into those needed to trigger and those needed to exploit.
- **Version:** one tested version; the published CVE page later carried the range.
- **Reproduction:** one code block of shell commands from source download and checksum through sanitizer build, server start, a single client command, and the expected result.
- **Impact and severity:** the submitted title and one-line impact claimed remote code execution; the maintainer listed the required conditions, moved the severity field from Critical to High, and retitled it; the reporter agreed.
- **Credit and tooling:** the reporter asked for a credit line; the published Reported-by line names the person and the model used. Tooling came out in later comments, not in the body.

### `h1-gitlab-file-read`

- **Source:** [HackerOne report 827052](https://hackerone.com/reports/827052), full text via the JSON endpoint and a browser. Submitted 2020-03-23, disclosed 2020-04-27; NVD maps it to CVE-2020-10977.
- **Use for:** a program template report and post-triage escalation.
- **Headings:** Summary, a video, Steps to reproduce, Impact, then the program template's current behavior, expected behavior, and output of checks with the environment dump.
- **First sentence:** component, flaw, result, and trigger in one sentence; attacker privilege not stated.
- **Version:** only the tested version, as a full environment dump; the range came from the vendor. A comment nine minutes later showed the hosted service was also affected.
- **Impact:** one sentence in the body; a later comment escalated to code execution with command output as proof.
- **Severity:** the platform field was set to Critical by the reporter.

### `h1-curl-socks5`

- **Source:** [HackerOne report 2187833](https://hackerone.com/reports/2187833), body via JSON, comments partly read in a browser. Created 2023-09-30, CVE-2023-38545. The reporter may be affiliated with the project; not verified.
- **Use for:** conditions-first opening, pinned code references, and an overclaim withdrawn in discussion.
- **Headings:** Summary, Walkthrough, Steps To Reproduce, Supporting Material/References, Solution, Impact.
- **First sentence:** a remote attacker can overflow a heap buffer if four listed conditions hold; root cause and a concrete scenario follow.
- **Version:** every code reference is a permalink pinned to a release tag with line ranges; no range claimed. Discussion later limited the published analysis to one major version.
- **Reproduction:** a code walkthrough, crash output, the arithmetic behind a guard message, one-line server and client commands, and a debug patch that forces the timing.
- **Impact:** default and non-default buffer sizes compared with arithmetic to show which configurations are affected.
- **Thread:** the maintainer showed one claimed consequence was impossible; the reporter agreed and the paragraph was removed.
- **Register:** impersonal present tense; first person only for opinions.

### `h1-node-smuggling`

- **Source:** [HackerOne report 1238099](https://hackerone.com/reports/1238099), body via JSON; comments not read. Created 2021-06-19, CVE-2021-22960.
- **Use for:** a baseline control before the attack.
- **Shape:** bold Summary and Description labels, then Steps To Reproduce and Impact. The first sentence gives component, tested version, and flaw; the second gives the result and the deployment condition.
- **Reproduction:** a docker-compose PoC archive, transcripts showing the protected path is blocked through the proxy, the attack command, and a log line printed only when the protected path is reached.
- **Impact:** states the limit, that the smuggling is blind, next to the capability, and frames the result as an access-control bypass only where the proxy enforces access.

### `bmo-webgl`

- **Source:** [Mozilla bug 1841050](https://bugzilla.mozilla.org/show_bug.cgi?id=1841050), all 37 comments via the REST API. Filed 2023-06-29 by an external reporter, CVE-2023-6204.
- **Use for:** form-field reports and what happens when reproduction conditions are missing.
- **Shape:** Bugzilla fields User Agent, Steps to reproduce, Actual results, Expected results; the root-cause analysis landed under Actual results and the impact under Expected results.
- **Severity:** none from the reporter; the vendor set it and explained it in a comment.
- **Thread:** the developer could not reproduce at first and asked for a crash report and environment details, then found the missing conditions; the reporter retested the fix build.

### `oss-qualys-regresshion`

- **Source:** [oss-security 2024/07/01/3](https://www.openwall.com/lists/oss-security/2024/07/01/3), full text. Qualys, 2024-07-01, CVE-2024-6387.
- **Use for:** a public post after coordinated release, and separating tested targets from the affected range.
- **Headings:** Contents, Summary, one section per tested server banner with theory, practice, and timing, an architecture section, Patches and mitigation, Acknowledgments, Timeline. Epigraphs open each section.
- **Version:** the range in three intervals with the introducing commit and regression history; tested targets given separately as exact banners and images; platform scope with a reason one platform is not affected.
- **Reproduction:** no PoC; attempt counts and time to success per target with the settings used.
- **Impact:** demonstrated on one architecture; another stated as believed, not demonstrated; test conditions named.
- **Fix:** upstream commit, a minimal patch, and a configuration workaround with its trade-off.
- **Timeline:** `YYYY-MM-DD: We ...`, one event per line, ending at the coordinated release date. Plain text at 72 columns, no bold.

### `oss-suse-screen`

- **Source:** [oss-security 2025/05/12/1](https://www.openwall.com/lists/oss-security/2025/05/12/1), full text. A distribution security team, 2025-05-12.
- **Use for:** several findings in one post, per-version and per-distribution scope, and a frank disclosure history.
- **Headings:** Introduction; configurations and versions; issues 3.a to 3.f each with Bugfix and Affected Distributions; possible further issues; general recommendations; the coordinated disclosure process and upstream status; an affectedness matrix; Timeline; References.
- **Version and impact:** each issue states which releases and install modes are affected; consequences differ per distribution; one issue is judged not a security bug but worth fixing.
- **Reproduction:** prompt-labeled transcripts; a race is reported with its success rate.
- **Limits:** unclear purpose of one code path, unclear upstream status, suspected but unconfirmed issues.

### `ghsl-advisories`

- **Source:** [GitHub Security Lab advisories index](https://securitylab.github.com/advisories/), and [GHSL-2026-072](https://securitylab.github.com/advisories/GHSL-2026-072_Orchard_CMS/), [GHSL-2026-065](https://securitylab.github.com/advisories/GHSL-2026-065_Umbraco_CMS/), [GHSL-2026-105](https://securitylab.github.com/advisories/GHSL-2026-105_Signal-iOS/), summaries confirmed on key facts. Published 2026-09-21 after patches.
- **Use for:** a research team's advisory skeleton and an argument that behavior is unintended.
- **Headings:** title with ID and one-line summary, Coordinated Disclosure Timeline, Summary, Project, Tested Version, Details with per-issue subsections such as attack scenario and proof of concept, Impact, CWEs, Credit, Contact.
- **First block:** product first, then the flaw in one declarative sentence.
- **Version:** a single tested value, a development commit or a release tag; no range expression.
- **Reproduction:** numbered attack scenario with attacker profile, target, steps, result, and request blocks with headers and JSON bodies.
- **Severity:** no CVSS; CWE listed separately.
- **Limits:** one advisory compares the path with its sibling delete path to argue the behavior is not intended.
- **Credit:** the discovery tool and the person who verified manually are both credited.

### `ghsl-taskflow`

- **Source:** [GitHub blog on the Security Lab taskflow agent](https://github.blog/security/ai-supported-vulnerability-triage-with-the-github-security-lab-taskflow-agent/), 2026-01-20, summary.
- **Use for:** a research team stating that a person reviews every model-generated finding before it is reported.

## Research-team advisories and write-ups

These are published after a fix or a deadline. Their Timeline, Credit, and lesson sections are filled in by the publisher; a private report carries only the dates its writer knows.

### `qualys-snap-confine` and `qualys-crackarmor`

- **Source:** [snap-confine advisory](https://cdn2.qualys.com/advisory/2026/03/17/snap-confine-systemd-tmpfiles.txt) and [CrackArmor advisory](https://cdn2.qualys.com/advisory/2026/03/10/crack-armor.txt), plain text, summaries.
- **Use for:** finding-first summaries and analysis separated from exploitation.
- **Shape:** Summary states the result on a default install, then the cause. Case studies split Analysis from Exploitation transcripts. A note keeps "still vulnerable" separate from "mitigated by a vendor change". No CVSS; a missing CVE is stated as missing. Acknowledgments in prose; Timeline in ISO dates with the actor as subject. Playful titles and epigraphs are this team's public convention.

### `zdi-advisory`

- **Source:** [ZDI-26-750](https://www.zerodayinitiative.com/advisories/ZDI-26-750/) and [ZDI-26-756](https://www.zerodayinitiative.com/advisories/ZDI-26-756/), raw HTML. Published 2026-09-30.
- **Use for:** a fixed-formula advisory.
- **Fields:** title, date, ZDI ID, ZDI-CAN ID, CVE, CVSS score with vector, affected vendors and products, Vulnerability Details, Additional Details, Disclosure Timeline, Credit.
- **Formula:** the title runs vendor, product, component, flaw class, impact. The body's four sentences say what remote attackers can do, whether authentication is needed, where the flaw is, and that it results from missing validation, then the execution context.
- **Severity:** the publisher sets CVSS 3 with vector. Fix is one line pointing at the vendor update; the 0-day variant lists vendor contact attempts and a one-line mitigation.

### `talos-report`

- **Source:** [TALOS-2026-2414](https://talosintelligence.com/vulnerability_reports/TALOS-2026-2414), raw HTML. Published 2026-10-07.
- **Use for:** a summary formula and code excerpts with numbered markers.
- **Headings:** CVE Number, Summary, Confirmed Vulnerable Versions, Product URLs, CVSSv3 Score, CWE, Details, Timeline, Credit.
- **Summary:** a flaw class exists in a function of a product at a version; a crafted input leads to the impact; the attacker delivers it in a stated way.
- **Version:** a fixed sentence that listed versions were tested by the team or confirmed by the vendor, then a development commit.
- **Details:** bracketed markers inside code excerpts referenced from the prose; explains why a standard library protection does not apply.
- **Impact:** bounded by required user interaction, with a realistic workflow argument.

### `ncc-libssh`

- **Source:** [NCC Group technical advisory, libSSH authentication bypass](https://www.nccgroup.com/research/technical-advisory-authentication-bypass-in-libssh/), full text in a browser. 2018-10-17.
- **Use for:** a key-value header and impact bounded in both directions.
- **Shape:** Vendor, Versions affected, Author, CVE, Risk, then Summary, Location, Impact, Details, Recommendation, Vendor Communication. The headings do not match their content: the flaw sits under Location.
- **Version:** affected range only, no tested version. Impact says not every server is vulnerable to the bypass, yet every server should update for a second reason.

### `doyensec-chrome-ios` and `doyensec-ovs`

- **Source:** [Chrome for iOS prompt bypass](https://blog.doyensec.com/2026/09/24/chrome-ios-policy-bypass.html), 2026-09-24, and [Open vSwitch post](https://blog.doyensec.com/2026/09/17/ovs.html), 2026-09-17, raw HTML; the second partly skimmed.
- **Use for:** preconditions first, and disclosure of AI assistance in a public write-up.
- **Shape:** TL;DR, background, mechanism, Security impact, Remediation, References. The first post gives neither tested version nor range and bounds the final effect by platform, app, and URL. The second leads its TL;DR with every precondition, lists three preconditions in their own section, shows before and after probe output to confirm the mechanism, states that one distribution's default configuration is not exploitable, gives three mitigations with trade-offs, credits prior work for the technique, names the AI assistant used, and says an automated review found a sibling path the first patch missed.

### `wiz-ingress`

- **Source:** [IngressNightmare](https://www.wiz.io/blog/ingress-nginx-kubernetes-vulnerabilities), raw HTML. 2025-03-24 with a later update.
- **Use for:** the public, branded write-up style and its risks.
- **Shape:** product, The Vulnerability, Mitigation and Detection, discovery, background, one section per CVE, the chain to code execution, Conclusions, Responsible Disclosure Timeline, product promotion, Update. Opens with a brand name, CVSS 9.8, and exposure statistics. One CVE section contradicts its own title, likely a copy error. Timeline in active voice includes reported bypasses of proposed fixes.

### `snyk-entry`

- **Source:** [SNYK-JS-LODASH-567746](https://security.snyk.io/vuln/SNYK-JS-LODASH-567746), raw HTML. 2020-04-28.
- **Use for:** a database entry: flaw class, package, and semver range in the title; fix version in How to fix; a three-line PoC with expected output as a comment; three scores from three sources side by side.

### `tob-writeup` and `tob-report-anatomy`

- **Source:** [Trail of Bits post](https://blog.trailofbits.com/2026/08/25/state-divergence-enables-unauthorized-access/), 2026-08-25, and [anatomy of a report](https://www.trailofbits.com/anatomy-of-a-report/), summaries.
- **Use for:** a post-fix write-up with temporary and full fixes side by side, dates inline in the lead, and consulting-report findings rated separately for severity and difficulty with short-term and long-term recommendations.

### `sonar-voyager`

- **Source:** [The tainted voyage](https://www.sonarsource.com/blog/the-tainted-voyage-uncovering-voyagers-vulnerabilities/), summary. Dated 2025-01-27; its timeline says 2025-01-21; the discrepancy was not resolved.
- **Use for:** a timeline that records follow-ups and elapsed days when the maintainer does not answer, and impact stated separately for standalone and chained issues.

## Receiving-side guidance

What the people who triage reports ask for, and what makes them close a report.

### `curl-policy`

- **Source:** [VULN-DISCLOSURE-POLICY.md](https://github.com/curl/curl/blob/master/docs/VULN-DISCLOSURE-POLICY.md), raw; [secprocess page](https://curl.se/dev/secprocess.html). Read 2026-10-14.
- **Use for:** an OSS project's channel rule, severity policy, and its explicit list of non-security issues.
- **Channel and voice:** report on HackerOne, not email; explain briefly in your own voice; do not paste long AI-generated explanations. No report template.
- **Severity:** the security team rates Low, Medium, High, Critical and does not use CVSS, not even in its own CVE records. Issues likely found by basic testing rarely rate above Low.
- **Not security issues:** small leaks, never-ending transfers, impractical attacks, undocumented API misuse, attackers already local, debug and test code, crashes a malicious server can cause, legacy dependencies, weak algorithms a user asked for, CRLF in data, and unreleased code. Only releases are considered secure.
- **Disclosure:** nothing is public before the announcement; every report, valid or not, is eventually disclosed.

### `curl-ai-policy`

- **Source:** [CONTRIBUTE.md, On AI use in curl](https://github.com/curl/curl/blob/master/docs/CONTRIBUTE.md), raw.
- **Use for:** the clearest AI rule from an OSS maintainer. If an AI tool found the problem, say so in the report. Verify that the issue exists and behaves as the tool claims. Pasting an AI-generated report is seldom advisable; once the finding is verified, write the report and explain the problem as you understood it. Reporters of made-up issues are banned.

### `curl-cvss` and `curl-bounty-end`

- **Source:** [CVSS is dead to us](https://daniel.haxx.se/blog/2025/01/23/cvss-is-dead-to-us/), 2025-01-23, and [the end of the curl bug bounty](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/), 2026-01-26, summaries; [LWN coverage](https://lwn.net/Articles/1058266).
- **Use for:** why one maintainer refuses CVSS, and the bounty's end in January 2026. The January post's channel advice and the current policy file disagree; the policy file was treated as current.

### `curl-slop-2025`

- **Source:** [Death by a thousand slops](https://daniel.haxx.se/blog/2025/07/14/death-by-a-thousand-slops/), 2025-07-14, summary.
- **Use for:** scale of the problem. About a fifth of 2025 submissions to that point were AI slop and about one in twenty were real; the stated concern is quality, with or without AI.

### `larson-slop-2024`

- **Source:** [New era of slop security reports for open source](https://sethmlarson.dev/slop-security-reports), 2024-12-03, summary. Author triages for CPython, pip, urllib3, and Requests.
- **Use for:** reporter obligations: a person reviews every report before it is sent; send a few, learn from feedback, then more; submit patches with reports; no bulk submissions.
- **Slop signs:** plausible at first and slow to refute; flags correct usage as a flaw; the vulnerability is in the PoC's own misuse of the project; mass submission.
- **Dated advice:** also says not to use AI to detect vulnerabilities, which later accepted AI-found reports contradict (`curl-h1-uaf`, `doyensec-ovs`). The shared point is human verification.

### `openssf-finder` and `openssf-template`

- **Source:** [OpenSSF finder guide](https://github.com/ossf/oss-vulnerability-guide/blob/main/finder-guide.md) and [disclosure template](https://github.com/ossf/oss-vulnerability-guide/blob/main/templates/notifications/disclosure.md), raw.
- **Use for:** the finder's question list and a public-ready advisory template.
- **Questions:** what was found; versions believed vulnerable; product; steps and the software and hardware needed; vulnerable lines, root cause, and when it was introduced; impact, an estimated CVSS 3.1 score that the maintainer may revise, and a CWE; known exploitation; remediation, with patches welcome; time constraints; who else knows; willingness to demonstrate.
- **Advice:** send the PoC once a secure channel exists; write the first report so it can become the public advisory.
- **Template order:** Summary, CVE, Affected versions, Reporter, Severity with a motivation and attack scenario, where CVSS is optional but a given score carries its vector, Proof of Concept, Remediation and Mitigation, Further Analysis, Timeline.
- **When rejected:** check the report named the vulnerable lines, the concrete risk, what an attacker ultimately does, how to replicate, and how to fix.

### `cert-useful-reports`, `cert-credibility`, `cert-validation`

- **Source:** CERT/CC Guide to CVD, [providing useful information](https://certcc.github.io/CERT-Guide-to-CVD/howto/initiation/useful_reports/), [report credibility](https://github.com/CERTCC/CERT-Guide-to-CVD/blob/main/docs/howto/coordination/_report_credibility.md), [validating reports](https://certcc.github.io/CERT-Guide-to-CVD/howto/coordination/validation/), raw.
- **Use for:** the most complete list of credibility indicators, usable as checks.
- **Include:** exact product versions, how the issue was found and with which tools, PoC or reproduction, a suggested fix if known, impact and attack scenario, time constraints; CWE or CAPEC to name the type.
- **For credibility:** specific about what is affected, reproducible, attack scenario, mitigation, PoC, impact neither exaggerated nor understated. Screenshots and video support the text and do not replace it.
- **Against credibility:** vague products or versions; vague preconditions; vague or exaggerated impact; extraordinary claims without matching evidence; unclear gain over what the attacker already had; rare non-default preconditions without evidence they occur; dire impact for a trivially found bug; narrative rambling; misused terminology; mostly raw tool output; video or images instead of text; no security impact; no attack scenario.
- **Grammar:** poor grammar or spelling is explicitly not a credibility indicator, out of regard for non-native writers.
- **After reporting:** questions from the receiver are validation; answer them specifically and courteously.

### `google-reproduce`, `google-attack-scenario`, `google-native-language`, `google-automated-poc`, `google-vrp-quality`

- **Source:** Google Bug Hunters, [help us quickly reproduce the bug](https://bughunters.google.com/learn/improving-your-reports/how-to-report/help-us-quickly-reproduce-the-bug), [write down the attack scenario](https://bughunters.google.com/learn/improving-your-reports/how-to-report/write-down-the-attack-scenario), [use your native language](https://bughunters.google.com/learn/improving-your-reports/how-to-report/use-your-native-language), [create an exceptional automated PoC](https://bughunters.google.com/learn/improving-your-reports/how-to-report/create-an-exceptional-automated-poc), [VRP rules, report quality](https://bughunters.google.com/about/rules/google-friends/6625378258649088/google-and-alphabet-vulnerability-reward-program-vrp-rules#report-quality), full text in a browser.
- **Reproduce:** the minimum needed to reproduce, sometimes a single URL; replay your own steps before sending.
- **Attack scenario:** who exploits it, for what gain, and how; the attacker's starting position and what is still out of reach; assumptions about the victim; other prerequisites; each party's actions in order. Writing it can reveal that the bug gains nothing.
- **Language:** a writer not fluent in English may write in their native language.
- **Automated PoC:** runs on a Debian-based Linux; minimal, self-contained, core libraries; documented; lets the receiver supply their own credentials; no browser automation, rare languages, or extra exploits for the same bug.
- **Quality table:** rewards are multiplied by 0.8, 1, or 1.2 across seven criteria: vulnerability description, attack preconditions, impact analysis, reproduction and PoC, target information, reproduction output, and responsiveness. Theoretical or speculative impact rates Low. Reproduction should be automated when possible. Target information means product, version, and hostnames. For responsiveness, AI slop rates Low, and concise, precise replies within three workdays rate Exceptional. Only information present before triage counts.

### `chromium-faq`, `chromium-severity`, `chromium-vrp-faq`

- **Source:** Chromium [security FAQ](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md), [severity guidelines](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md), [VRP FAQ](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/vrp-faq.md), raw.
- **Use for:** a vendor's attachment and reproduction rules and its stance on AI features.
- **Version:** at least the version, OS, and release channel; a bisection to the introducing commit for full reward.
- **PoC:** attached as individual files, not archives or links; named `poc.html`; minimized; a patch as a git patch with a clear base commit; no showy success logging; demonstrated in the shipped binary, not a test binary.
- **Steps:** numbered, with full command line and flags; no custom harness.
- **Report:** concise; show reachability and user harm; theoretical bugs from static analysis without demonstration are closed as not reproducible; empty placeholder reports can suspend the account.
- **Severity:** set by the team; mitigating factors such as unusual user interaction lower it; most crashes are not vulnerabilities.
- **AI features:** unsafe or misleading model output is not a vulnerability, and influencing a feature's output through page content is not one by itself unless further user harm is shown.

### `apple-guidelines`

- **Source:** [Apple Security Bounty guidelines](https://security.apple.com/bounty/guidelines/), summary.
- **Use for:** a vendor's content and eligibility rules. State observed behavior, expected behavior, the security mechanism bypassed, and how an attacker exploits it; numbered steps; crash log or diagnostics; an exploit or reliable PoC attached, not linked; reproducible on the latest public or beta release. Avoid long AI-generated descriptions; issues found by AI without proper validation are ineligible alongside theoretical issues; repeated ineligible submissions pause the account.

### `msrc-example` and `msrc-faq`

- **Source:** [MSRC example report submission](https://www.microsoft.com/en-us/msrc/bounty-example-report-submission), summary, and [report an issue FAQ](https://www.microsoft.com/en-us/msrc/faqs-report-an-issue), summary confirmed by a second fetch.
- **Use for:** expected versus observed result, and graded report quality.
- **Example:** Title, Platform, Class, Bounty Program, Summary, Description, Proof of Concept, Expected Result, Observed Result, Acknowledgment. Platform carries OS and build; no impact or severity field; the vendor decides severity. Quality tiers rise from type, version, environment, and output, to a minimized PoC, to an exact root cause with timing and environment constraints that reproduces without a debugger.
- **FAQ:** description, steps that reproduce consistently, how an attacker would use it against another user, and a PoC; one report per vulnerability; verify scanner findings manually first.

### `h1-quality` and `bugcrowd-guide`

- **Source:** [HackerOne quality reports](https://docs.hackerone.com/en/articles/8475116-quality-reports), summary, page dated 2025-02-05; [Bugcrowd: how to write excellent reports](https://www.bugcrowd.com/resources/levelup/how-to-write-excellent-reports-techniques-that-save-triagers-time-and-mistakes-that-should-be-avoided-in-reports/), summary, undated.
- **Use for:** platform conventions. HackerOne: a clear title, numbered steps with URLs, parameters, and roles, expected versus actual, impact, supporting material; avoid detail the team does not need. Bugcrowd: title with type, asset, and parameter; a minimal PoC and no deeper digging than proof needs; impact written for the asset rather than copied; one report for one bug across several endpoints; Markdown headings, code blocks, and bold for key notes.

### `stenberg-llm-2024`

- **Source:** [The I in LLM stands for intelligence](https://daniel.haxx.se/blog/2024/01/02/the-i-in-llm-stands-for-intelligence/), 2024-01-02, summary. Read 2026-11-25.
- **Use for:** why fluent slop costs a triager more than obvious junk: the better a report looks, the longer it takes to close. In the post's buffer-overflow example, the maintainer asked where the overflow was and received more generated explanation instead of a location. Its 2024 bounty statistics are not current rates.

### `bugcrowd-slop`

- **Source:** [Bugcrowd glossary: AI slop](https://www.bugcrowd.com/glossary/ai-slop/), undated, summary. Read 2026-11-25.
- **Use for:** a triager-side list of slop signals: unverified claims, missing or fabricated PoC, hallucinated references and functions, generic text that fits any system, repackaged scanner output, false exploit chains, overstated impact, and a reporter who disappears when asked follow-up questions.

### `django-policy`

- **Source:** [Django security policy](https://docs.djangoproject.com/en/dev/internals/security/), summary. The page also contains a note addressed to AI tools; it was recorded, not followed.
- **Use for:** a short-report OSS policy. A brief description, a minimal PoC, tested Django and Python versions; a patch is optional. No CVSS, no long background, no self-assessment of whether it is a vulnerability. One issue at a time. If AI was used, say which tool did what; verify reproducibility; unverified AI output is closed without reply.

### `kernel-policy`

- **Source:** [Linux kernel security bugs](https://docs.kernel.org/process/security-bugs.html), raw text, re-read 2026-10-14. The page includes instructions addressed to AI assistants; they were recorded as policy content, not followed.
- **Use for:** the strictest plain-text channel and the most detailed AI rules.
- **Required:** an affected version range with stable identifiers, not "latest mainline" or a distribution kernel version; verified on a recent tree, at least by checking that the code has not changed since the detected version; a description with traces; a reproducer that both triggers the issue and confirms it happened, not binary-only; the conditions, such as configuration, permissions, and timing.
- **Format:** plain text, without attachments where possible; Markdown, HTML, and RST are frowned upon. Separate messages for separate parts unless the same maintainers fix them in one commit.
- **AI-assisted reports:** keep them short with the key facts first; plain text; verifiable impact only, without speculative consequences; a tested reproducer, shared only on request; a tested fix with a Fixes tag. An AI-found bug should be treated as effectively public, because others tend to find it the same day.
- **Threat model:** most reports to the security list are ordinary bugs; check whether the issue crosses a trust boundary on a correctly configured system. Reporters must be available to answer questions.

### `node-security`

- **Source:** [Node.js SECURITY.md](https://github.com/nodejs/node/blob/main/SECURITY.md), raw.
- **Use for:** test conduct and a threat model with triage dispositions.
- **Report quality:** clear steps, reproducible code, the minimum PoC, harmful payloads removed.
- **Conduct:** isolated environments; no production testing without authorization; no access to other users' data; stop at accidental access.
- **Threat model:** reports that assume a trusted element is compromised are out of scope. Dispositions are vulnerability, security-interest bug, common bug, and invalid; defense-in-depth fixes are not vulnerabilities and get no CVE; a security-interest bug touching a security control should still be reported privately first. A long list of non-vulnerabilities with CWE numbers follows.

### `rails-policy`

- **Source:** [Rails security policy](https://rubyonrails.org/security), summary.
- **Use for:** a channel-only policy: HackerOne; after 30 days without reply, email or ask in public channels for a contact without discussing the issue.

### `google-oss-guide` and `depthfirst-policy`

- **Source:** [Google OSS vulnerability guide](https://github.com/google/oss-vulnerability-guide/blob/main/guide.md) and [depthfirst disclosure approach](https://depthfirst.com/research/our-approach-to-coordinated-vulnerability-disclosure), 2025-12-05, summaries.
- **Use for:** maintainer expectations and a vendor's verification statement. The Google guide asks for reproduction steps, affected systems, versions, and packages, treats designed behavior and hardening suggestions as non-vulnerabilities, and sets a 90-day norm. depthfirst, a vendor of automated findings, states that a person verifies every report, which carries an executive summary, exploit impact, technical details, PoC, and suggested fix.

## Record formats

### `cve-cna-rules`

- **Source:** [CVE CNA Operational Rules](https://www.cve.org/ResourcesSupport/AllResources/CNARules) 4.2.0, read from the site's raw data file.
- **Record:** at least one affected product marked affected or unknown; fixed versions should be identified; a type or root cause, with CWE preferred; a prose description; a public reference other than the record.
- **Description:** must summarize the vulnerability, must not contradict the record, must not credit people or tools, which have their own credits field, must be English, must not carry irrelevant content, should not only describe the difference from another CVE; key details phrasing is optional.
- **Counting:** no security impact means no vulnerability; separate CVEs only for independently fixable issues; interdependent conditions are one vulnerability; updating a dependency is not a new one. No severity requirement.

### `cve-key-details`

- **Source:** [Key Details Phrasing](https://www.cve.org/Resources/General/Key-Details-Phrasing.pdf), 2016 slides read as images.
- **Template:** `[VULNTYPE] in [COMPONENT] in [VENDOR] [PRODUCT] [VERSION] allows [ATTACKER] to [IMPACT] via [VECTOR].` A second form puts `[ROOT CAUSE], which allows` after the version.
- **Versions:** `1.2.3`, `1.2.3 and earlier`, `before 1.2.3`, ranges with `through`; no leading `v`; no official form for "and later".
- **Attackers:** remote attackers, remote authenticated users, local users, physically proximate attackers, man-in-the-middle attackers, context-dependent attackers, and others. Unknown impact is "unspecified impact"; unknown vector is "via unspecified vectors".

### `github-pvr`

- **Source:** [privately reporting a security vulnerability](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) and its form reusable, raw from github/docs, changed 2026-10-02.
- **Form:** by default requires a summary, details, proof of concept, and impact statement; maintainers can replace the form with `.github/VULNERABILITY_REPORT.yml`, set minimum lengths, and require a CWE. An optional checkbox reads that AI assistance was used to find or write up the report. The reporter becomes a collaborator and credited user and may start a temporary private fork to work on a fix. The repository's security policy is shown above the form. The documentation does not say whether the form accepts attachments.
- **API:** `summary` up to 1024 characters and `description` up to 65535; affected packages with ecosystem, name, vulnerable range, patched versions, functions; CWE IDs; severity as a label or a CVSS vector, not both.

### `github-advisory-docs`

- **Source:** [writing security advisories](https://docs.github.com/en/code-security/tutorials/fix-reported-vulnerabilities/write-security-advisories), [creating a repository advisory](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/fix-reported-vulnerabilities/create-repository-advisory), [about the Advisory Database](https://docs.github.com/en/code-security/security-advisories/working-with-global-security-advisories-from-the-github-advisory-database/about-the-github-advisory-database), raw.
- **Ranges:** operator, one space, version; lower bound first, then a comma and a space, then the upper bound, as in `>= 3.4.0-rc.0, <= 3.4.9`; `>` is discouraged because OSV cannot express it; one range per affected-product entry; do not write `< n` and then name `n+1` as patched. Following the syntax lets the advisory be reviewed without follow-up questions.
- **Fields:** title, CVE, description, affected products, severity or a CVSS 3.1 or 4.0 calculator, CWE, credits typed Finder, Reporter, Analyst, Coordinator, Remediation developer, Remediation reviewer, Remediation verifier, Tool, Sponsor. Database severity has four levels.

### `osv-schema`

- **Source:** [OSV schema](https://ossf.github.io/osv-schema/) 1.9.2, raw.
- **Fields:** `summary` one English plain-text line, about 120 characters; `details` English CommonMark; ranges as events `introduced`, `fixed`, `last_affected`, `limit`, with `fixed` strongly preferred; `severity` entries with type and vector; `credits` with the same types as GitHub plus OTHER.

### `cwe-mapping`

- **Source:** [CWE root cause mapping guidance](https://cwe.mitre.org/documents/cwe_usage/guidance.html) 1.1, 2024-03-22, two summaries.
- **Rules:** map to Base or Variant entries; a Class only when nothing lower fits; never a Category. CWE-20, CWE-74, and CWE-284 are discouraged. Phrases like "bypass authorization" describe impact or a prerequisite, not the weakness; map the missing or incorrect behavior. Read the entry's mapping notes and have a colleague check.

### `cvss31-guide`

- **Source:** [CVSS v3.1 User Guide](https://www.first.org/cvss/v3.1/user-guide) and specification, two summaries.
- **Rules:** CVSS measures severity and should not be used alone as risk. Base scores usually come from the product maintainer. Score the reasonable final impact you are confident an attacker can reach. For libraries, assume the reasonable worst-case use and document the assumption. Chaining is outside the formal metrics: list each vulnerability's own score, and a chained score separately. Scope changes only across an authorization boundary. Ratings: None 0.0, Low 0.1 to 3.9, Medium 4.0 to 6.9, High 7.0 to 8.9, Critical 9.0 to 10.0.

### `cvss40-spec`

- **Source:** [CVSS v4.0 specification](https://www.first.org/cvss/v4.0/specification-document) and [user guide](https://www.first.org/cvss/v4.0/user-guide), two summaries.
- **Rules:** Base and Supplemental come from the organization maintaining the vulnerable system; Threat and Environmental belong to the consumer. Label displayed numbers CVSS-B, CVSS-BT, CVSS-BE, or CVSS-BTE. New base metrics include Attack Requirements and passive or active user interaction; scope is replaced by vulnerable-system and subsequent-system impact. No guidance specific to LLMs or prompt injection.

## Accepted advisories in Python and agent tooling

Read through the repository advisory API. The public API hides whether an advisory came through private reporting, so authorship of each body is inferred from its style.

### `ghsa-fedify`, `ghsa-faraday`, `ghsa-nginx-ui`, `ghsa-asynchttpclient`

- **Source:** [GHSA-xw9q-2mv6-9fr8](https://github.com/advisories/GHSA-xw9q-2mv6-9fr8) with its predecessor [GHSA-p9cg-vqcc-grcx](https://github.com/advisories/GHSA-p9cg-vqcc-grcx), [GHSA-5rv5-xj5j-3484](https://github.com/advisories/GHSA-5rv5-xj5j-3484), [GHSA-h246-wpgf-vmq5](https://github.com/advisories/GHSA-h246-wpgf-vmq5), [GHSA-2jwh-9rmr-j4xf](https://github.com/advisories/GHSA-2jwh-9rmr-j4xf), summaries with key sentences confirmed.
- **Use for:** incomplete-fix reports.
- **Framing:** the prior advisory ID comes first; one sentence on what the prior fix covered; the single missing axis, such as an address range, an input type, a sibling code path, or a parallel router; evidence such as a protected and unprotected request pair or a regression test that only covers one type. One body has a section on why it is not a duplicate and leaves new advisory versus update to the maintainer. One title marks itself a possible incomplete fix.
- **Limits:** source-verified at a named commit without a running instance; the PoC did not touch real internal services; a side candidate marked low confidence.
- **Severity:** CVSS in the published fields; who entered it is not visible. One advisory's vector says no confidentiality impact while its body describes a credential being sent.
- **Disclosure:** one Attribution section says AI-assisted tools supported discovery and analysis.

### `ghsa-mcp-python-sdk`

- **Source:** [GHSA-w4fh-qvv9-3v23](https://github.com/modelcontextprotocol/python-sdk/security/advisories/GHSA-w4fh-qvv9-3v23), 2026-10-05, API.
- **Use for:** a maintainer-written user advisory: Summary, Am I affected?, Fix. Two separate affected ranges for two release lines; a warning that upgrading alone is not enough, with a workaround. No reproduction in the published body.

### `ghsa-fastmcp`

- **Source:** [GHSA-m8x7-r2rg-vh5g](https://github.com/advisories/GHSA-m8x7-r2rg-vh5g), 2026-03-31, API.
- **Use for:** a short body: two paragraphs, a PoC with the observed effect, impact limited to one operating system and wrapper type with the others excluded. The repository range string broke GitHub's spacing rule and was normalized by curation.

### `ghsa-langchain-core`

- **Source:** [GHSA-qh6h-p6c9-ff54](https://github.com/advisories/GHSA-qh6h-p6c9-ff54), 2026-03-26, API.
- **Use for:** a table of vulnerable code paths, impact bounded by file-extension limits and by the need for an app that accepts untrusted configuration, and a severity label with its reason in the body. The body's credit section with a contact address is the opposite of the CVE description rule.

### `ghsa-vllm`

- **Source:** [GHSA-25q3-v2hm-8vpf](https://github.com/vllm-project/vllm/security/advisories/GHSA-25q3-v2hm-8vpf), 2026-09-03, API.
- **Use for:** verification evidence. Summary, Details, Proof of concept, Impact, Verification, Patches, Workarounds, Not affected, References. A table compares unpatched and patched official images with a control request run first; it states that confidentiality and integrity are unaffected, lists unaffected endpoints with reasons, and argues the defect is not in a dependency. Published without a CWE.

### `ghsa-gradio`

- **Source:** [GHSA-jmh7-g254-2cq9](https://github.com/advisories/GHSA-jmh7-g254-2cq9), 2026-02-27, API.
- **Use for:** numbered steps with file and line references and an external PoC gist; a broad, unbounded impact list; a free-text range field normalized by curation.

### `ghsa-mlflow`

- **Source:** [GHSA-26p8-2jq9-3vq9](https://github.com/mlflow/mlflow/security/advisories/GHSA-26p8-2jq9-3vq9), 2026-10-09, API.
- **Use for:** the most complete reporter-style body in the set. Summary, Technical details, Proof of concept, Reproduction environment, Affected range and source lineage, Impact, Artifacts and attachments. The tested version is pinned by release commit, image tag, and digest; the introducing commit is named and an earlier release lacks the feature. The PoC only writes a marker file, runs with the network disabled, and a remote run on an owned host has its address redacted. Impact depends on container settings, and a read-only filesystem blocks the chain. A sentence saying no fixed release exists was left in after the record gained a patched version.

## Community evidence

### `reddit-survey`

- **Source:** a survey of 13 Reddit threads with full comment trees read through an archive, 2026-10-14, by the pack maintainer. Thread permalinks are in r/bugbounty, r/cybersecurity, r/github, r/ethicalhacking. Scores are mostly below 10; claims that a report was AI-written are commenters' guesses; one triage account appears in four threads.
- **Use for:** weak, corroborating signals only. A PoC that creates the condition it then observes; claims about code that a single real request would refute; no evidence when asked for a recording; severity inflation; bold pseudo-headings and emoji, with one valid report accepted despite them; mismatched CWE or OWASP references; repeating the same AI answer when questioned; for fix bypasses in bounty programs, a new report is the common expectation, and some programs take it only after the original is closed as fixed. Where a rule rests on this source alone, the rule says so.

## Source disagreements

| Question | Positions | Sources |
| --- | --- | --- |
| Severity in a private report | No score; team decides | `curl-policy`, `django-policy`, `msrc-example`, `p0-report-2026`, `ghsl-advisories` |
| | Reporter estimates CVSS with vector, maintainer may revise | `openssf-finder`, `openssf-template`, `github-pvr` |
| | Reporter sets a platform field, triage adjusts | `h1-gitlab-file-read`, `curl-h1-uaf` |
| Who owns which CVSS metrics | Base from maintainer; Temporal or Threat from analysts in 3.1, from consumers in 4.0 | `cvss31-guide`, `cvss40-spec` |
| First block | Finding first | most report sources |
| | Two or three sentences of background first | `p0-report-2026` |
| Depth of the initial report | Enough to triage, without long background or many sections | `django-policy`, `kernel-policy`, `curl-policy`, `google-reproduce` |
| | Full root cause and analysis | `msrc-example`, `p0-report-2026`, `ghsa-mlflow` |
| Person | Impersonal | `ghsl-advisories`, `p0-report-2026`, `zdi-advisory`, `talos-report` |
| | We | `oss-qualys-regresshion`, `oss-suse-screen`, `h1-node-smuggling` |
| | I | `curl-h1-uaf`; I only for opinions in `h1-curl-socks5` |
| Formatting | Plain text only | `kernel-policy`, oss-security posts |
| | Markdown with bold for key notes | `bugcrowd-guide` |
| | Bold pseudo-headings read as machine-written | `reddit-survey`, weak |
| Attachments | Individual files, no archives, no links | `chromium-vrp-faq`, `apple-guidelines` |
| | Archive with environment and patch | `curl-h1-uaf`, `h1-node-smuggling` |
| | Plain text without attachments where possible | `kernel-policy` |
| Fix suggestion | Welcome or expected | `openssf-finder`, `kernel-policy`, `larson-slop-2024`, `cert-useful-reports` |
| | Optional | `django-policy`, `h1-quality` |
| | Receivers may ignore it | `reddit-survey`, weak |
| AI use | Disclose and verify | `curl-ai-policy`, `django-policy`, `github-pvr`, `kernel-policy` |
| | Do not use AI to find bugs | `larson-slop-2024`, 2024 |
| | AI-found bugs treated as effectively public | `kernel-policy` |
| AI-drafted report text | The reporter writes it after verifying | `curl-ai-policy`, `apple-guidelines` |
| | AI may draft, with disclosure and human verification | `django-policy`, `kernel-policy` |
| Affected range in the report | Tested version only; the receiver sets the range | `h1-gitlab-file-read`, `curl-h1-uaf`, `ghsl-advisories` |
| | Reporter proposes a range labeled an estimate | `github-pvr`, `openssf-finder`, `ghsa-fedify` |
| Range syntax | `before 1.2.3`; `< 1.2.3`; `introduced` and `fixed` events | `cve-key-details`; `github-advisory-docs`; `osv-schema` |
| Credit in a description | Forbidden in CVE descriptions | `cve-cna-rules` |
| | Credit section in a GHSA body | `ghsa-langchain-core` |
| Weakness type | Required in a CVE record, CWE preferred | `cve-cna-rules` |
| | GitHub advisory published without a CWE | `ghsa-vllm` |

The venue's own written policy settles each of these for a given report.

## Local decisions

These rules are the pack maintainer's requirements or the pack's review practice rather than a published source. They are kept because they protect the report or the reporter, and each is labeled `local` where it is used. Where a published source points the same way, the basis names it; that source supports the direction, not the rule as written.

| Rule | Basis |
| --- | --- |
| The agent drafts, checks, and packages; the person verifies, owns the text, and submits | Pack authority rule; human verification in `curl-ai-policy`, `django-policy` |
| No answers to a maintainer in the person's name unless asked | Pack authority rule |
| Search advisories, issues, pull requests, and the prior fix for duplicates | Pack review practice |
| Reproduction by the person or a user-approved fresh agent; `review-panel` only on request, after the provider warning | Pack authority rule; reproduce from the text in `google-reproduce` |
| Re-run every check and re-hash attachments after each revision | Pack review practice; a rewrite can drop a precondition or add an unverified claim |
| A full CVSS vector, one sentence per disputable metric, and the label reporter's estimate | Pack rule; vector requested in `openssf-template`, `github-pvr` |
| Score a variant for its own path | Pack rule; `cvss31-guide` scores each vulnerability alone but says nothing on variants |
| Each measured result in the field that owns it; each scope note once, beside the claim it limits | Pack rule from a cross-field count of two AI-assisted reports against maintainer-written advisories; impact without repeated figures in `ghsa-vllm` |
| Follow-up comments short and casual, answering the question first | Pack owner's preference; customer-service replies as a slop signal in `stenberg-llm-2024`, `bugcrowd-slop` |
| Name the commit, tag, and first release when a version string does not identify the code | Pack rule; stable identifiers in `kernel-policy` |
| Bound a range by comparing source across tags | Pack rule; the unchanged-code check in `kernel-policy` |
| An email subject that does not reveal the bug | Pack rule |
| Units and provenance on every number, and numbers that match their attachments | Pack review practice |
| Say each limit once, in the sentence it limits | Pack style choice; one weak source advises stating key facts and preconditions twice, `reddit-survey` |
| Scope words only with the checked scope | Pack rule; vague claims in `cert-credibility` |
| No em dashes, decorative bold runs, or emoji, and the generated-filler word list | Pack writing profile; plain text in `kernel-policy`; weak signals in `reddit-survey` |
| No placeholders left in a draft | Pack rule; empty reports in `chromium-vrp-faq` |
| Negative and positive controls, each in its own attachment | Pack review practice; baseline and fixed-build controls in `h1-node-smuggling`, `ghsa-vllm` |
| Setup through the normal path, with any administrative shortcut justified | Pack rule; setup kept apart from attack in `larson-slop-2024`, `reddit-survey` |
| A generic error, timeout, or exception counts as inconclusive | Pack rule |
| Describe impact rather than attack real users to analyze it | Pack conduct rule; test conduct in `node-security` |
| Record how each environment value was captured | Pack review practice |
| Quote source code exactly, with line numbers and marked elisions | Pack review practice; pinned permalinks in `h1-curl-socks5`, file and line citations in `p0-report-2026` |
| Stable attachment names, each cited from the observation it supports | Pack review practice; artifact lists in `ghsa-mlflow` |
| Record the SHA-256 of each attachment or bundle and send the bytes that were reviewed | Pack review practice; no surveyed source states it |
| Keep a separate finding out of the main bundle | Pack rule; one issue at a time in `django-policy` |
| Scan evidence for home directories, user names, hostnames, internal addresses, and tokens before sending | Pack maintainer's requirement; redaction in `ghsa-mlflow`, conduct rules in `node-security` |
| Never imply a recording that does not exist; keep the environment to make one | Pack rule; recordings support text in `cert-credibility` |

## Limits of this catalog

- Most sources are published after a fix. Private originals are `p0-report-*`, the HackerOne reports, `bmo-webgl`, and GHSA bodies that read as reporter-written. Timeline and Credit sections in public advisories were written by publishers.
- Summaries were used for several guidance pages and for the CWE and CVSS guides; their entries say so. HackerOne comment threads were only partly read.
- Whether a GHSA body came through private reporting is not visible in the public API.
- Rules from `reddit-survey` alone are weak and marked where used.
- Sources were not checked again after 2026-10-14; policies change, so re-read a target's own policy before every report.
