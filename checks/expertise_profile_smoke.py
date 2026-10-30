"""Exercise expertise disclosures and the personal sheet in a local browser.

Usage: python3 checks/expertise_profile_smoke.py http://127.0.0.1:4186/
The check never publishes or writes browser data to an external service.
"""
import asyncio
import json
import re
import shutil
import sys
from pathlib import Path

from playwright.async_api import async_playwright

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4186/").rstrip("/") + "/"
AREAS = ("production", "operations", "business", "technology")
ROOT = Path(__file__).resolve().parents[1]
UI = json.loads(re.search(r"const ui = (\{.*?\});\n\s*const root", (ROOT / "preferences.js").read_text(), re.S).group(1))


async def check_translations(page, language):
    index = ("it", "es", "en").index(language)
    for key, value in await page.locator("[data-ui]").evaluate_all(
        "els => els.map(el => [el.dataset.ui, el.textContent])"
    ):
        assert value == UI[key][index], (language, key, value, UI[key][index])
    for key, value in await page.locator("[data-label]").evaluate_all(
        "els => els.map(el => [el.dataset.label, el.getAttribute('aria-label')])"
    ):
        assert value == UI[key][index], (language, key, value, UI[key][index])
    for key, value in await page.locator("[data-alt]").evaluate_all(
        "els => els.map(el => [el.dataset.alt, el.getAttribute('alt')])"
    ):
        assert value == UI[key][index], (language, key, value, UI[key][index])


async def visible_panels(page):
    return await page.locator("[data-area-panel]").evaluate_all(
        "els => els.filter(el => !el.hidden).map(el => el.id)"
    )


async def check_areas(page, label):
    buttons = page.locator("[data-area]")
    assert await buttons.count() == len(AREAS), (label, "duplicated area controls")
    assert await buttons.evaluate_all("els => els.map(el => el.dataset.area)") == list(AREAS), (label, "area order changed")
    geometry = await buttons.evaluate_all("""elements => elements.map(button => {
      const rect=button.getBoundingClientRect();
      const icon=button.querySelector('.area-plus').getBoundingClientRect();
      const range=document.createRange(); range.selectNodeContents(button.querySelector('.area-label'));
      return {left:rect.left,right:rect.right,top:rect.top,height:rect.height,iconLeft:icon.left,
              text:[...range.getClientRects()].map(item=>({left:item.left,right:item.right}))};
    })""")
    if page.viewport_size['width'] <= 700:
        assert abs(geometry[0]['top']-geometry[1]['top']) < 1 and abs(geometry[2]['top']-geometry[3]['top']) < 1, (label, 'expected two rows of two buttons')
        assert geometry[2]['top'] > geometry[0]['top'], (label, 'areas need two visible rows')
        for item in geometry:
            assert 0 <= item['left'] < item['right'] <= page.viewport_size['width'], (label, 'area outside viewport', item)
            assert item['height'] >= 44, (label, 'small touch target', item)
            for fragment in item['text']:
                assert fragment['left'] >= item['left']+4 and fragment['right'] <= item['iconLeft']-2, (label, 'area text overlaps its chevron', item)
    assert not await visible_panels(page), (label, "initial panels should be collapsed")
    shared = page.locator(".expertise-shared")
    assert await shared.count() == 1, (label, "shared leadership paragraph duplicated")
    assert await shared.is_hidden(), (label, "shared paragraph should stay hidden with all areas closed")
    for area in AREAS:
        button = page.locator(f'[data-area="{area}"]')
        target = await button.get_attribute("aria-controls")
        assert target, (label, area, "missing aria-controls")
        panel = page.locator(f"#{target}")
        await button.click()
        assert await button.get_attribute("aria-expanded") == "true", (label, area)
        assert await visible_panels(page) == [target], (label, area, "more than one panel open")
        assert await panel.is_visible(), (label, area, "panel not visible")
        assert await shared.is_visible(), (label, area, "shared leadership paragraph missing")
        assert len((await panel.inner_text()).strip()) > 70, (label, area, "empty capability content")
        assert await panel.locator(".area-points > li").count() == 4, (label, area, "expected four concise capabilities")
        tools = panel.locator("details.area-tools-disclosure")
        assert await tools.count() == 1, (label, area, "tools need one native disclosure")
        assert await tools.get_attribute("open") is None, (label, area, "tools should start collapsed")
        first_tool = tools.locator(".area-chip").first
        assert await first_tool.is_hidden(), (label, area, "tools leaked out of collapsed disclosure")
        summary = tools.locator("summary")
        await summary.focus()
        await page.keyboard.press("Enter")
        assert await tools.get_attribute("open") is not None, (label, area, "Enter did not expand tools")
        assert await first_tool.is_visible(), (label, area, "expanded tools remain hidden")
        await page.keyboard.press("Space")
        assert await tools.get_attribute("open") is None, (label, area, "Space did not close tools")
        assert await buttons.evaluate_all(
            "els => els.filter(el => el.getAttribute('aria-expanded') === 'true').length"
        ) == 1, (label, area, "ambiguous selected control")
        # The next selection replaces the current panel rather than stacking cards.
    last = page.locator(f'[data-area="{AREAS[-1]}"]')
    await last.click()
    assert not await visible_panels(page), (label, "second click must close the selected area")
    assert await last.get_attribute("aria-expanded") == "false"
    assert await shared.is_hidden(), (label, "shared paragraph remains after closing all areas")


