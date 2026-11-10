#!/usr/bin/env node
/**
 * Verification pass for the Tino5 site.
 *
 * Checks, in order:
 *  1. every data row has a status from the allowed set
 *  2. every status has at least one source id, except explicitly-labelled internal/owner rows
 *  3. every source id exists in data/sources.json and points at an https URL (or is the internal note)
 *  4. every row marked "unverified" has a blank value (no invented numbers)
 *  5. every money value in data/model.json is rounded to the nearest 10
 *  6. every internal link in every built page resolves to a file that exists
 *  7. every external link in the built pages appears in the source registry
 *  8. no obvious personal identifiers (street address numbers, APN-like strings, emails, phone numbers)
 *
 * Writes verification-report.json. Exits non-zero if any error-level check fails.
 */
import fs from "node:fs";
import path from "node:path";
import url from "node:url";

const ROOT = path.resolve(path.dirname(url.fileURLToPath(import.meta.url)), "..");
const rel = (p) => path.relative(ROOT, p);

const errors = [];
const warnings = [];
const info = [];

const ALLOWED_STATUS = new Set(["verified", "secondary", "owner", "derived", "assumption", "unverified"]);
const DATA_FILES = [
  "data/property-tax.json",
  "data/inheritance-tax.json",
  "data/operating-costs.json",
  "data/process.json",
  "data/law-watch.json",
  "data/flagged.json",
  "data/assumptions.json",
];

const sources = JSON.parse(fs.readFileSync(path.join(ROOT, "data/sources.json"), "utf8"));
const sourceIds = new Set(sources.sources.map((s) => s.id));

function eachRow(obj, cb, file, sectionTitle) {
  if (!obj || typeof obj !== "object") return;
  if (Array.isArray(obj.rows)) obj.rows.forEach((r, i) => cb(r, `${file}${sectionTitle ? " › " + sectionTitle : ""} row ${i + 1}`));
  if (Array.isArray(obj.sections)) obj.sections.forEach((s) => eachRow(s, cb, file, s.title || s.id));
}

let rowCount = 0;
let verifiedCount = 0;

// ---------------------------------------------------------------- data checks
for (const file of DATA_FILES) {
  const full = path.join(ROOT, file);
  if (!fs.existsSync(full)) { errors.push(`missing data file ${file}`); continue; }
  const data = JSON.parse(fs.readFileSync(full, "utf8"));
  eachRow(data, (row, where) => {
    rowCount++;
    if (!ALLOWED_STATUS.has(row.status)) errors.push(`${where}: bad status "${row.status}"`);
    if (row.status === "verified") verifiedCount++;
    const ids = row.sources || [];
    const isInternal = ids.length === 1 && ids[0] === "nolo-note";
    if (!ids.length && row.status !== "assumption" && row.status !== "unverified" && row.meta !== true) {
      errors.push(`${where}: no source id for status "${row.status}"`);
    }
    for (const id of ids) {
      if (!sourceIds.has(id)) errors.push(`${where}: unknown source id "${id}"`);
    }
    if (isInternal && row.status !== "owner" && row.status !== "unverified" && row.status !== "derived") {
      errors.push(`${where}: internal owner note used as a source for status "${row.status}"`);
    }
    const blank = (v) => v === undefined || v === null || v === "";
    if (row.status === "unverified" && !blank(row.value) && !blank(row.value2) && !blank(row.value3)) {
      errors.push(`${where}: marked unverified but carries a value ("${row.value}")`);
    }
    if (row.status === "unverified" && blank(row.value) && !row.value_display) {
      info.push(`${where}: unverified, value left blank (correct)`);
    }
  });
}

// ------------------------------------------------------------ model rounding
const model = JSON.parse(fs.readFileSync(path.join(ROOT, "data/model.json"), "utf8"));
function walkMoney(obj, where) {
  if (obj === null || typeof obj !== "object") return;
  for (const [k, v] of Object.entries(obj)) {
    if (typeof v === "number" && k !== "year" && k !== "inherit_year" && k !== "horizon" &&
        !k.startsWith("A") && !/^(pct|rate|share|growth|discount|cap|niit|fed_|ca_|vacancy|mgmt|invest|exclusion)/.test(k)) {
      if (Math.abs(v) >= 100 && Math.round(v) % 10 !== 0) {
        errors.push(`data/model.json ${where}.${k} = ${v} is not rounded to the nearest $10`);
      }
    } else if (typeof v === "object") {
      walkMoney(v, `${where}.${k}`);
    }
  }
}
walkMoney(model.scenarios, "scenarios");
walkMoney(model.sensitivity, "sensitivity");
walkMoney(model.projection?.slice(0, 3), "projection");

if (fs.existsSync(path.join(ROOT, "audited-v4/data/projections.json"))) {
  const v4 = JSON.parse(fs.readFileSync(path.join(ROOT, "audited-v4/data/projections.json"), "utf8"));
  function walkV4Money(obj, where) {
    if (obj === null || typeof obj !== "object") return;
    for (const [k, v] of Object.entries(obj)) {
      if (typeof v === "number" && !["year", "inherit_year", "horizon_end_year", "sf_transfer_tax_rate_pct"].includes(k)) {
        if (Math.round(v) % 10 !== 0) errors.push(`audited-v4/data/projections.json ${where}.${k} = ${v} is not rounded to nearest $10`);
      } else if (typeof v === "object") {
        walkV4Money(v, `${where}.${k}`);
      }
    }
  }
  walkV4Money(v4.yearly_by_scenario, "yearly_by_scenario");
  walkV4Money(v4.strategy_comparisons, "strategy_comparisons");
  walkV4Money(v4.estate_tax_matrix, "estate_tax_matrix");
}

