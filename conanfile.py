from conans import ConanFile, CMake
from conans.tools import download, unzip, replace_in_file, os_info, SystemPackageTool
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
        unzip(zip_name)

        shutil.move("Celero-%s" % self.version, "Celero")

        replace_in_file(file_path="Celero/CMakeLists.txt",
                search="PROJECT(CeleroProject)",
                replace="PROJECT(CeleroProject)\ninclude(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\nconan_basic_setup()\n")

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
