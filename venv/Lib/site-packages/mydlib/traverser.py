import os
import pickle


def dump_file(obj,file_name):
    with open(file_name,'wb') as fhandle:
        pickle.dump(obj,fhandle)
def load_file(file_name):
    with open(file_name,'rb') as fhandle:
        return pickle.load(fhandle)
    
def get_relative(catalogue):
    
    return catalogue #will implement if needed
    base_dir = catalogue[0][0].split('/')[-1]
    replace_path = '/'.join(catalogue[0][0].split('/')[:-1])
    for i in range(len(catalogue)):
        catalogue[i][0] = catalogue[i][0].replace(replace_path,'')

def create_catalogue_txt(txt_file,file_name):
    """
    txt file: containing 
    book
    books/Project Tuva: Richard Feynman's Messenger Lecture Series - Microsoft Research.html
    books/Best Math Books - A Comprehensive Reading List. - Stumbling Robot core.html
    books/Advanced Topics. - Stumbling Robot.html
    books/All The Math Books You'll Ever Need | Math ∞ Blog.html
    books/Best Math Books - A Comprehensive Reading List. - Stumbling Robot.html
    books/Textbooks (Math and Statistics) - Mathematics - LibGuides at MIT Libraries.html
    books/Noam Nisan, Shimon Schocken - The Elements of Computing Systems_ Building a Modern Computer from First Principles-The MIT Press (2005).pdf
    books/Core Mathematics Subjects. - Stumbling Robot core.html
    books/MIT Department of Physics.html
    books/maths
    books/maths/Carl D. Meyer - Matrix analysis and applied linear algebra. With solutions to problems-SIAM_ Society for Industrial and Applied Mathematics (2001).pdf
    books/maths/pure mathematics
    
    """
    if os.path.isfile(file_name):
        raise ValueError("There already exists a file with same name.\n Please change name")
    if os.path.isfile(txt_file)==False:
        raise ValueError("text file does not exist containing paths.")
    with open(txt_file,'r') as fhandle:
        i =0
        files = []
        path = ''
        catalogue = []
        for line in fhandle:
            if line[-1]=='\n':
                line = line[:-1]
            if i==0:
                i+=1
                
                if '.' in line:
                    path = './'
                    files.append(line)
                else:
                    path = line
                continue
            if '.' in line:
                files.append(line.replace(path,'').replace('/',''))
            else:
                catalogue.append((path,[],files))
                path = line
                files = []
        catalogue.append((path,[],files))
    dump_file(catalogue,file_name)
    #print(catalogue)
    print('created catalogue...')
    
           
            
    
def create_catalogue_traversing(directory,file_name):
    """
    save relative
    
    
    """
    
    
    if os.path.isfile(file_name):
        raise ValueError("There already exists a file with same name.\n Please change name")
    catalogue = list(os.walk(directory))
    
    catalogue = get_relative(catalogue)
    print(catalogue)
    dump_file(catalogue,file_name)
    
#     with open(file_name,'wb') as fhandle:
#         pickle.dump(catalogue,fhandle)
    print("created catagloue...")

def creator(file_name):
    with open(file_name,'w') as f:
        f.write('kk')

def traverse_catalogue(file_name,action_function=creator):
    #file_name : file having catalogue.
    if os.path.isfile(file_name)==False:
        raise ValueError("File given does not exist...")
    catalogue = load_file(file_name)
    if len(catalogue[0][0].split('/'))<=1:
        replace_path = ''
        base_dir = catalogue[0][0].split('/')[-1]
    else:
        base_dir = catalogue[0][0].split('/')[-1]
        replace_path = '/'.join(catalogue[0][0].split('/')[:-1])
    
    if os.path.isdir(base_dir):
        raise ValueError("Directory already exists...",base_dir)
    #os.mkdir(base_dir)
    i = 0
    for path_, dirs, files in catalogue:
        path_ = path_.replace(replace_path,'')
        if path_[0]=='/':
            path_=path_[1:]
        print(path_)
        os.mkdir(path_)
        for file in files:
            file_name_with_path = os.path.join(path_ , file)
            action_function(file_name=file_name_with_path)
            print(file_name_with_path)
            
                
        
            
        
    
    
    
    
    
        
    