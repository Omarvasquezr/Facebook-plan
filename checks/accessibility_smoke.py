"""Audit semantics and practical access in a served portfolio.

Usage:
  python3 checks/accessibility_smoke.py http://127.0.0.1:4193/ \
    --axe /path/to/axe.min.js --report /tmp/accessibility-results.json

Axe is a development-only, optional input. It is not shipped or loaded by the site.
Automated results do not establish complete WCAG conformance or a device audit.
"""
import argparse
import asyncio
import json
from pathlib import Path
import shutil

from playwright.async_api import async_playwright


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", nargs="?", default="http://127.0.0.1:4193/")
    parser.add_argument("--axe", type=Path)
    parser.add_argument("--report", type=Path)
    return parser.parse_args()


async def axe_audit(page, source, label):
    await page.add_script_tag(content=source)
    result = await page.evaluate("""async () => axe.run(document, {
      runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}
    })""")
    violations = [{"id":item["id"], "impact":item["impact"],
                   "targets":[node["target"] for node in item["nodes"]]}
                  for item in result["violations"]]
    incomplete = [{"id":item["id"], "impact":item["impact"],
                   "targets":[node["target"] for node in item["nodes"]]}
                  for item in result["incomplete"]]
    assert not violations, (label, violations)
    return {"state":label, "violations":violations, "incomplete":incomplete}


