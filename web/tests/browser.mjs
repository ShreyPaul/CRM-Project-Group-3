import { chromium } from "playwright";
import assert from "node:assert/strict";
import { mkdir, readFile } from "node:fs/promises";
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
const errors = [];
page.on("pageerror", (e) => errors.push(e.message));
const cost = async (r) => page.locator(`.regime-${r} .total`).innerText();
try {
  await page.goto(process.env.APP_URL || "http://localhost:5173");
  await page
    .getByRole("heading", { name: "When is more monitoring worth the cost?" })
    .waitFor();
  assert.equal(await cost("A"), "$99.61M");
  assert.equal(await cost("B"), "$86.97M");
  assert.equal(await cost("C"), "$69.31M");
  await page.getByRole("button", { name: /01 \/ BEHAVIOR/ }).click();
  assert.equal(await cost("B"), "$61.14M");
  await page.getByRole("button", { name: /02 \/ PROTECTION/ }).click();
  assert.equal(await cost("B"), "$58.91M");
  await page.getByRole("button", { name: /03 \/ EMPLOYEES/ }).click();
  assert.equal(await cost("B"), "$83.42M");
  await page.getByRole("button", { name: "↺ Reset", exact: true }).click();
  assert.equal(await cost("B"), "$86.97M");
  await page
    .getByRole("button", { name: "No additional departures", exact: true })
    .click();
  assert.equal(await cost("B"), "$72.57M");
  await page.getByRole("button", { name: "↺ Reset", exact: true }).click();
  await page.getByRole("button", { name: "USB theft", exact: true }).click();
  assert.equal(await cost("B"), "$86.97M");
  assert.ok(
    await page
      .getByText(
        "USB attempts are equal across regimes in this baseline. Use Advanced inputs for custom rates.",
      )
      .isVisible(),
  );
  await page
    .getByRole("button", { name: "Email / cloud", exact: true })
    .click();
  const slider = page.getByRole("slider", {
    name: "Successful attacks remaining",
    exact: true,
  });
  await slider.focus();
  await page.keyboard.press("ArrowLeft");
  assert.notEqual(await cost("B"), "$86.97M");
  await page.getByRole("button", { name: "↺ Reset", exact: true }).click();
  assert.equal(await page.getByText("Try shared USB protection").count(), 0);
  await page.locator(".advanced > summary").click();
  const field = page
    .locator(".advanced .triple")
    .first()
    .getByRole("spinbutton")
    .first();
  await field.fill("");
  assert.equal(
    await page.getByRole("button", { name: "Apply all inputs" }).isDisabled(),
    true,
  );
  assert.equal(await cost("A"), "$99.61M");
  await field.fill("10");
  await page.getByRole("button", { name: "Apply all inputs" }).click();
  assert.equal(await cost("B"), "$86.97M");
  await page.getByRole("button", { name: "↺ Reset", exact: true }).click();
  await page.locator(".advanced > summary").click();
  await page
    .getByText("Replacement costing assumptions", { exact: true })
    .click();
  await page.getByLabel("Hiring & ramp-up ($)", { exact: true }).fill("16000");
  await page.getByRole("button", { name: "Apply all inputs" }).click();
  assert.equal(await cost("B"), "$87.67M");
  assert.equal(await cost("C"), "$69.84M");
  assert.equal(
    await page
      .getByRole("spinbutton", {
        name: "Additional employees who leave numeric value",
      })
      .inputValue(),
    "877.825",
  );
  assert.equal(
    await page.getByText("Manual cost override", { exact: true }).count(),
    0,
  );
  await page.getByRole("button", { name: "↺ Reset", exact: true }).click();
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export ↗" }).click();
  const download = await downloadPromise;
  const data = JSON.parse(await readFile(await download.path(), "utf8"));
  assert.equal(data.schemaVersion, 2);
  assert.ok(data.baselineHash);
  assert.ok(Math.abs(data.results.B.total - 86967487.4074) < 1);
  await mkdir("test-results", { recursive: true });
  await page.screenshot({ path: "test-results/desktop.png", fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  assert.ok(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  );
  await page.getByRole("button", { name: /02 \/ PROTECTION/ }).click();
  assert.equal(await cost("B"), "$58.91M");
  await page.getByRole("button", { name: "↺ Reset", exact: true }).click();
  await page.screenshot({ path: "test-results/mobile.png", fullPage: true });
  // Labels and patterns preserve interpretation without color.
  await page.emulateMedia({ forcedColors: "active", reducedMotion: "reduce" });
  assert.equal(await page.locator(".cost-card").count(), 3);
  assert.equal(
    await page.locator(".winner-label").innerText(),
    "Lowest modeled cost",
  );
  await page.emulateMedia({ forcedColors: "none" });
  await page.setViewportSize({ width: 390, height: 844 });
  for (const v of ["A", "B", "C"]) {
    const card = await page.locator(`.regime-${v}`).boundingBox();
    const amount = await page.locator(`.regime-${v} .total`).boundingBox();
    assert.ok(
      amount.x >= card.x && amount.x + amount.width <= card.x + card.width,
    );
  }
  assert.deepEqual(errors, []);
  console.log(
    "PASS: desktop/mobile, baseline, presets, reset, keyboard slider, advanced validation/apply, export, no horizontal overflow, no browser errors.",
  );
} finally {
  await browser.close();
}
