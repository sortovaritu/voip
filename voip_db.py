from os import getenv

from contextlib import contextmanager

import flask

import pymssql


DB_host = 'EVBYMINSD7900\\UCDEV'
DB_user = 'Python'
DB_password = 'Python#1'
DB_database = 'voip_new'


@contextmanager
def get_connection(cmd):
    try:
        flask.current_app.logger.info('Connection with Database %s\%s', DB_host, DB_database)
        connection = pymssql.connect(DB_host, DB_user, DB_password, DB_database,login_timeout=10)
        flask.current_app.logger.info('Connection with Database OK')
        yield connection
        connection.close()
        flask.current_app.logger.info('Connection with Database Closed')
    except Exception as ex:
        flask.current_app.logger.error('Connection with Database failed: ' + ex.args)



class VoIP_DB:


    def Get_Sub_By_Name(self, Name):
        cmd = 'SELECT TOP 1000\
                    [voip_new].[dbo].[users].[ID]\
                    ,[UserName]\
                    ,[Extension]\
                    ,[voip_new].[dbo].[locations].Location\
                    ,[DateOfAddition]\
                    ,[PrivateLine]\
                    ,[PMC_ID]\
                    FROM [voip_new].[dbo].[users]\
                left join [voip_new].[dbo].[locations] ON [voip_new].[dbo].[users].Location = [voip_new].[dbo].[locations].ID\
                where [UserName] LIKE \'' + Name + '%\''
        with get_connection(cmd) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(cmd)
                flask.current_app.logger.info('SQL SELECT request')
            except Exception as ex:
                flask.current_app.logger.error('SQL Bad request: ' + ex.args)
            ret = []
            for row in cursor:
                ret.append(row)
        return ret



    def Get_Sub_By_ID(self, ID):
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
        with get_connection(cmd) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(cmd)
                flask.current_app.logger.info('SQL SELECT request')
            except Exception as ex:
                flask.current_app.logger.error('SQL Bad request: ' + ex.args)
            ret = []
            for row in cursor:
                ret.append(row)
        return ret

    def Get_Sub_By_Field(self, field, value):
        cmd = 'SELECT *\
                FROM [voip_db].[dbo].[users]\
                where ' + field + ' LIKE ' + '\'' + value + '\''
        # conn = pymssql.connect(host=, user=, password=, database=)
        print cmd
        conn = pymssql.connect(DB_host, DB_user, DB_password, DB_database)
        cursor = conn.cursor()
        cursor.execute(cmd)
        ret = []
        for row in cursor:
            ret.append(row)
        conn.close()
        return ret

    def Update_Sub(self, form):
        cmd = 'UPDATE [voip_db].[dbo].[users]\
                SET UserName = \'%s\',\
                    Extension = %s,\
                    Password = \'%s\',\
                    VmPassword = \'%s\',\
                    Location = %s,\
                    Privateline = \'%s\',\
                    PMC_ID = \'%s\'\
                where ID_us = %s' % (form.username.data, form.extension.data, form.password.data, form.vmpassword.data, form.location.data, form.privateline.data, form.pmc_id.data, form.sub_id.data)
        print cmd
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
        conn = pymssql.connect(DB_host, DB_user, DB_password, DB_database)
        cursor = conn.cursor()
        cursor.execute(cmd)
        ret = []
        for row in cursor:
            ret.append(row)
        conn.close()
        return ret

    def Get_Locations_List(self):
        cmd = 'SELECT TOP 1000\
                    [voip_new].[dbo].[locations].[ID]\
                    ,[Location]\
                    ,[voip_new].[dbo].[PBX].PBXName\
                    ,[Info]\
                    FROM [voip_new].[dbo].[locations]\
                left join [voip_new].[dbo].[pbx] ON [voip_new].[dbo].[locations].PBX = [voip_new].[dbo].[PBX].ID'
        conn = pymssql.connect(DB_host, DB_user, DB_password, DB_database)
        cursor = conn.cursor()
        cursor.execute(cmd)
        ret = []
        for row in cursor:
            ret.append(row)
        conn.close()
        return ret