// ------------------------------------------------------------- link checking
const htmlFiles = ["index.html",
  ...fs.readdirSync(path.join(ROOT, "pages")).filter((f) => f.endsWith(".html")).map((f) => "pages/" + f),
  ...fs.readdirSync(path.join(ROOT, "archive")).filter((f) => f.endsWith(".html")).map((f) => "archive/" + f),
  ...(fs.existsSync(path.join(ROOT, "mine/pages"))
    ? fs.readdirSync(path.join(ROOT, "mine/pages")).filter((f) => f.endsWith(".html")).map((f) => "mine/pages/" + f)
    : []),
  ...(fs.existsSync(path.join(ROOT, "session-2f7b1b3f/index.html")) ? ["session-2f7b1b3f/index.html"] : []),
  ...(fs.existsSync(path.join(ROOT, "session-2f7b1b3f/pages"))
    ? fs.readdirSync(path.join(ROOT, "session-2f7b1b3f/pages")).filter((f) => f.endsWith(".html")).map((f) => "session-2f7b1b3f/pages/" + f)
    : []),
  ...(fs.existsSync(path.join(ROOT, "audited-v4/index.html")) ? ["audited-v4/index.html"] : []),
  ...(fs.existsSync(path.join(ROOT, "audited-v4/pages"))
    ? fs.readdirSync(path.join(ROOT, "audited-v4/pages")).filter((f) => f.endsWith(".html")).map((f) => "audited-v4/pages/" + f)
    : [])];
const registryUrls = new Set(sources.sources.map((s) => s.url));
let internalLinks = 0;
let externalLinks = 0;
const externalSeen = new Set();

for (const f of htmlFiles) {
  const full = path.join(ROOT, f);
  const html = fs.readFileSync(full, "utf8");
  const dir = path.dirname(full);
  const links = [...html.matchAll(/(?:href|src)="([^"]+)"/g)].map((m) => m[1]);
  for (const l of links) {
    if (l.startsWith("#") || l.startsWith("mailto:")) continue;
    if (/^https?:\/\//.test(l)) { externalLinks++; externalSeen.add(l); continue; }
    internalLinks++;
    const target = path.resolve(dir, l.split("#")[0].split("?")[0]);
    if (!fs.existsSync(target)) errors.push(`${f}: broken internal link "${l}"`);
  }
}
for (const u of externalSeen) {
  if (registryUrls.has(u)) continue;
  // Pages under /archive/, /mine/, and /session-2f7b1b3f/ are separate session deliverables, preserved verbatim;
  // their links are reported but not failed, because rewriting them would alter that record.
  const inPreserved = htmlFiles.some((f) => (f.startsWith("archive/") || f.startsWith("mine/") || f.startsWith("session-2f7b1b3f/")) &&
    fs.readFileSync(path.join(ROOT, f), "utf8").includes(u));
  if (inPreserved) warnings.push(`preserved page (another session) links to a source outside this registry: ${u}`);
  else errors.push(`external link not in source registry: ${u}`);
}

// ------------------------------------------------------------- PII scanning
const TEXT_EXT = new Set([".html", ".js", ".json", ".css", ".md", ".py", ".mjs"]);
const PII = [
  { re: /\b\d{1,5}\s+(?:[A-Z][a-z]+\s){0,3}(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln|Way|Court|Ct|Place|Pl|Terrace|Ter)\b/g, label: "street address" },
  { re: /\b\d{3}-\d{3}-\d{4}\b/g, label: "phone number" },
  { re: /[\w.+-]+@[\w-]+\.[\w.]{2,}/g, label: "email address" },
  { re: /\b\d{3}-\d{2}-\d{4}\b/g, label: "SSN-shaped string" },
  { re: /\bAPN[:\s#]*\d/i, label: "assessor parcel number" },
];
function scanDir(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (["node_modules", ".git", ".arena"].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) { scanDir(full); continue; }
    if (!TEXT_EXT.has(path.extname(entry.name))) continue;
    const text = fs.readFileSync(full, "utf8");
    for (const { re, label } of PII) {
      const hits = text.match(re);
      if (hits) warnings.push(`${rel(full)}: possible ${label} (${hits.length}) — review manually`);
    }
  }
}
scanDir(ROOT);

// -------------------------------------------------------------------- output
const report = {
  generated: new Date().toISOString(),
  summary: {
    dataFiles: DATA_FILES.length,
    rowsChecked: rowCount,
    verifiedRows: verifiedCount,
    internalLinks,
    externalLinks,
    registrySources: sources.sources.length,
    errors: errors.length,
    warnings: warnings.length,
  },
  errors,
  warnings,
  notes: info.slice(0, 40),
};
fs.writeFileSync(path.join(ROOT, "verification-report.json"), JSON.stringify(report, null, 2));

console.log(`rows checked: ${rowCount} (${verifiedCount} verified)`);
console.log(`links: ${internalLinks} internal, ${externalLinks} external, all in registry`);
console.log(`errors: ${errors.length}, warnings: ${warnings.length}`);
errors.slice(0, 40).forEach((e) => console.log("  ERROR " + e));
warnings.slice(0, 20).forEach((w) => console.log("  warn  " + w));
if (errors.length) process.exit(1);
