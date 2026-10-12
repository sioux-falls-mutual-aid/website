from pathlib import Path
from datetime import datetime, timezone, timedelta
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parent
html=(root/'prototype.html').read_text()
html=html.replace('<link rel="stylesheet" href="calendar.css">','<style>'+ (root/'calendar.css').read_text()+'</style>')
html=html.replace('<script src="calendar.js" defer></script>','').replace('</body>','<script>'+(root/'calendar.js').read_text()+'</script></body>')
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    for width in [320,375,768]:
        page=browser.new_page(viewport={'width':width,'height':800})
        page.clock.install(time=datetime(2026,10,12,12,tzinfo=timezone(timedelta(hours=-5))))
        page.set_content(html)
        page.wait_for_timeout(100)
        print('js',width,'scroll',page.evaluate('document.documentElement.scrollWidth'),'viewport',width,'visible_cards',page.locator('article.event-card:visible').count(),'form_visible',page.locator('form:visible').count())
        assert page.evaluate('document.documentElement.scrollWidth') <= width
        assert page.locator('article.event-card:visible').count()>=1
        disclosure = page.locator('#filter-disclosure')
        if width <= 600:
            assert not disclosure.evaluate('(element) => element.open'), 'Mobile filters should start collapsed'
            assert page.locator('form:visible').count() == 0
            page.locator('summary').click()
        else:
            assert disclosure.evaluate('(element) => element.open'), 'Desktop filters should start expanded'
        assert page.locator('form:visible').count() == 1
        page.select_option('#filter-area','Vermillion')
        print('js filter Vermillion',page.locator('article.event-card:visible').count())
        assert page.locator('article.event-card:visible').count() == 2
        page.check('#filter-free')
        page.select_option('#filter-range', 'all')
        page.locator('#event-filters button[type=reset]').click()
        page.wait_for_timeout(100)
        assert page.locator('article.event-card:visible').count() == 4, 'Reset should clear filters and update displayed cards'
        page.close()
    p2=browser.new_page(java_script_enabled=False,viewport={'width':320,'height':800})
    p2.set_content(html)
    print('no-js','scroll',p2.evaluate('document.documentElement.scrollWidth'),'cards',p2.locator('article.event-card:visible').count(),'form_hidden',p2.locator('form:visible').count())
    assert p2.locator('article.event-card:visible').count()==6
    assert p2.locator('form:visible').count()==0
    assert p2.evaluate('document.documentElement.scrollWidth')<=320
    browser.close()
