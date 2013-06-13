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
        data['headline'] = advisory.find('h1').get_text()
        meta = advisory.find('h1').find_next_sibling('p')

        #TODO make these work
        #description = advisory.find(text="Description").find_next_sibling('p')
        #references = advisory.find(text="References").find_next_siblings('p')

        data['title'] = meta.find(text="Title:").parent.next_sibling
        data['impact'] = meta.find(text="Impact:").parent.next_sibling

        #TODO make date
        data['date_s'] = meta.find(text="Announced:").parent.next_sibling

        data['reporter'] = meta.find(text="Reporter:").parent.next_sibling

        data['products'] = meta.find(
                text="Products:"
            ).parent.next_sibling.split(',')

        data['fixed_in'] = []
        fin = meta.find(text="Fixed in:")
        # this gets the first sibling, on the same line
        data['fixed_in'].append(fin.parent.next_sibling)
        # this gets the rest of the siblings
        for sibling in fin.parent.find_next_siblings():
            for string in sibling.stripped_strings:
                data['fixed_in'].append(string)

        print data


