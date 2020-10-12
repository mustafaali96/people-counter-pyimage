import requests as rq
from bs4 import BeautifulSoup as BS
from tqdm import tqdm
def get_info(res):
    """
    This will extract info about result, provided by libgen.
    input: res , one of results for the search.
    output: info, a dictionary 
            info['author'] : author of the book
            info['title']  : title of the book
            info['pages']  : number of pages in the book
            info['lang']   : language of the book
            info['size']   : size of the book
            info['type']   : file type of the book i.e. pdf, djvu
            info['links']  : links (mirror links)
            info['code']   : book code used by libgen
            info['download_page'] : currently mirror link with source 93.174.95.29 is selected by default.
    """
    info = {}
    
    temp = res.find_all('td')
    info['author'] = temp[1].text
    info['title'] = temp[2].text
    val = ''.join(list(filter(str.isdigit,temp[5].text)))
    try:
        val = int(val)
    except:
        val = 0
     
    info['pages'] = val
    info['lang'] = temp[6].text
    info['size'] = temp[7].text
    info['type'] = temp[8].text
        
    info['links'] = [x.a['href'] for x in temp[9:-1]]
    def get_code(link):
        return link.split('/')[-1]
    info['code'] = get_code(info['links'][0])
    def get_download_page(links):
        for i in links:
            if 'http://93.174.95.29/_ads/' in i:
                return i
        return None
    info['download_page'] = get_download_page(info['links'])
    
    
    
    return info
    
def get_download_link(download_page):
    """
    get dowloadable link from the download page.
    input: download page link
    output: downloadable link
    """
    soup = BS(rq.get(download_page).content,'html.parser')
    base = 'http://93.174.95.29/' #''.join(download_page.split('/')[:-2])
    return base+soup.find_all('td',{"id":'info'})[0].a['href']

def retrieve(download_link,file_name):
    """
    download the file and save to file_name
    input:
            download_link: donwloadable link
            file_name: target file name
    output: 
        None

    """
    rs = rq.get(download_link,stream=True)
    chunk_size = 2000
    
    with open(file_name,'wb') as fhandle:
        for chunk in tqdm(rs.iter_content(chunk_size)):
            fhandle.write(chunk)

    
    
def get_book(book_name='',file_name='',auto=True):
    """
    Downloads a book name given book name
            otherwise tries to extract book name from file name. if both are not present : Error
        if book not found returns False
    input:
            book_name: name of the book
            file_name: name of the file
            auto: True for automatic choice made by code
                  False for selecting one of results ( user can select multiple results.)
    output: 
            True if book is downloaded
            False if book is not downloaded


    """
    if download(book_name=book_name,file_name=file_name,auto=auto)==False:
        book_name = get_better_name(book_name)
        if download(book_name=book_name,file_name=file_name,auto=auto)==False:
            print("Sorry could not find the book  ",book_name)
            return False
    return True
def get_better_name(book_name):

    """
    Sometimes book name is slightly different than entered.
    This will try find more suitable book name using google search.

    """
    return book_name

def download(book_name='',file_name='',auto=True):
    """
    Downloads a book name given book name
            otherwise tries to extract book name from file name. if both are not present : Error
        if book not found returns False
    input:
            book_name: name of the book
            file_name: name of the file
    output: 
            True if book is downloaded
            False if book is not downloaded


    """
    if book_name=='':
        if file_name!='':
            book_name = file_name.split('/')[-1].split('.')[0]
        else:
            raise ValueError("neither book name is provided nor file name")

    search_rs_url = "http://libgen.is/search.php?req=%s&lg_topic=libgen&open=0&view=simple&res=25&phrase=1&column=def"%(book_name)
    def get_results(search_rs_url):
        return BS(rq.get(search_rs_url).content,'html.parser').find_all('tr',{'valign':'top'})
    results = get_results(search_rs_url)
    print("Got all results.....")
    
    infos = [get_info(result) for result in results[1:]]
    #print(infos)
    if len(infos)<1:
        print("No books found for entered name...",book_name)
        return False
            
    
    def to_be_downloaded(infos):
        def comparing(x):
            return x['pages']

        if auto:
            return [max(infos,key=comparing)]
        else:
            i = 0
            for info in infos[:5]:
                print("##"*20)
                print("Result ",str(i+1))
                print("Title: ", info['title'][:70])
                print("Author: ",info['author'])
                print("Pages: ", info['pages'])
                print("Language: ",info['lang'])
                print("Size: ",info['size'])
                i+=1
            print("Enter your selection space seperated ex for result 1 and 3, your enter: 1 3")
            selection = input().split()
            return [infos[int(i)-1] for i in selection]





        return x['pages']
    finals = to_be_downloaded(infos)
    for final in finals:

        download_link = get_download_link(final['download_page'])
        print('download link')
        print(download_link)
        print('File size  ',final['size'])
        print('pages ',final['pages'])
        print('Title',final['title'])
        title = final['title']
        file_type = final['type'].lower()
        if file_name=='':
            file_name = title+file_type 
        print('starting downloading...')
        retrieve(download_link,file_name)
        print('download completed...')
    
    return True
    
    
        
        
    
    