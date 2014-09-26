from os import getenv
import pymssql

print "Database Connected"

DB_host = 'EVBYMINSD7900\\UCDEV'
DB_user = 'Python'
DB_password = 'Python#1'
DB_database = 'voip_db'



class VoIP_DB:



    def Get_Sub_By_Name(self,Name):
        cmd = 'SELECT TOP 1000\
                    [ID_us]\
                    ,[UserName]\
                    ,[Extension]\
                    ,[voip_db].[dbo].[Location].Location\
                    ,[cur_date]\
                    ,[privateline]\
                    ,[PMC_ID]\
                    FROM [voip_db].[dbo].[users]\
                left join [voip_db].[dbo].[Location] ON [voip_db].[dbo].[users].Location = [voip_db].[dbo].[Location].ID_loc\
                where [UserName] LIKE \'' + Name + '%\''
        #conn = pymssql.connect(host=, user=, password=, database=)
        conn = pymssql.connect(DB_host, DB_user, DB_password, DB_database)
        cursor = conn.cursor()
        cursor.execute(cmd)
        ret = []
        for row in cursor:
            ret.append(row)
        conn.close()
        return ret


    def Get_Sub_By_ID(self,ID):
        cmd = 'SELECT TOP 1000\
                    [ID_us]\
                    ,[UserName]\
                    ,[Extension]\
                    ,[Location]\
                    ,[Password]\
                    ,[VmPassword]\
                    ,[privateline]\
                    ,[PMC_ID]\
                FROM [voip_db].[dbo].[users]\
                where [ID_us] = ' + ID
        #conn = pymssql.connect(host=, user=, password=, database=)

        conn = pymssql.connect(DB_host, DB_user, DB_password, DB_database)
        cursor = conn.cursor()
        cursor.execute(cmd)
        ret = []
        for row in cursor:
            ret.append(row)
        conn.close()
        return ret


    def Get_Sub_By_Field(self,field,value):
        cmd = 'SELECT *\
                FROM [voip_db].[dbo].[users]\
                where ' + field + ' LIKE ' + '\'' + value + '\''
        #conn = pymssql.connect(host=, user=, password=, database=)
        print cmd
        conn = pymssql.connect(DB_host, DB_user, DB_password, DB_database)
        cursor = conn.cursor()
        cursor.execute(cmd)
        ret = []
        for row in cursor:
            ret.append(row)
        conn.close()
        return ret

    def Update_Sub(self,form):
        cmd = 'UPDATE [voip_db].[dbo].[users]\
                SET UserName = \'%s\',\
                    Extension = %s,\
                    Password = \'%s\',\
                    VmPassword = \'%s\',\
                    Location = %s,\
                    Privateline = \'%s\',\
                    PMC_ID = \'%s\'\
                where ID_us = %s' % (form.username.data,form.extension.data,form.password.data,form.vmpassword.data,form.location.data,form.privateline.data,form.pmc_id.data,form.sub_id.data)
        print cmd
        #conn = pymssql.connect(host=, user=, password=, database=)

        conn = pymssql.connect(DB_host, DB_user, DB_password, DB_database)
        cursor = conn.cursor()
        cursor.execute(cmd)
        conn.commit()
        ret = []
        for row in cursor:
            ret.append(row)
        conn.close()
        return ret


    def Get_Locations(self):
        cmd = 'SELECT DISTINCT ID_loc, Location FROM [voip_db].[dbo].[Location]'
        #conn = pymssql.connect(host=, user=, password=, database=)

        conn = pymssql.connect(DB_host, DB_user, DB_password, DB_database)
        cursor = conn.cursor()
        cursor.execute(cmd)
        ret = []
        for row in cursor:
            ret.append(row)
        conn.close()
        return ret
