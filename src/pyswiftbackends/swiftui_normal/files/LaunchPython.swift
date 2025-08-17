//
//  LaunchPython.swift
//  MySwiftUI
//
//  Created by CodeBuilder on 09/07/2025.
//
import Python
import PySwiftKit
import PySerializing
import PyCallable
import Foundation
import Combine
import PySwiftWrapper

func PyStatus_Exception(_ status: PyStatus) -> Bool {
    PyStatus_Exception(status) == 1
}

extension PyStatus {
    var error: String {
        .init(cString: err_msg)
    }
}

fileprivate func PythonCall<A>(call: PyPointer, _ a: A) throws where
    A: PySerialize {
    let arg = a.pyPointer
    guard let result = PyObject_CallOneArg(call, arg) else {
        PyErr_Print()
        Py_DecRef(arg)
        throw PythonError.call
    }
    Py_DecRef(arg)
    Py_DecRef(result)
}

fileprivate func PythonCall<A, B>(call: PyPointer, _ a: A, _ b: B) throws where
    A: PySerialize,
    B: PySerialize {
    let args = VectorCallArgs.allocate(capacity: 2)
    args[0] = a.pyPointer
    args[1] = b.pyPointer
    guard let result = PyObject_Vectorcall(call, args, 2, nil) else {
        PyErr_Print()
        Py_DecRef(args[0])
        Py_DecRef(args[1])
        args.deallocate()
        throw PythonError.call
    }
    Py_DecRef(args[0])
    Py_DecRef(args[1])
    args.deallocate()
    Py_DecRef(result)
}



//@dynamicMemberLookup
class PyEngine: ObservableObject {
    
    static let shared = PyEngine()
    
    let resourcePath = Bundle.main.resourcePath!
    
    var appFolder: String {
        "\(resourcePath)/app"
    }
    
    var environ = Environment()
    
    var __main__: MainModule = .init()
    
    init() {
        start()
        run_main()
    }
    
    func run_main() {
        
        environ.PYTHONUNBUFFERED = 1
        environ.LC_CTYPE = "UTF-8"
        
        let gil = PyGILState_Ensure()
        guard
            let module_dict = PyDict_New()
        else {
            PyErr_Print()
            fatalError()
        }
        
        let fp = fopen("\(appFolder)/main.py", "rb")
        defer { fclose(fp) }
        print("\nRunning main.py.....")
        
        guard let result = PyRun_File(fp, "main", Py_file_input, module_dict, module_dict) else {
            PyErr_Print()
            fatalError()
        }
        result.decref()
        let module_content = try! [String:PyPointer](object: module_dict)
        print("\ncontent of locals:\n")
        print(module_content)
        print()
        __main__.__main__ = module_content
        PyGILState_Release(gil)
    }
    
//    subscript(dynamicMember member: String) -> PyPointer? {
//        __main__[member]
//    }
}

extension PyEngine {
    @dynamicMemberLookup
    class MainModule {
        var __main__: [String: PyPointer] = [:]
        
        init() {
            
        }
        
        subscript(dynamicMember member: String) -> PyPointer? {
            __main__[member]
        }
        
    }
}

extension PyEngine {
    
