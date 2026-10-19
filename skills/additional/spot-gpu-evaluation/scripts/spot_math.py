#!/usr/bin/env python3
"""Planning arithmetic for evaluation runs on preemptible (spot) GPU capacity.

Three subcommands, each reading numbers from the command line and printing
results; nothing here calls a cloud API.

episode  Chance that an episode is interrupted at least once, and the active
         time needed to finish it when every interruption restarts it with a
         fresh full budget.
restart  Share of allocations that reach a healthy model server, and the
         productive share of billed and wall time, for a given cold-start time.
tokens   Blended per-token price of a hosted API for a token mix, optionally
         compared with self-hosting on a node billed by the hour.

The episode and restart models treat preemptions as random arrivals while the
node runs: allocation lifetime is exponential with mean `--lifetime-h`. That is
the simplest model consistent with providers publishing no age-based policy.
When preemptions cluster soon after start, the model overstates the risk to
episodes that start after the risky window and understates failed restarts.

Requires Python 3.10 or newer and only the standard library, so it runs as
`python3 -I spot_math.py ...`. Exit status is 0 on success and 2 on a usage
error or an invalid value.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass

# Records are dataclasses because this bundled script must run with the
# standard library alone; there is no project environment to install into.

DEFAULT_SHARES: tuple[float, float, float] = (0.10, 0.85, 0.05)
SHARE_TOLERANCE: float = 1e-6


@dataclass(frozen=True)
class EpisodeRisk:
    """Interruption risk and fresh-budget completion cost for one episode length."""

    duration_min: float
    weight: float
    p_interrupted: float
    expected_preemptions_to_finish: float
    expected_active_h_fresh_budget: float
    fresh_budget_factor: float


@dataclass(frozen=True)
class EpisodeReport:
    """Per-duration risks and their weighted mean interruption probability."""

    lifetime_h: float
    episodes: list[EpisodeRisk]
    weighted_p_interrupted: float


@dataclass(frozen=True)
class RestartReport:
    """Cold-start cost against a mean allocation lifetime."""

    startup_min: float
    lifetime_h: float
    wait_min: float
    p_reach_healthy: float
    productive_share_of_billed: float
    productive_share_of_wall: float
    startup_overhead_without_preemption: float | None


@dataclass(frozen=True)
class TokenReport:
    """Blended hosted-API price and, when a node is given, the self-hosted price."""

    shares: dict[str, float]
    api_per_million: float
    self_host_per_million: float | None
    api_to_self_host_ratio: float | None


def episode_risk(duration_min: float, weight: float, lifetime_h: float) -> EpisodeRisk:
    """Return the interruption risk of one episode length under random preemption.

    An episode needing D hours survives with probability exp(-D/tau). Restarting
    it from scratch with a full budget after every interruption needs, in
    expectation, tau * (exp(D/tau) - 1) hours of active time and exp(D/tau) - 1
    preemptions before one uninterrupted run completes.
    """
    duration_h: float = duration_min / 60.0
    ratio: float = duration_h / lifetime_h
    growth: float = math.expm1(ratio)
    active_h: float = lifetime_h * growth
    return EpisodeRisk(
        duration_min=duration_min,
        weight=weight,
        p_interrupted=-math.expm1(-ratio),
        expected_preemptions_to_finish=growth,
        expected_active_h_fresh_budget=active_h,
        fresh_budget_factor=active_h / duration_h,
    )


def episode_report(durations_min: list[float], weights: list[float], lifetime_h: float) -> EpisodeReport:
    """Combine per-duration risks with weights normalized to sum to one."""
    total: float = sum(weights)
    risks: list[EpisodeRisk] = [episode_risk(d, w / total, lifetime_h) for d, w in zip(durations_min, weights)]
    weighted: float = sum(r.weight * r.p_interrupted for r in risks)
    return EpisodeReport(lifetime_h=lifetime_h, episodes=risks, weighted_p_interrupted=weighted)


def restart_report(startup_min: float, lifetime_h: float, wait_min: float, productive_min: float | None) -> RestartReport:
    """Return the productive shares of an allocation with a cold start of `startup_min`.

    Billing runs for the whole allocation, expected length tau. Productive time is
    the part after startup, expected tau * exp(-S/tau). Wall time adds the
    unbilled wait from preemption to the next running allocation.
    """
    startup_h: float = startup_min / 60.0
    survive: float = math.exp(-startup_h / lifetime_h)
    productive_h: float = lifetime_h * survive
    wall_h: float = lifetime_h + wait_min / 60.0
    overhead: float | None = None if productive_min is None else startup_min / productive_min
    return RestartReport(
        startup_min=startup_min,
        lifetime_h=lifetime_h,
        wait_min=wait_min,
        p_reach_healthy=survive,
        productive_share_of_billed=survive,
        productive_share_of_wall=productive_h / wall_h,
        startup_overhead_without_preemption=overhead,
    )


def token_report(
    prices: tuple[float, float, float],
    shares: tuple[float, float, float],
    *,
    node_price_per_hour: float | None,
    output_tokens_per_second: float | None,
    utilization: float,
) -> TokenReport:
    """Return per-million-token prices for a mix of uncached input, cached input, and output.

    Prices are per million tokens. Self-hosted throughput is given as output
    tokens per second and scaled to all tokens with the output share, so the
    node processes output_tps / share_output tokens per second at this mix.
    """
    api: float = sum(p * s for p, s in zip(prices, shares))
    self_host: float | None = None
    ratio: float | None = None
    if node_price_per_hour is not None and output_tokens_per_second is not None:
        tokens_per_hour: float = output_tokens_per_second / shares[2] * 3600.0 * utilization
        self_host = node_price_per_hour / tokens_per_hour * 1e6
        ratio = api / self_host
    return TokenReport(
        shares={"input": shares[0], "cached_input": shares[1], "output": shares[2]},
        api_per_million=api,
        self_host_per_million=self_host,
        api_to_self_host_ratio=ratio,
    )


def positive(text: str) -> float:
    """Parse a strictly positive number for argparse."""
    value: float = float(text)
    if not math.isfinite(value) or value <= 0:
        raise argparse.ArgumentTypeError(f"must be a positive number, got {text}")
    return value


def non_negative(text: str) -> float:
    """Parse a number that may be zero for argparse."""
    value: float = float(text)
    if not math.isfinite(value) or value < 0:
        raise argparse.ArgumentTypeError(f"must be zero or positive, got {text}")
    return value


def build_parser() -> argparse.ArgumentParser:
    """Define the three subcommands and their options."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--json", action="store_true", help="print one JSON object instead of text")
    sub = parser.add_subparsers(dest="command", required=True)

    ep: argparse.ArgumentParser = sub.add_parser("episode", help="interruption risk per episode length")
    ep.add_argument("--duration-min", type=positive, nargs="+", required=True, help="episode lengths in minutes")
    ep.add_argument("--weights", type=positive, nargs="+", help="relative share of each length; default equal")
    ep.add_argument("--lifetime-h", type=positive, required=True, help="mean allocation lifetime in hours")

    rs: argparse.ArgumentParser = sub.add_parser("restart", help="productive share given a cold-start time")
    rs.add_argument("--startup-min", type=non_negative, required=True, help="start of allocation to serving healthy")
    rs.add_argument("--lifetime-h", type=positive, required=True, help="mean allocation lifetime in hours")
    rs.add_argument("--wait-min", type=non_negative, default=0.0, help="mean unbilled minutes from preemption to running")
    rs.add_argument("--productive-min", type=positive, help="productive minutes per allocation, for S/P without preemption")

    tk: argparse.ArgumentParser = sub.add_parser("tokens", help="hosted API versus self-hosted price per million tokens")
    tk.add_argument("--price-input", type=non_negative, required=True, help="uncached input price per million")
    tk.add_argument("--price-cached", type=non_negative, required=True, help="cached input price per million")
    tk.add_argument("--price-output", type=non_negative, required=True, help="output price per million")
    tk.add_argument(
        "--shares",
        type=non_negative,
        nargs=3,
        default=list(DEFAULT_SHARES),
        metavar=("INPUT", "CACHED", "OUTPUT"),
        help="token shares summing to 1; default 0.10 0.85 0.05, a cache-heavy agent loop",
    )
    tk.add_argument("--node-price-per-hour", type=positive, help="self-hosted node price per hour")
    tk.add_argument("--output-tokens-per-second", type=positive, help="measured aggregate output tokens per second")
    tk.add_argument("--utilization", type=positive, default=1.0, help="productive share of billed node time")
    return parser


