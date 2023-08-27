const { chromium } = require('playwright');

const FEED_URL = 'https://www.luminor.lv/lv/rss.xml';

async function getresponse(context) {
    const page = await context.newPage();

    const response = await page.goto(FEED_URL);
    const contentType = await response.headerValue('content-type');
    console.error('Goto', response.url(), response.status(), response.statusText(), contentType);

    if (response.ok() && contentType == 'text/html') {
        console.error('Waiting for F5 Networks JS');
        return page.waitForResponse(FEED_URL, {timeout: 10000});
    }

    return response;
}

(async () => { 
    const browser = await chromium.launch({ headless: true }); 
    const context = await browser.newContext();

    const response = await getresponse(context);
    const contentType = await response.headerValue('content-type');
    const text = await response.text();
    console.error('Response', response.url(), response.status(), response.statusText(), contentType);

    await context.close();
    await browser.close(); 

    if (response.ok() && contentType == 'application/rss+xml; charset=utf-8') {
        console.log(text);
    } else {
        process.exit(1);
    }
})();
