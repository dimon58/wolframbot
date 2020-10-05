from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
import asyncio
import pyppeteer

session = WolframLanguageSession(r"C:\Program Files\Wolfram Research\Wolfram Engine\12.1\WolframKernel.exe")


async def natural_language_process(querry):
    res = session.evaluate(wl.WolframAlpha(querry))
    return res


def encode_hex_for_wl(s: str):
    res = ''
    for i in s:
        if i.isalpha() or i.isdigit():
            res += i
        else:
            if i.isspace():
                res += '+'
            else:
                res += '%' + i.encode('ascii').hex().upper()
    return res


async def page_screenshot(url,
                          xpath='/html/body/div[1]/div/div/main/div[2]/div/div[2]',
                          out_file_name='WolframScreen.png'):
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto(url)
    await asyncio.sleep(10)
    await page.setViewport(dict(width=3840, height=2160))
    # await page.waitForXPath('/html')
    element = await page.xpath(xpath)
    await element[0].screenshot({'path': 'temp/' + out_file_name})
    await browser.close()
    return 'temp/' + out_file_name

async def wolfram(cmd):
    _url = encode_hex_for_wl(cmd)
    return await page_screenshot(f'https://www.wolframalpha.com/input/?i={_url}')
