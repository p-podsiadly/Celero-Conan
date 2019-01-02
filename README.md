[![Build status](https://ci.appveyor.com/api/projects/status/i0pjaohck68iu2ax?svg=true)](https://ci.appveyor.com/project/p-podsiadly/celero-conan)


# Celero-Conan


[Conan](https://bintray.com/ppodsiadly/conan/celero%3Appodsiadly) package for Celero library.


## Basic setup

    $ conan install celero/2.4.0@ppodsiadly/stable
    
## Project setup

If you handle multiple dependencies in your project is better to add a `conanfile.txt`:
    
    [requires]
    celero/2.4.0@ppodsiadly/stable

    [options]
    celero:shared=True # or False, default is True
    
    [generators]
    cmake
    
    [imports]
    bin, *.dll -> ./bin # Copy Celero's DLL from the package to the build directory

Complete the installation of requirements for your project running:

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files `conanbuildinfo.cmake` with all the paths and variables that you need to link with your dependencies.