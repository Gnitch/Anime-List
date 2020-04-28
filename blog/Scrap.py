import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError

class Scrap():

    def __init__(self, title):
        self.title = title

    def scrap(self):
        s = self.title
        newS = ''
        for each in s :
            if(each != ' '):
                newS = newS + each      
            else :
                newS = newS + str('%')

        url = 'https://myanimelist.net/search/all?q='+newS
        try :
            url = urlopen(url)
            bs = BeautifulSoup(url,'html.parser')
            new_url = bs.find( 'div', { 'class' : 'information di-tc va-t pt4 pl8' } )
            children = new_url.findChildren('a',recursive=False)
            newUrl = children[0]['href']
            newUrl = urlopen(newUrl)
            bs = BeautifulSoup(newUrl,'html.parser')
            para = bs.find('span', { 'itemprop' : 'description'}).get_text()
            rem =  len(para)-24

            genre = bs.findAll( 'span', {"itemprop": "genre"} )
            genreStr='Genre:'
            i=0
            for each in genre :
                if(i==0):
                    i += 1
                    genreStr = genreStr + each.get_text()
            
                else :
                    genreStr = genreStr+str(',')+ each.get_text()

            div_all = bs.findAll( 'div',{'class':'spaceit'} )
            stat = div_all[0].get_text().strip()
            episodes = ''
            for i in range(len(stat)-1,0,-1) :
                if(stat[i] == ' '):
                    break
                else :
                    episodes = stat[i] + episodes

            divOP = bs.find('div', {'class':'theme-songs js-theme-songs opnening'})
            divED = bs.find('div', {'class':'theme-songs js-theme-songs ending'})
            childrenOp = divOP.findChildren('span',recursive=False)
            childrenED = divED.findChildren('span',recursive=False)
            op_list = '' 
            for each_OP in childrenOp :
                op_list = op_list + each_OP.get_text() + ','

            ed_list = ''
            for each_ED in childrenED :
                ed_list = ed_list + each_ED.get_text() + ','
            op = ''
            ed = ''
            flag_op = False 
            flag_ed = False
            for each_op in op_list:
                print(each_op)
                if(each_op == ':'):
                    flag_op = True
                    continue

                if(each_op == ','):
                    op =op +each_op
                    flag_op= False
                
                if(flag_op == True ) :
                    op = op +each_op


            for each_ed in ed_list:

                if( each_ed==':'):
                    flag_ed =True
                    continue
    
                if(each_ed == ','):
                    ed = ed + each_ed
                    flag_ed = False

                if(flag_ed == True) :
                    ed = ed +each_ed
       

            if(len(childrenOp)==1 and len(childrenED)==1) :
                return str(para[:rem]), genreStr, episodes, op_list, ed_list
                
            elif(len(childrenOp)==1):
                return str(para[:rem]), genreStr, episodes, op_list, ed

            elif(len(childrenED)==1):
                return str(para[:rem]), genreStr, episodes, op, ed_list
        
            else :
                return str(para[:rem]), genreStr, episodes, op, ed

        except HTTPError as e :
            return e


