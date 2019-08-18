print(" ") 
print("==============Script starts here==============") 
print(" ") 
import sys
import os
import ctypes
import winreg
import getpass
import wmi
#import psutil

username = getpass.getuser()

#process = psutil.Process(os.getpid())

def get_registry_value(key, subkey, value):
    if sys.platform != 'win32':
        raise OSError("get_registry_value is only supported on Windows")
        
    import winreg
    key = getattr(winreg, key)
    handle = winreg.OpenKey(key, subkey)
    (value, type) = winreg.QueryValueEx(handle, value)
    return value

class SystemInformation:
    def __init__(self):
        self.os = self._os_version().strip()
        self.cpu = self._cpu().strip()
        self.browsers = self._browsers()
        self.totalRam, self.availableRam = self._ram()
        self.totalRam = self.totalRam / (1024*1024*1024*1024*1024)
        self.availableRam = self.availableRam / (1024*1024*1024*1024*1024)
        self.hdTotal = self._disk_c2() / (1024*1024*1024)
        self.hdFree = self._disk_c() / (1024*1024*1024)
    
    def _os_version(self):
        def get(key):
            return get_registry_value(
                "HKEY_LOCAL_MACHINE", 
                "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion",
                key)
        os = get("ProductName")
        build = get("CurrentBuildNumber")
        return "%s (build %s)" % (os, build)
            
    def _cpu(self):
        return get_registry_value(
            "HKEY_LOCAL_MACHINE", 
            "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
            "ProcessorNameString")
            
    def _firefox_version(self):
        try:
            version = get_registry_value(
                "HKEY_CURRENT_USER", 
                "Software\\Mozilla\\Mozilla Firefox",
                "CurrentVersion")
            version = (u"Mozilla Firefox", version)
        except WindowsError:
            version = None
        return version
        
    def _iexplore_version(self):
        try:
            version = get_registry_value(
                "HKEY_LOCAL_MACHINE", 
                "SOFTWARE\\Microsoft\\Internet Explorer",
                "Version")
            version = (u"Internet Explorer", version)
        except WindowsError:
            version = None
        return version
		
    def _chrome_version(self):
        try:
            version = get_registry_value(
                "HKEY_CURRENT_USER", 
                "Software\\Google\\Chrome\\BLBeacon",
                "version")
            version = (u"Google Chrome", version)
        except WindowsError:
            version = None
        return version
        
    def _browsers(self):
        browsers = []
        firefox = self._firefox_version()
        if firefox:
            browsers.append(firefox)
        iexplore = self._iexplore_version()
        if iexplore:
            browsers.append(iexplore)
        chrome = self._chrome_version()
        if chrome:
            browsers.append(chrome)
            
        return browsers
    
    def _ram(self):
        kernel32 = ctypes.windll.kernel32
        c_int32 = ctypes.c_int32
        c_uint64 = ctypes.c_uint64
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [
                 ('length', c_int32),
                 ('memoryLoad', c_int32),
                 ('totalPhys', c_uint64),
                 ('availPhys', c_uint64),
                 ('totalPageFile', c_uint64),
                 ('availPageFile', c_uint64),
                 ('totalVirtual', c_uint64),
                 ('availVirtual', c_uint64),
                 ('availExtendedVirtual', c_uint64)
		    ]
    
        memoryStatus = MEMORYSTATUS()
        memoryStatus.length = ctypes.sizeof(MEMORYSTATUS)
        kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))
        return (memoryStatus.totalPhys, memoryStatus.availPhys)
        
    def _disk_c(self):
        drive = (os.getenv("SystemDrive"))
        freeuser = ctypes.c_int64()
        total = ctypes.c_int64()
        free = ctypes.c_int64()
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(drive, 
                                        ctypes.byref(freeuser), 
                                        ctypes.byref(total), 
                                        ctypes.byref(free))
        return freeuser.value

    def _disk_c2(self):
        drive = (os.getenv("SystemDrive"))
        freeuser = ctypes.c_int64()
        total = ctypes.c_int64()
        free = ctypes.c_int64()
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(drive, 
                                        ctypes.byref(freeuser), 
                                        ctypes.byref(total), 
                                        ctypes.byref(free))
        return total.value

if __name__ == "__main__":
    s = SystemInformation()
    print ("Host Name: " + os.environ['COMPUTERNAME'])
    print ("User Name: " + username)
    print ("Operating System: " + s.os)
    print ("CPU: " + s.cpu)
    print ("Browsers: ")
    print ("\n".join(["   %s %s" % b for b in s.browsers]))
    print ("RAM : %dMb total" % s.totalRam)
    #print(process.memory_info().rss / (1024*1024))
    print ("RAM : %dMb free" % s.availableRam)
c = wmi.WMI()
for pm in c.Win32_PhysicalMedia():
    print ("HD S/N: "  + pm.Tag, pm.SerialNumber)
	
print ("System HD : %dGb total size" % s.hdTotal)
print ("System HD : %dGb free" % s.hdFree)
print(" ") 
print("===============Script ends here===============")	
print(" ") 