async def check_dialog(page, trigger, label, keyboard=False):
    dialog = page.locator("#profile-dialog")
    await trigger.scroll_into_view_if_needed()
    await trigger.focus()
    if keyboard:
        await page.keyboard.press("Enter")
    else:
        await trigger.click()
    assert await dialog.is_visible(), (label, "personal sheet did not open")
    assert await dialog.evaluate("el => el.matches(':modal')"), (label, "sheet is not modal")
    assert await dialog.evaluate("el => el.scrollTop === 0"), (label, "reopened sheet starts midway through its content")
    card = dialog.locator("#about-omar")
    assert await card.evaluate("el => el.scrollTop === 0"), (label, "reopened personal card starts midway through its content")
    portrait = dialog.locator(".profile-portrait")
    assert await portrait.count() == 1, (label, "portrait missing or duplicated")
    await portrait.evaluate("img => img.decode()")
    assert await portrait.evaluate("img => img.complete && img.naturalWidth > 0 && img.naturalHeight > 0"), (label, "portrait did not load")
    image_shape = await portrait.evaluate("""img => {
        const box = img.getBoundingClientRect();
        return {width:box.width,height:box.height,naturalWidth:img.naturalWidth,naturalHeight:img.naturalHeight,
                declaredWidth:+img.getAttribute('width'),declaredHeight:+img.getAttribute('height'),fit:getComputedStyle(img).objectFit};
    }""")
    assert abs(image_shape["width"] / image_shape["height"] - image_shape["naturalWidth"] / image_shape["naturalHeight"]) < .002, (label, "portrait cropped or distorted", image_shape)
    assert image_shape["declaredWidth"] == image_shape["naturalWidth"] and image_shape["declaredHeight"] == image_shape["naturalHeight"], (label, "incorrect portrait dimensions", image_shape)
    assert image_shape["fit"] == "contain", (label, "portrait should preserve its full frame", image_shape)
    assert (await portrait.get_attribute("alt") or "").strip(), (label, "portrait needs a localized alternative")
    assert await dialog.evaluate("el => el.contains(document.activeElement)"), (label, "focus outside sheet")
    # Native modality prevents an obscured page control from stealing focus.
    await page.locator("#language-toggle").evaluate("el => el.focus()")
    assert await dialog.evaluate("el => el.contains(document.activeElement)"), (label, "background remains interactive")
    for _ in range(4):
        await page.keyboard.press("Tab")
        # Chromium can visit the browser boundary (activeElement === body)
        # between the last and first dialog controls. No page control may gain focus.
        assert await dialog.evaluate("el => el.contains(document.activeElement) || document.activeElement === document.body"), (label, "Tab reached a background control")
    bounds = await dialog.bounding_box()
    width = page.viewport_size["width"]
    height = page.viewport_size["height"]
    assert bounds and bounds["x"] >= 0 and bounds["x"] + bounds["width"] <= width + 1, (label, "sheet clipped", bounds)
    assert bounds["y"] >= 0 and bounds["y"] + bounds["height"] <= height + 1, (label, "sheet exceeds viewport", bounds)
    # Portrait + text may scroll inside a short viewport. Both close methods
    # remain usable after reaching the end, and the next opening resets to top.
    await card.evaluate("el => {el.scrollTop = el.scrollHeight}")
    assert await dialog.locator("[data-profile-close]").evaluate(
        "el => {const r=el.getBoundingClientRect(); return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)?.closest('[data-profile-close]')===el}"
    ), (label, "close button is obscured after scrolling the portrait/card")
    await dialog.evaluate('el => {window.__profileCheckClosed = new Promise(done => el.addEventListener("close", () => done(true), {once:true}))}')
    if keyboard:
        await page.keyboard.press("Escape")
    else:
        await dialog.locator("[data-profile-close]").click()
    await page.evaluate("window.__profileCheckClosed")
    assert not await dialog.is_visible(), (label, "sheet did not close")
    assert await trigger.evaluate("el => el === document.activeElement"), (label, "focus was not restored")


