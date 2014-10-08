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
    except Exception as ex:
        flask.current_app.logger.error('Connection with Database failed: ' + ex.args)
    yield connection
    connection.close()
    flask.current_app.logger.info('Connection with Database Closed')

def send_select(conn,cmd,sender):
    cursor = conn.cursor()
    ret = []
    try:
        flask.current_app.logger.info('SQL SELECT request: ' + sender)
        flask.current_app.logger.debug(cmd)
        cursor.execute(cmd)
    except Exception:
        flask.current_app.logger.error('SQL bad request: ' + sender)
    for row in cursor:
        ret.append(row)
    return ret


def send_update(conn,cmd,sender):
    cursor = conn.cursor()
    try:
        flask.current_app.logger.info('SQL UPDATE request: ' + sender)
        flask.current_app.logger.debug(cmd)
        cursor.execute(cmd)
        conn.commit()
    except Exception:
        flask.current_app.logger.error('SQL bad request: ' + sender)


def send_update(conn,cmd,sender):
    cursor = conn.cursor()
    try:
        flask.current_app.logger.info('SQL UPDATE request: ' + sender)
        flask.current_app.logger.debug(cmd)
        cursor.execute(cmd)
        conn.commit()
    except Exception:
        flask.current_app.logger.error('SQL bad request: ' + sender)




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
        ret = []
        with get_connection(cmd) as conn:
            try:
                ret = send_select(conn,cmd,self.Get_Sub_By_Name.__name__)
            except Exception as e:
                flask.current_app.logger.error(e.args)
        return ret



    def Get_Sub_By_ID(self, ID):
        cmd = 'SELECT TOP 1000\
                    [ID]\
                    ,[UserName]\
                    ,[Extension]\
                    ,[Location]\
                    ,[Password]\
                    ,[VmPassword]\
                    ,[privateline]\
                    ,[PMC_ID]\
                FROM [voip_new].[dbo].[users]\
                where [ID] = ' + ID
        ret = []
        with get_connection(cmd) as conn:
            try:
                ret = send_select(conn,cmd,self.Get_Sub_By_ID.__name__)
            except Exception as e:
                flask.current_app.logger.error(e.args)
        return ret





    def Get_Sub_By_Field(self, field, value):
        cmd = 'SELECT *\
                FROM [voip_new].[dbo].[users]\
                where ' + field + ' LIKE ' + '\'' + value + '\''
        ret = []
        with get_connection(cmd) as conn:
            try:
                ret = send_select(conn,cmd,self.Get_Sub_By_Field.__name__)
            except Exception as e:
                flask.current_app.logger.error(e.args)
        return ret





    def Update_Sub(self, form):
        cmd = 'UPDATE [voip_new].[dbo].[users]\
                SET UserName = \'%s\',\
                    Extension = %s,\
                    Password = \'%s\',\
                    VmPassword = \'%s\',\
                    Location = %s,\
                    Privateline = \'%s\',\
                    PMC_ID = \'%s\'\
                where ID = %s' % (form.username.data, form.extension.data, form.password.data, form.vmpassword.data, form.location.data, form.privateline.data, form.pmc_id.data, form.sub_id.data)
        with get_connection(cmd) as conn:
            cursor = conn.cursor()
            flask.current_app.logger.info('SQL UPDATE request: Update_Sub')
            cursor.execute(cmd)
            conn.commit()



    def Update_Loc(self, form):
        cmd = 'UPDATE [voip_new].[dbo].[locations]\
                SET Location = \'%s\',\
                    PBX = %s,\
                    Info = \'%s\'\
                where ID = %s' % (form.location.data, form.pbx.data, form.info.data, form.loc_id.data)
        with get_connection(cmd) as conn:
            cursor = conn.cursor()
            flask.current_app.logger.info('SQL UPDATE request: Update_Loc')
            cursor.execute(cmd)
            conn.commit()




    def Add_Loc(self, form):
        cmd = 'INSERT INTO [voip_new].[dbo].[locations]\
                VALUES (\'%s\',%s,\'%s\')' % (form.location.data, form.pbx.data, form.info.data)
        with get_connection(cmd) as conn:
            cursor = conn.cursor()
            flask.current_app.logger.info('SQL UPDATE request: Update_Loc')
            cursor.execute(cmd)
            conn.commit()





    def Get_Locations(self):
        cmd = 'SELECT DISTINCT ID, Location FROM [voip_new].[dbo].[locations]'
        ret = []
        with get_connection(cmd) as conn:
            try:
                ret = send_select(conn,cmd,self.Get_Locations.__name__)
            except Exception as e:
                flask.current_app.logger.error(e.args)
        return ret






    def Get_Locations_List(self):
        cmd = 'SELECT TOP 1000\
                    [voip_new].[dbo].[locations].[ID]\
                    ,[Location]\
                    ,[voip_new].[dbo].[PBX].PBXName\
                    ,[Info]\
                    FROM [voip_new].[dbo].[locations]\
                    left join [voip_new].[dbo].[pbx] ON [voip_new].[dbo].[locations].PBX = [voip_new].[dbo].[PBX].ID'
        ret = []
        with get_connection(cmd) as conn:
            try:
                ret = send_select(conn,cmd,self.Get_Locations_List.__name__)
            except Exception as e:
                flask.current_app.logger.error(e.args)
        return ret



    def Get_Location_By_ID(self,ID):
        cmd = 'SELECT TOP 1000\
                    [ID]\
                    ,[Location]\
                    ,[PBX]\
                    ,[Info]\
                    FROM [voip_new].[dbo].[locations]\
                    where [voip_new].[dbo].[locations].[ID] = ' + ID
        ret = []
        with get_connection(cmd) as conn:
            try:
                ret = send_select(conn,cmd,self.Get_Locations_List.__name__)
            except Exception as e:
                flask.current_app.logger.error(e.args)
        return ret


    def Get_Location_By_Name(self,Location):
        cmd = 'SELECT TOP 1000\
                    [ID]\
                    ,[Location]\
                    ,[PBX]\
                    ,[Info]\
                    FROM [voip_new].[dbo].[locations]\
                    where [voip_new].[dbo].[locations].[Location] = \'' + Location + '\''
        ret = []
        with get_connection(cmd) as conn:
            try:
                ret = send_select(conn,cmd,self.Get_Location_By_Name.__name__)
            except Exception as e:
                flask.current_app.logger.error(e.args)
        return ret



    def Get_PBX(self):
        cmd = 'SELECT TOP 1000\
                    [ID]\
                    ,[PBXName]\
                    FROM [voip_new].[dbo].[pbx]'
        ret = []
        with get_connection(cmd) as conn:
            try:
                ret = send_select(conn,cmd,self.Get_PBX.__name__)
            except Exception as e:
                flask.current_app.logger.error(e.args)
        return ret


    def Get_PBX_List(self):
        cmd = 'SELECT * FROM [voip_new].[dbo].[pbx]'
        ret = []
        with get_connection(cmd) as conn:
            try:
                ret = send_select(conn,cmd,self.Get_Locations_List.__name__)
            except Exception as e:
                flask.current_app.logger.error(e.args)
        return ret