    func start() {
        
        let resourcePath = Bundle.main.resourcePath!//.replacingOccurrences(of: " ", with: "\\ ")
        
        var preconfig = PyPreConfig()
        var config = PyConfig()
        
        var wtmp_str: UnsafeMutablePointer<wchar_t>?
        var app_packages_path_str: UnsafeMutablePointer<wchar_t>?
        //var app_module_name: String
        //var app_module_str: UnsafeMutablePointer<CChar>?
        
        //var app_module: PyPointer?
        
        var status: PyStatus
        
        print("Configuring isolated Python...")
        PyPreConfig_InitIsolatedConfig(&preconfig)
        PyConfig_InitIsolatedConfig(&config)
        
        preconfig.utf8_mode = 1
        
        config.buffered_stdio = 0
        
        config.write_bytecode = 0
        
        config.module_search_paths_set = 1
        
        setenv("LC_CTYPE", "UTF-8", 1)
        
        print("Pre-initializing Python runtime...")
        status = Py_PreInitialize(&preconfig)
        if PyStatus_Exception(status) {
            crash_dialog("Unable to pre-initialize Python interpreter: \(status.error)")
            PyConfig_Clear(&config)
            Py_ExitStatusException(status)
        }
        
        
        let python_tag = "3.11"
        let python_home = "\(resourcePath)/python"
        print(python_home, FileManager.default.fileExists(atPath: python_home))
        print("PythonHome: \(python_home)")
        wtmp_str = Py_DecodeLocale(python_home, nil)
        var config_home = config.home
        status = PyConfig_SetString(&config, &config_home, wtmp_str)
        config.home = config_home
        if PyStatus_Exception(status) {
            crash_dialog("Unable to set PYTHONHOME: \(status.error)")
            PyConfig_Clear(&config)
            Py_ExitStatusException(status)
        }
        PyMem_RawFree(wtmp_str)
        
        guard let app_module_name = Bundle.main.object(forInfoDictionaryKey: "MainModule") as? String else {
            fatalError("Unable to identify app module name.")
        }
        app_module_name.withCString { name in
            var run_module = config.run_module
            status = PyConfig_SetBytesString(&config, &run_module, name)
            config.run_module = run_module
        }
        if PyStatus_Exception(status) {
            crash_dialog("Unable to set app module name: \(status.error)")
            PyConfig_Clear(&config)
            Py_ExitStatusException(status)
        }
        
        status = PyConfig_Read(&config)
        if PyStatus_Exception(status) {
            crash_dialog("Unable to read site config: \(status.error)")
            PyConfig_Clear(&config)
            Py_ExitStatusException(status)
        }
        
        print("PYTHONPATH:")
        var path = "\(python_home)/lib/python\(python_tag)"
        print(" - \(path)")
        wtmp_str = Py_DecodeLocale(path, nil)
        status = PyWideStringList_Append(&config.module_search_paths, wtmp_str)
        if PyStatus_Exception(status) {
            crash_dialog("Unable to set PYTHONHOME: \(status.error)")
            PyConfig_Clear(&config)
            Py_ExitStatusException(status)
        }
        PyMem_RawFree(wtmp_str)
        
        path = "\(python_home)/lib/python\(python_tag)/lib-dynload"
        print(" - \(path)")
        wtmp_str = Py_DecodeLocale(path, nil)
        status = PyWideStringList_Append(&config.module_search_paths, wtmp_str)
        if PyStatus_Exception(status) {
            crash_dialog("Unable to set PYTHONHOME: \(status.error)")
            PyConfig_Clear(&config)
            Py_ExitStatusException(status)
        }
        PyMem_RawFree(wtmp_str)
        
        path = "\(resourcePath)/app"
        print(" - \(path)")
        wtmp_str = Py_DecodeLocale(path, nil)
        status = PyWideStringList_Append(&config.module_search_paths, wtmp_str)
        if PyStatus_Exception(status) {
            crash_dialog("Unable to set app path: \(status.error)")
            PyConfig_Clear(&config)
            Py_ExitStatusException(status)
        }
        PyMem_RawFree(wtmp_str)
        
        print("Initializing Python runtime...")
        status = Py_InitializeFromConfig(&config)
        if PyStatus_Exception(status) {
            crash_dialog("Unable to initialize Python interpreter: \(status.error)")
            PyConfig_Clear(&config)
            Py_ExitStatusException(status)
        }
        
        path = "\(resourcePath)/site_packages"
        app_packages_path_str = Py_DecodeLocale(path, nil)
        print("Adding app_packages as site directory: \(path)")
        
        guard let module = PyImport_ImportModule("site") else {
            crash_dialog("Could not import site module")
            exit(-11)
        }
        
        guard let module_attr = PyObject_GetAttrString(module, "addsitedir"), PyCallable_Check(module_attr) == 1 else {
            crash_dialog("Could not access site.addsitedir")
            exit(-12)
        }
        
        guard let app_packages_path = PyUnicode_FromWideChar(app_packages_path_str, wcslen(app_packages_path_str)) else {
            crash_dialog("Could not convert app_packages path to unicode")
            exit(-13)
        }
        PyMem_RawFree(app_packages_path_str)
        
        try? PythonCall(call: module_attr, app_packages_path)
        
        if let err = PyErr_Occurred() {
            crash_dialog("Could not add app_packages directory using site.addsitedir")
            exit(-15)
        }
        
        print("---------------------------------------------------------------------------")
        PyEval_SaveThread()
    }
}




func crash_dialog(_ details: String) {
    print("Application has crashed!")
    print("========================\n\(details)")
}


@discardableResult
private func load_custom_builtin_importer() -> Int32 {
    """
    import sys, imp, types
    from os import environ
    from os.path import exists, join
    try:
        # python 3
        import _imp
        EXTS = _imp.extension_suffixes()
        sys.modules['subprocess'] = types.ModuleType(name='subprocess')
        sys.modules['subprocess'].PIPE = None
        sys.modules['subprocess'].STDOUT = None
        sys.modules['subprocess'].DEVNULL = None
        sys.modules['subprocess'].CalledProcessError = Exception
        sys.modules['subprocess'].CompletedProcess = None
        sys.modules['subprocess'].check_output = None
    except ImportError:
        EXTS = ['.so']
    # Fake redirection to supress console output
    if environ.get('KIVY_NO_CONSOLE', '0') == '1':
        class fakestd(object):
            def write(self, *args, **kw): pass
            def flush(self, *args, **kw): pass
        sys.stdout = fakestd()
        sys.stderr = fakestd()
    # Custom builtin importer for precompiled modules
    class CustomBuiltinImporter(object):
        def find_module(self, fullname, mpath=None):
            # print(f'find_module() fullname={fullname} mpath={mpath}')
            if '.' not in fullname:
                return
            if not mpath:
                return
            part = fullname.rsplit('.')[-1]
            for ext in EXTS:
               fn = join(list(mpath)[0], '{}{}'.format(part, ext))
               # print('find_module() {}'.format(fn))
               if exists(fn):
                   return self
            return
        def load_module(self, fullname):
            f = fullname.replace('.', '_')
            mod = sys.modules.get(f)
            if mod is None:
                # print('LOAD DYNAMIC', f, sys.modules.keys())
                try:
                    mod = imp.load_dynamic(f, f)
                except ImportError:
                    # import traceback; traceback.print_exc();
                    # print('LOAD DYNAMIC FALLBACK', fullname)
                    mod = imp.load_dynamic(fullname, fullname)
                sys.modules[fullname] = mod
                return mod
            return mod
    sys.meta_path.insert(0, CustomBuiltinImporter())
    """.withCString(PyRun_SimpleString)
}