async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=shutil.which("chromium") or shutil.which("google-chrome"),
            args=["--no-sandbox"],
        )
        for width in (320, 390, 768, 1440):
            ctx = await browser.new_context(
                viewport={"width": width, "height": 900}, reduced_motion="reduce", color_scheme="light"
            )
            await ctx.add_init_script("sessionStorage.setItem('ov-intro','1')")
            page = await ctx.new_page()
            await page.clock.install(time="2026-10-29T11:00:00Z")
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            await page.goto(BASE, wait_until="networkidle")
            await page.evaluate("document.fonts.ready")
            assert await page.locator(".profile-entry").count() == 0, "duplicate Conóceme link remains"
            assert await page.locator(".name a,.profile-name").count() == 0, "large title must remain static"
            assert (await page.locator(".name").text_content()).strip() == "OMAR"
            assert await page.locator("[data-profile-open]").count() == 2, "expected one name entry and one footer entry"
            assert await page.locator("#profile-open").get_attribute("data-sky-trigger") is not None
            assert await page.locator("#profile-open").get_attribute("aria-pressed") is None
            for language in ("it", "es", "en"):
                await page.locator("#language-toggle").click()
                await page.locator(f'[data-language="{language}"]').click()
                await check_translations(page, language)
                for theme in ("light", "dark"):
                    if await page.locator("html").get_attribute("data-theme") != theme:
                        await page.locator(".compact-theme").click()
                    label = (width, language, theme)
                    assert await page.locator("html").get_attribute("lang") == language, label
                    await check_areas(page, label)
                    await check_dialog(page, page.locator("#profile-open"), label, keyboard=True)
                    footer_trigger = page.locator(".profile-footer [data-profile-open]")
                    await check_dialog(page, footer_trigger, label)
                    assert await page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (label, "horizontal document overflow")
                    assert not errors, (label, errors)
                    results.append({"width": width, "language": language, "theme": theme, "passed": True})
            # Enter and Space activate the same area buttons as touch/click.
            button = page.locator(f'[data-area="{AREAS[0]}"]')
            await button.focus()
            await page.keyboard.press("Enter")
            assert await button.get_attribute("aria-expanded") == "true"
            await page.keyboard.press("Space")
            assert await button.get_attribute("aria-expanded") == "false"
            await ctx.close()

        # Language synchronization also reaches the already-open dialog, whose
        # section was moved out of main during progressive enhancement.
        ctx = await browser.new_context(reduced_motion="reduce")
        await ctx.add_init_script("sessionStorage.setItem('ov-intro','1')")
        first = await ctx.new_page()
        second = await ctx.new_page()
        await first.clock.install(time="2026-10-29T11:00:00Z")
        await second.clock.install(time="2026-10-29T11:00:00Z")
        await first.goto(BASE, wait_until="networkidle")
        await second.goto(BASE, wait_until="networkidle")
        await first.locator("#profile-open").click()
        await second.locator("#language-toggle").click()
        await second.locator('[data-language="es"]').click()
        await first.wait_for_function("document.documentElement.lang === 'es'")
        await check_translations(first, "es")
        assert await first.locator("#profile-dialog").is_visible()
        await first.keyboard.press("Escape")
        assert await first.locator("#profile-open").evaluate("el => el === document.activeElement")
        await ctx.close()

        ctx = await browser.new_context(
            viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, reduced_motion="reduce"
        )
        await ctx.add_init_script("sessionStorage.setItem('ov-intro','1')")
        page = await ctx.new_page()
        await page.clock.install(time="2026-10-29T11:00:00Z")
        await page.goto(BASE, wait_until="networkidle")
        button = page.locator('[data-area="technology"]')
        await button.tap()
        assert await button.get_attribute("aria-expanded") == "true"
        await page.locator("#profile-open").tap()
        assert await page.locator("#profile-dialog").is_visible()
        await page.locator("#profile-dialog [data-profile-close]").tap()
        assert not await page.locator("#profile-dialog").is_visible()
        await ctx.close()

        # All expertise content survives if scripts are unavailable.
        ctx = await browser.new_context(java_script_enabled=False, viewport={"width": 320, "height": 900})
        page = await ctx.new_page()
        await page.goto(BASE, wait_until="networkidle")
        assert await page.locator("[data-area-panel]").count() == len(AREAS)
        for panel in await page.locator("[data-area-panel]").all():
            assert await panel.is_visible(), "expertise content hidden without JavaScript"
            tools = panel.locator("details.area-tools-disclosure")
            assert await tools.get_attribute("open") is None
            await tools.locator("summary").focus()
            await page.keyboard.press("Enter")
            assert await tools.get_attribute("open") is not None, "tools cannot be opened without JavaScript"
            assert await tools.locator(".area-chip").first.is_visible()
        assert await page.locator("#about-omar").is_visible(), "personal sheet hidden without JavaScript"
        assert await page.locator("#profile-dialog").count() == 0
        assert await page.locator("#profile-open").get_attribute("href") == "#about-omar"
        assert await page.locator("#about-omar [data-profile-close]").is_hidden()
        assert await page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "no-JS overflow"
        await ctx.close()
        await browser.close()
    print(json.dumps(results, indent=2))
    print(f"{len(results)} width/language/theme states passed; ordered four-area selection, native tools disclosure, uncropped portrait, translated UI/ARIA/alt, keyboard, modal scroll/close and focus restoration, touch, no-JS and zero observed JS errors passed.")


if __name__ == "__main__":
    asyncio.run(main())
