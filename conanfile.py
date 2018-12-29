from conans import ConanFile, CMake
from conans.tools import download, check_sha256, unzip, replace_in_file, os_info, SystemPackageTool
import shutil

class CeleroConan(ConanFile):
    name = "celero"
    version = "2.4.0"
    license = "Apache License Version 2.0"
    url = "https://github.com/DigitalInBlue/Celero-Conan"
    description = "C++ Benchmark Authoring Library/Framework"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    def source(self):

        zip_name = "v%s.zip" % self.version

        download("https://github.com/DigitalInBlue/Celero/archive/%s" % zip_name, zip_name)

        check_sha256(zip_name, "ff39642b0d14fef3eb70afb7154b9393a9b8e12c333aeeb109db1a9c0d762a7c")

        unzip(zip_name)

        shutil.move("Celero-%s" % self.version, "Celero")

        # Add call to conan_basic_setup() at the beginning of CMakeLists.txt
        # This is needed in order to make Visual Studio use the correct runtime
        replace_in_file(file_path="Celero/CMakeLists.txt",
                search="PROJECT(CeleroProject)",
                replace="PROJECT(CeleroProject)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\nconan_basic_setup()\n")

        # Replace _declspec (single underscore) with __declspec (double underscore)
        # Needed by MinGW
        replace_in_file(file_path="Celero/include/celero/Export.h",
                        search="_declspec",
                        replace="__declspec")

    def requirements(self):

        ncurses_pkg = None

        if os_info.is_linux:

            if os_info.linux_distro == "ubuntu":
                ncurses_pkg = "libncurses-dev"
            elif os_info.linux_distro in ("fedora", "centos"):
                ncurses_pkg = "ncurses-devel"

        if ncurses_pkg:
            installer = SystemPackageTool()
            installer.install(ncurses_pkg)

    def build(self):
        cmake = CMake(self)

        if self.options.shared:
            cmake.definitions["CELERO_COMPILE_DYNAMIC_LIBRARIES"] = "ON"
        else:
            cmake.definitions["CELERO_COMPILE_DYNAMIC_LIBRARIES"] = "OFF"

        cmake.definitions["CELERO_ENABLE_EXPERIMENTS"] = "OFF"
        cmake.definitions["CELERO_ENABLE_FOLDERS"] = "OFF"
        cmake.configure(source_folder = self.source_folder + "/Celero/")
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*", src="package")

    def package_info(self):

        if not self.options.shared:
            self.cpp_info.defines = ["CELERO_STATIC"]

        self.cpp_info.libs = ["celerod"] if self.settings.build_type == "Debug" else ["celero"]

        self.cpp_info.libdirs = ["lib","lib/static","bin"]
