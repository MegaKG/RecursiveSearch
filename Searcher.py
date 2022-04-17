#!/usr/bin/env python3
import PythonSimpleSQL5 as PSS

class searcher:
    def __init__(self,Config={}):
        self.DB = PSS.mysqlcon(
            Config['DB_Host'],
            Config['DB_User'],
            Config['DB_Password'],
            Config['DB_Database'],
            int(Config['DB_Port'])
            )
        
        if Config['DB_Table'] not in self.DB.showtables():   
            self.DB.maketable(Config['DB_Table'],{
                'Terms':'VARCHAR(64)',
                'URL':'VARCHAR(128)',
                'Description':'TEXT(512)'
            })
            self.DB.enable_full_text(Config['DB_Table'],'Terms')


    def search(self,Term):
        Output = []


    def __del__(self):
        pass


    
    
    

        