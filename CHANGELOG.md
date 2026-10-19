# Changelog

All notable changes to FlakeLedger are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- Rule tables are being reorganised for the next patch.
- The cost report is being reviewed for the next minor.

### Fixed

- A `<testsuites>` wrapper no longer lends a nested suite's `commit` and
  `attempt` markers to a suite that carries none of its own. Such a suite now
  falls back to the documented defaults and records the missing metadata
  warning, instead of being attributed to another run's commit.

## [5.0.0] - 2026-09-16

### Added

- `report --summary` prints only the per-state counts, for CI logs.

## [4.1.0] - 2026-09-15

### Added

- A per-suite view grouping the ledger by suite name.

## [3.1.0] - 2026-08-29

### Changed

- Quarantine suggestions are ranked by cost, matching the report order.

## [2.0.0] - 2026-08-05

### Added

- The report carries a `runs` block with the window and run count.
- Fixtures for the shared-timestamp tie.

## [1.0.1] - 2026-07-21

### Fixed

- Runs sharing a timestamp are ordered by file name so the classification is
  stable across machines.
- A fixture for the tie, and the smoke run now covers it.

## [1.0.0] - 2026-02-10

### Added

- Stable CLI contract: `classify`, `cost` and `report` with exit codes 0, 1
  and 2.
- `docs/FORMAT.md` as the written contract for the JUnit input and the report.
- Deterministic JSON report with a fixed key order.

## [0.9.0] - 2025-03-25

### Added

- Quarantine suggestions with the evidence runs that support them.
- `--min-runs` so a single failing run never earns the flaky label.

## [0.7.0] - 2024-06-18

### Added

- The cost model: retry minutes and runner minutes attributed per test.
- Ranked report ordered by flake tax, not by raw failure count.

## [0.6.0] - 2023-11-07

### Added

- JSON report: `report --format json` with stable key order.
- Line numbers on every parse error instead of aborting the run.

## [0.5.0] - 2022-09-27

### Added

- Classification rules: flaky, broken and undetermined, with the undetermined
  case refusing to guess.
- A worked run over the bundled samples.

## [0.4.0] - 2021-10-12

### Added

- Run grouping by test id across attempts and suites.
- Attempt numbers surfaced in the report so a rerun is visible.

## [0.3.0] - 2020-11-24

### Added

- JUnit XML parser with strict validation for ids, times and outcomes.
- `classify` subcommand and the first report shape.

## [0.2.0] - 2019-09-17

### Added

- Multi-run model: the same test across many files is one ledger row.
- Outcome comparison between attempts of the same run.

## [0.1.0] - 2018-05-08

### Added

- First release: single-run parser and a line oriented report with a findings
  total.