def run(args: argparse.Namespace, parser: argparse.ArgumentParser) -> EpisodeReport | RestartReport | TokenReport:
    """Validate cross-argument rules and compute the requested report."""
    if args.command == "episode":
        weights: list[float] = args.weights or [1.0] * len(args.duration_min)
        if len(weights) != len(args.duration_min):
            parser.error("--weights needs one value per --duration-min")
        return episode_report(args.duration_min, weights, args.lifetime_h)
    if args.command == "restart":
        return restart_report(args.startup_min, args.lifetime_h, args.wait_min, args.productive_min)
    shares: tuple[float, float, float] = (args.shares[0], args.shares[1], args.shares[2])
    if abs(sum(shares) - 1.0) > SHARE_TOLERANCE or shares[2] <= 0:
        parser.error("--shares must sum to 1 and the output share must be positive")
    if (args.node_price_per_hour is None) != (args.output_tokens_per_second is None):
        parser.error("--node-price-per-hour and --output-tokens-per-second go together")
    if args.utilization > 1.0:
        parser.error("--utilization is a share of billed time and cannot exceed 1")
    prices: tuple[float, float, float] = (args.price_input, args.price_cached, args.price_output)
    return token_report(
        prices,
        shares,
        node_price_per_hour=args.node_price_per_hour,
        output_tokens_per_second=args.output_tokens_per_second,
        utilization=args.utilization,
    )


