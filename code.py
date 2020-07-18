# Keyword Counter
# This program takes a url as input and scrapes the page for h-tags, p-tags, and links.

def webscraper(website, keyword):
    import urllib.request, urllib.parse, urllib.error
    from bs4 import BeautifulSoup
    import ssl
    import re
    
    
    # define containers
    re_keyword_dict = dict()
    pwordcount = 0 #count of words in p tags

    
    # ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    
    # get url, open with urllib handle
    dict_sort = ["url", "title", "h1", "h2", "h3", "h4", "h5", "h6", "p", "a", "img", "meta", "p-tag wordcount", "count excl. a href", "total count"]
    tags = ["title", "h1", "h2", "h3", "h4", "h5", "h6", "p", "a", "img", "meta"]
    keyword_lower = keyword.lower()
    re_keyword = keyword_lower.split()
    re_keyword = "[\s_\-\/\.\+]*".join(re_keyword)
    url = urllib.request.Request(website, headers={'User-Agent': 'Chrome/56.0.2924.87'})
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    
    
    # retrieve text in all tags in tags list
    # add words in each tag to re_keyword_dict
    for tag_type in tags:
        print(f"Tag type: {tag_type}")
        tag_words = ""
        for tag in soup.find_all(tag_type):
            if tag_type != "a" and tag_type != "img" and tag_type != "meta":
                print(tag.text.strip())
                tag_words += f"{tag.text.strip().lower()} "
                re_num_keywords_found = len(re.findall(re_keyword, tag_words))
                re_keyword_dict[tag_type] = re_num_keywords_found
                if tag_type =="p":
                    pwordcount += len(tag.text.strip().split())                
            if tag_type == "a":
                print(tag.get("href"))
                try:
                    for tag_text in tag.get("href").split("\n"):
                        tag_words += f"{tag_text.lower()} "
                        re_num_keywords_found = len(re.findall(re_keyword, tag_words))
                        re_keyword_dict[tag_type] = re_num_keywords_found
                except:
                    pass                
            if tag_type == "img":
                tag_text = (tag.get("alt"))
                print(tag_text)
                try:
                    for tag_text in tag.get("alt").split("\n"):
                        tag_words += f"{tag_text.lower()} "
                        re_num_keywords_found = len(re.findall(re_keyword, tag_words))
                        re_keyword_dict[tag_type] = re_num_keywords_found
                except:
                    pass
            if tag_type == "meta":
                if tag.get("name") == "description":
                    print(tag.get("content"))
                    try:
                        for tag_text in tag.get("content").split("\n"):
                            tag_words += f"{tag_text.lower()} "
                            re_num_keywords_found = len(re.findall(re_keyword, tag_words))
                            re_keyword_dict[tag_type] = re_num_keywords_found
                    except:
                        pass

        if tag_type not in re_keyword_dict:
            re_keyword_dict[tag_type] = 0
        print()    
    
    
    #count the number of times keyword appears in file (based on "tags" but excludes a href tags)
    keyword_count_dict = {key:value for key,value in re_keyword_dict.items() if key in (tags) and key != "a"}
    keyword_count = sum(list(keyword_count_dict.values()))
    
    
    #add url, p-tag word count, keyword count excluding a href, and total keywords to re_keyword_dict
    re_keyword_dict["p-tag wordcount"] = pwordcount
    re_keyword_dict["url"] = website
    re_keyword_dict["count excl. a href"] = keyword_count
    re_keyword_dict["total count"] = keyword_count + re_keyword_dict["a"]
    
    
    #sort the dictionary keys
    data_output_list = sorted(re_keyword_dict.items(), key = lambda item: dict_sort.index(item[0]))
    data_output_list = [value for item, value in data_output_list]
        
    
    #print the results
    print("----------------------------")
    print(f"Number of times {keyword} appears on page (excluding a href tags): {keyword_count}\n")
    print(f"RE KEYWORD DICT: {re_keyword_dict}\n")
    print(f"Word count for text in p-tags: {pwordcount}")
   
    return(data_output_list)


def keyword_counter():
    from time import time
    
    #get keyword from user
    keyword = input("Please enter a keyword: ")
    fkeyword = keyword.replace(" ", "-")
    fname = str(fkeyword.lower()) + str(time()) + ".csv"
    
    
    # create the file and write the headers; get a url from user
    with open(fname, "w") as outfile:
        outfile.write("url, title, h1, h2, h3, h4, h5, h6, p, a, img, meta, p-wordcount, count excl. a href, total count")
        outfile.write("\n")
        while True:
            website = input("Please enter a url: ")
            
            if website == "":
                break
            
            output = webscraper(website, keyword)
            
            #output the data from each webscrape
            data_output = f"{output[0]}, {output[1]}, {output[2]}, {output[3]}, {output[4]}, {output[5]}, {output[6]}, {output[7]}, {output[8]}, {output[9]}, {output[10]}, {output[11]}, {output[12]}, {output[13]}, {output[14]}"
            outfile.write(data_output)
            outfile.write("\n")