async def check_reduced_language_reflow(browser, base):
    """Static language information must fit when its animation is disabled."""
    results = []
    for width, height in ((320,568),(375,812),(390,844),(812,375)):
        for language in ("it", "es", "en"):
            context = await browser.new_context(
                viewport={"width":width,"height":height}, reduced_motion="reduce"
            )
            await context.add_init_script(
                "sessionStorage.setItem('ov-intro','1');localStorage.setItem('ov-theme','light');"
                f"localStorage.setItem('ov-language','{language}')"
            )
            page = await context.new_page()
            await page.goto(base, wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            original = page.locator(".marquee-langs > .seq-langs:not([data-marquee-copy])")
            assert await original.count() == 1
            assert await original.locator(":scope > .lang").count() == 3
            await original.scroll_into_view_if_needed()
            measurements = await original.evaluate("""sequence => {
              const track=sequence.closest('.strip-track').getBoundingClientRect();
              return [...sequence.querySelectorAll(':scope > .lang')].map(language => ({
                text:language.textContent.trim(),
                visible:language.getClientRects().length>0,
                track:{left:track.left,right:track.right,top:track.top,bottom:track.bottom},
                fragments:[...language.querySelectorAll('b,i')].flatMap(part => {
                  const range=document.createRange(); range.selectNodeContents(part);
                  return [...range.getClientRects()].map(rect => ({
                    left:rect.left,right:rect.right,top:rect.top,bottom:rect.bottom
                  }));
                })
              }));
            }""")
            for item in measurements:
                assert item["visible"] and item["text"] and item["fragments"], (width,language,item)
                track = item["track"]
                for fragment in item["fragments"]:
                    assert fragment["left"] >= max(0,track["left"])-1, (width,language,"language text clipped left",item)
                    assert fragment["right"] <= min(width,track["right"])+1, (width,language,"language text clipped right",item)
                    assert fragment["top"] >= track["top"]-1, (width,language,"language text clipped above",item)
                    assert fragment["bottom"] <= track["bottom"]+1, (width,language,"language text clipped below",item)
            assert await page.locator(".marquee-langs").evaluate("element=>getComputedStyle(element).animationName") == "none"
            results.append({"width":width,"height":height,"language":language,"texts":[item["text"] for item in measurements],"passed":True})
            await context.close()
    return results


async def main():
    args = arguments()
    base = args.url.rstrip("/") + "/"
    axe_source = args.axe.read_text() if args.axe else None
    results = {"axe":[], "access":[], "assets":[], "reducedLanguageReflow":[]}
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            executable_path=shutil.which("chromium") or shutil.which("google-chrome"),
            args=["--no-sandbox"],
        )
        for language in ("it", "es", "en"):
            for theme in ("light", "dark"):
                context = await browser.new_context(viewport={"width":1440,"height":900}, reduced_motion="reduce")
                await context.add_init_script(
                    "sessionStorage.setItem('ov-intro','1');"
                    f"localStorage.setItem('ov-language','{language}');localStorage.setItem('ov-theme','{theme}')"
                )
                page = await context.new_page()
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                await page.goto(base, wait_until="networkidle")
                await page.evaluate("document.fonts.ready")
                assert await page.locator("html").get_attribute("lang") == language
                assert await page.get_by_role("main").count() == 1
                assert await page.get_by_role("heading", level=1).count() == 1
                if axe_source:
                    results["axe"].append(await axe_audit(page, axe_source, f"{language}-{theme}-main"))
                if language == "es":
                    await page.locator('[data-area="business"]').click()
                    await page.locator("#area-business details > summary").focus()
                    await page.keyboard.press("Enter")
                    assert await page.locator("#area-business details").get_attribute("open") is not None
                    if axe_source:
                        results["axe"].append(await axe_audit(page, axe_source, f"{language}-{theme}-tools"))
                    await page.locator("#profile-open").click()
                    await page.locator(".profile-portrait").evaluate("image=>image.decode()")
                    if axe_source:
                        results["axe"].append(await axe_audit(page, axe_source, f"{language}-{theme}-dialog"))
                    await page.keyboard.press("Escape")
                assert not errors, errors
                await context.close()

        for width, height in ((320,568),(375,812),(390,844),(412,915),(812,375),(640,450)):
            context = await browser.new_context(viewport={"width":width,"height":height}, reduced_motion="reduce", has_touch=True)
            await context.add_init_script("sessionStorage.setItem('ov-intro','1');localStorage.setItem('ov-theme','light');localStorage.setItem('ov-language','es')")
            page = await context.new_page()
            await page.goto(base, wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            assert await page.evaluate("document.documentElement.scrollWidth<=innerWidth"), (width,height,"horizontal overflow")
            assert (await page.locator(".mail").get_attribute("href")).startswith("mailto:")
            assert (await page.locator(".phone").get_attribute("href")).startswith("tel:")
            # Focus must be visible and reachable without any hover gesture.
            for _ in range(18):
                await page.keyboard.press("Tab")
                obscured = await page.evaluate("""() => {
                  const element=document.activeElement;
                  if (!element || element===document.body) return null;
                  const rect=element.getBoundingClientRect();
                  const x=Math.min(innerWidth-1,Math.max(1,rect.x+rect.width/2));
                  const y=Math.min(innerHeight-1,Math.max(1,rect.y+rect.height/2));
                  const hit=document.elementFromPoint(x,y);
                  return hit===element || element.contains(hit) ? null : {tag:element.tagName,id:element.id};
                }""")
                assert obscured is None, (width,height,"focused control obscured",obscured)
            await page.locator("#profile-open").click()
            dialog = page.locator("#profile-dialog")
            assert await dialog.evaluate("element=>element.contains(document.activeElement)")
            await page.locator("#about-omar").evaluate("element=>element.scrollTop=element.scrollHeight")
            close = dialog.locator("[data-profile-close]")
            assert await close.evaluate("""element=>{
              const rect=element.getBoundingClientRect();
              return document.elementFromPoint(rect.x+rect.width/2,rect.y+rect.height/2)?.closest('[data-profile-close]')===element;
            }"""), (width,height,"dialog close obscured")
            await close.click()
            assert not await dialog.is_visible()
            results["access"].append({"width":width,"height":height,"passed":True})
            if not results["assets"]:
                for name in ("Omar-Vasquez-CV.pdf","Omar-Vasquez-CV-telefono.pdf"):
                    response = await page.request.get(base+name)
                    assert response.status == 200 and (await response.body()).startswith(b"%PDF-"), name
                    results["assets"].append({"name":name,"status":response.status})
            await context.close()

        # Informative scrolling content has a keyboard-operable pause control.
        context = await browser.new_context(viewport={"width":390,"height":844}, reduced_motion="no-preference")
        await context.add_init_script("sessionStorage.setItem('ov-intro','1');localStorage.setItem('ov-theme','light')")
        page = await context.new_page()
        await page.goto(base, wait_until="networkidle")
        pause = page.locator("[data-marquee-pause]")
        assert await pause.count() == 1 and await pause.is_enabled()
        await pause.scroll_into_view_if_needed()
        await page.mouse.move(1,1)
        await pause.focus()
        await page.keyboard.press("Enter")
        assert await pause.get_attribute("aria-pressed") == "true"
        await page.locator(".compact-theme").focus()
        assert await page.locator(".marquee-langs").evaluate("element=>getComputedStyle(element).animationPlayState") == "paused"
        await pause.focus()
        await page.keyboard.press("Space")
        assert await pause.get_attribute("aria-pressed") == "false"
        await page.locator(".compact-theme").focus()
        await page.wait_for_function("getComputedStyle(document.querySelector('.marquee-langs')).animationPlayState === 'running'")
        await context.close()

        results["reducedLanguageReflow"] = await check_reduced_language_reflow(browser, base)

        context = await browser.new_context(java_script_enabled=False, viewport={"width":320,"height":568})
        page = await context.new_page()
        await page.goto(base, wait_until="networkidle")
        assert await page.locator("#about-omar").is_visible()
        assert await page.locator("[data-area-panel]").count() == 4
        for panel in await page.locator("[data-area-panel]").all():
            assert await panel.is_visible()
            summary = panel.locator("details > summary")
            await summary.click()
            assert await panel.locator("details").get_attribute("open") is not None
        assert await page.evaluate("document.documentElement.scrollWidth<=innerWidth")
        await context.close()
        await browser.close()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(results,indent=2))
    print(f"{len(results['axe'])} axe states and {len(results['access'])} keyboard/viewport states passed; PDFs, contact links, dialogue and no-JS content passed.")
    print("Contrast over gradients/transparency may remain incomplete; no full WCAG or real-device certification is implied.")


if __name__ == "__main__":
    asyncio.run(main())
