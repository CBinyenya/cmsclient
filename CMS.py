from multiprocessing import freeze_support
import multiprocessing
import os
import sys
import shutil
import cPickle as Pickle
details = []
def authorizer(cond):
    """Starts the login window and the authentication process"""
    appfile_management("appfiles")
    name = multiprocessing.current_process().name
    global details
    print 'Calling the login form', name
    with cond:
        cond.notify_all()        
        import login        
        
    print '%s log in success preceding to System initialization' % name


def system_initializer(cond,event):
    """Start after authorizer and import sytem files"""
    name = multiprocessing.current_process().name    
    with cond:
        cond.wait()
        if not os.path.exists("appfiles/authorization.dat"):
            sys.exit()
        with open("appfiles/authorization.dat","rb") as confidential:            
            details = Pickle.load(confidential)            
            for user,passwd in details.items():
                details = [user,passwd]               
        
        print '%s running as %s'%( name, details[0])
        import serverManager as SM
        event.set()
        from serverManager import ServerAccess
        server = ServerAccess()
        server.get_appfiles()
        # SM.runKlass(details)
        
        
def user_interfece_builder(cond,event):
    """Start after authorizer and import sytem files"""
    try:
        event.wait()
    except AssertionError,e:
        return
    name = multiprocessing.current_process().name
    with open("appfiles/authorization.dat", "rb") as confidential:
        details = Pickle.load(confidential)            
        for user, passwd in details.items():
            details = [user,passwd]               
    print '%s running'% name
    import AppGUI        
    AppGUI.main(details)
    
def appfile_management(folder):
    try:        
        if os.path.exists(folder):
            shutil.rmtree(folder)         
    except:
        pass
    if not os.path.exists("bin"):
        os.mkdir("bin")
    if not os.path.exists("databases"):
        os.mkdir("databases")
    return
        
if __name__ == '__main__':
    freeze_support()
    condition = multiprocessing.Condition()
    mgr = multiprocessing.Manager()
    namespace = mgr.Namespace()
    namespace.my_list = []

    event = multiprocessing.Event()
    p1 = multiprocessing.Process(name='User authorizer',
                                 target=authorizer, args=(condition,))
    p1.daemon = True
    p2 = multiprocessing.Process(name='Initializer',
                                 target=system_initializer, args=(condition, event))
    p2.daemon = True
    p3 = multiprocessing.Process(name='User Interface',
                                 target=user_interfece_builder, args=(condition, event))
    p3.daemon = True
    p2.start()
    p3.start()    
    p1.start()
    lock = multiprocessing.Lock()
    p3.join()
    p1.join()
    p2.join()
