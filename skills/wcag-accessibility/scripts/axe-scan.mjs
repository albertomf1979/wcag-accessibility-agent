#!/usr/bin/env node
// Run axe-core (via @axe-core/cli + headless Chrome) against a URL and print a
// compact JSON summary of the results on stdout.
//
// Usage: node axe-scan.mjs <url> [tags]
//   tags defaults to the WCAG 2.1 A + AA rule set: wcag2a,wcag2aa,wcag21a,wcag21aa
//
// Requires Node.js 18+ and Chrome. The first run downloads @axe-core/cli through npx.
// If Chrome and the bundled ChromeDriver versions differ, set CHROMEDRIVER_PATH
// to a matching driver (e.g. `npx @puppeteer/browsers install chromedriver@<chrome-major>`).
// Exit code: 0 when the scan ran (even with violations), 1 when it could not run.
// The output is evidence from an automated tool only: an empty violation list
// does NOT mean the page conforms to WCAG.

import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";

const DEFAULT_TAGS = "wcag2a,wcag2aa,wcag21a,wcag21aa";

function fail(error, extra = {}) {
  console.log(JSON.stringify({ success: false, error, ...extra }, null, 2));
  process.exit(1);
}

// Prefer the npx that ships next to the running node binary (nvm, Homebrew...).
function findNpx() {
  const name = process.platform === "win32" ? "npx.cmd" : "npx";
  const sibling = join(dirname(process.execPath), name);
  return existsSync(sibling) ? sibling : name;
}

function summarize(data, url, tags) {
  const violations = data.violations ?? [];
  const incomplete = data.incomplete ?? [];
  const byImpact = {};
  for (const v of violations) {
    const impact = v.impact ?? "unknown";
    byImpact[impact] = (byImpact[impact] ?? 0) + 1;
  }
  return {
    success: true,
    url,
    tags_checked: tags,
    engine: data.testEngine?.name ?? "axe-core",
    engine_version: data.testEngine?.version ?? "",
    violations_total: violations.length,
    violations_by_impact: byImpact,
    passes_count: (data.passes ?? []).length,
    incomplete_count: incomplete.length,
    violations: violations.map((v) => ({
      id: v.id,
      impact: v.impact,
      description: v.description,
      help: v.help,
      helpUrl: v.helpUrl,
      wcag_tags: (v.tags ?? []).filter((t) => t.startsWith("wcag")),
      nodes_count: (v.nodes ?? []).length,
      nodes_sample: (v.nodes ?? []).slice(0, 3).map((n) => ({
        html: (n.html ?? "").slice(0, 250),
        target: n.target ?? [],
        failureSummary: (n.failureSummary ?? "").slice(0, 400),
      })),
    })),
    incomplete_sample: incomplete.slice(0, 10).map((i) => ({
      id: i.id,
      description: i.description,
      impact: i.impact,
    })),
    note:
      "Automated axe-core results from the rendered DOM (JS+CSS executed). " +
      "Automated tools only detect part of WCAG failures: 'incomplete' items " +
      "need manual review, and zero violations does not imply conformance.",
  };
}

function main() {
  const [url, tags = DEFAULT_TAGS] = process.argv.slice(2);
  if (!url) fail("Usage: node axe-scan.mjs <url> [tags]");

  const args = [
    "-y", "@axe-core/cli", url,
    "--tags", tags,
    "--stdout",
    "--timeout", "90",
    "--chrome-options=--no-sandbox,--disable-dev-shm-usage",
  ];
  if (process.env.CHROMEDRIVER_PATH) args.push("--chromedriver-path", process.env.CHROMEDRIVER_PATH);

  const result = spawnSync(
    findNpx(),
    args,
    {
      encoding: "utf8",
      timeout: 120_000,
      maxBuffer: 64 * 1024 * 1024,
      shell: process.platform === "win32",
      env: { ...process.env, FORCE_COLOR: "0", NO_COLOR: "1" },
    },
  );

  if (result.error?.code === "ETIMEDOUT") fail("axe-cli timed out after 120 seconds.");
  if (result.error) fail(`Could not run npx: ${result.error.message}`);

  // axe-cli may print a non-JSON preamble; parse from the first [ or {.
  const stdout = (result.stdout ?? "").trim();
  const start = stdout.search(/[[{]/);
  if (start === -1) {
    fail("axe-cli produced no JSON output.", {
      stderr: (result.stderr ?? "").slice(0, 500),
      stdout: stdout.slice(0, 300),
    });
  }

  let raw;
  try {
    raw = JSON.parse(stdout.slice(start));
  } catch (e) {
    fail(`Failed to parse axe-cli JSON: ${e.message}`, { raw_stdout: stdout.slice(0, 500) });
  }
  const data = Array.isArray(raw) ? raw[0] : raw;
  console.log(JSON.stringify(summarize(data, url, tags), null, 2));
}

main();
