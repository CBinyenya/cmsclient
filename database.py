import os
import sqlite3


class Alldatabase:

    @staticmethod
    def createOpendb():
        db_is_new = os.path.exists('databases/groups.db')
        table = 'group_t'
        if db_is_new:            
            return
        
        else:
            print 'Creating database...'
            filename = 'databases/groups.db'
            conn = sqlite3.connect(filename)
            print 'Creating schema...'
            
            """Database Functions Creation """
            schema_filename = 'databases/groups_schema.sql'           
         
            conn = sqlite3.connect(filename)
            try:
            
                if (table) not in filename:
                    print 'Creating groups table...'
                    conn.execute('''CREATE TABLE cgroups(
                        Id_no integer primary key autoincrement,
                        gName text,
                        NoofMembers integer);''')              
                
                    print 'Table created successfully'                
                    
                else: pass
            
            
                if (table) not in filename:
                    print 'Creating groups table...'
                    conn.execute('''CREATE TABLE group_t(
                        Id_no integer primary key,
                        fname text,                        
                        mname text,
                        sname text,
                        phone integer,
                        email text,
                        address text,                    
                        city text,
                        groups text);''')
                
                
                    print 'Table created successfully'
                
                    conn.commit()
                    conn.close()
                
                else: pass
            except sqlite3.OperationalError,e:
                print "Tables exists"
                pass
            finally:
                pass             
                    
                                
                
        
    
    
    createOpendb()