def render_text(report: EpisodeReport | RestartReport | TokenReport) -> str:
    """Format a report as aligned key-value lines."""
    lines: list[str] = []
    if isinstance(report, EpisodeReport):
        lines.append(f"mean allocation lifetime: {report.lifetime_h:g} h")
        for r in report.episodes:
            lines.append(
                f"episode {r.duration_min:g} min (weight {r.weight:.2f}): "
                f"P(interrupted) {r.p_interrupted:.1%}, "
                f"fresh-budget reruns need {r.expected_active_h_fresh_budget:.2f} h active "
                f"({r.fresh_budget_factor:.2f}x), {r.expected_preemptions_to_finish:.2f} preemptions expected"
            )
        lines.append(f"weighted P(interrupted): {report.weighted_p_interrupted:.1%}")
    elif isinstance(report, RestartReport):
        lines.append(f"startup {report.startup_min:g} min, lifetime {report.lifetime_h:g} h, wait {report.wait_min:g} min")
        lines.append(f"P(allocation reaches healthy): {report.p_reach_healthy:.1%}")
        lines.append(f"productive share of billed time: {report.productive_share_of_billed:.1%}")
        lines.append(f"productive share of wall time: {report.productive_share_of_wall:.1%}")
        if report.startup_overhead_without_preemption is not None:
            lines.append(f"startup overhead S/P without preemption: {report.startup_overhead_without_preemption:.1%}")
    else:
        mix: str = ", ".join(f"{k} {v:.2f}" for k, v in report.shares.items())
        lines.append(f"token mix: {mix}")
        lines.append(f"hosted API blended price per million tokens: {report.api_per_million:.4f}")
        if report.self_host_per_million is not None and report.api_to_self_host_ratio is not None:
            lines.append(f"self-hosted price per million tokens: {report.self_host_per_million:.4f}")
            lines.append(f"API / self-hosted: {report.api_to_self_host_ratio:.2f}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Parse arguments, compute, and print; argparse exits with 2 on usage errors."""
    parser: argparse.ArgumentParser = build_parser()
    args: argparse.Namespace = parser.parse_args(argv)
    report: EpisodeReport | RestartReport | TokenReport = run(args, parser)
    print(json.dumps(asdict(report), indent=2) if args.json else render_text(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
