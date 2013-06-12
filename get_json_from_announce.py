from bs4 import BeautifulSoup

advisories = BeautifulSoup(open("known-vulnerabilities/firefox.html"))

for link in advisories.find_all('a'):
    # create a new advisory now
    # path = href, title = text
    href = link.get('href')
    if "announce" in href:
        filename = href.replace('/security/', '')
        text = link.get_text()

        # make_advisory_from_file href
        advisory = BeautifulSoup(open(filename))
        data = {}
        #data['what_is_this'] = advisory.find('h1').get_text()
        data['title'] = advisory.find(text="Title:").parent.next_sibling
        data['impact'] = advisory.find(text="Impact:").parent.next_sibling
        #TODO make date
        data['date_s'] = advisory.find(text="Announced:").parent.next_sibling
        data['reporter'] = advisory.find(text="Reporter:").parent.next_sibling
        #TODO extract data from products
        data['products'] = advisory.find(text="Products:").parent.next_sibling
        #TODO extract data from fixed_in
        data['fixed_in'] = advisory.find(text="Fixed in:").parent.next_sibling
        print data
        

        

