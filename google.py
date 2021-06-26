import selenipupser as browser

query = browser.Element('[name=q]')


def visit():
    browser.driver.get('https://google.com')
