import time
from bs4 import BeautifulSoup

advisories = BeautifulSoup(open("announce/index.html"))

for link in advisories.find_all('a'):
    # create a new advisory now
    # path = href, title = text
    href = link.get('href')
    if "announce" in href:

        filename = href.replace('/security/', '')

        #TODO break data out into a model
        # make_advisory_from_file href
        advisory = BeautifulSoup(open(filename))
        data = {}

        data['headline'] = advisory.find('h1').get_text()
        data['id'] = link.get_text().replace('MFSA ', '')

        meta = advisory.find('h1').find_next_sibling('p')

        meta_fields = {
            'Title:': 'title',
            'Impact:': 'impact',
            'Announced:': 'date_s',
            'Reporter:': 'reporter',
            'Products:': 'products',
            'Fixed in:': 'fixed_in'
        }

        for key, value in meta_fields.iteritems():
            element = meta.find(text=key)
            if (element): 
                if "products" in value:
                    data[value] = []
                    for product in element.parent.next_sibling.split(','):
                        data[value].append(product.strip())
                elif "fixed_in" in value:
                    data[value] = []
                    data[value].append(element.parent.next_sibling.strip())
                    for sibling in element.parent.find_next_siblings():
                        for string in sibling.stripped_strings:
                            data[value].append(string.strip())
                else:
                    data[value] = element.parent.next_sibling.strip()

        data['date'] = time.strptime(data['date_s'], '%B %d, %Y')

        description = advisory.find('h3', text='Description')
        if description:
            data['description'] = description.find_next_sibling('p')

        references = advisory.find('h3', text="References")
        if references:
            data['references'] = references.find_next_siblings()[0]

        print data


