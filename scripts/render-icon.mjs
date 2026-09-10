import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { Resvg } = require("@resvg/resvg-js");

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const assets = join(root, "assets");
const svg = readFileSync(join(assets, "icon.svg"));
mkdirSync(assets, { recursive: true });

for (const size of [16, 24, 32, 48, 64, 128, 256]) {
  const resvg = new Resvg(svg, {
    fitTo: { mode: "width", value: size },
    background: "rgba(0,0,0,0)",
  });
  const out = join(assets, `icon-${size}.png`);
  writeFileSync(out, resvg.render().asPng());
  console.log("wrote", out);
}
