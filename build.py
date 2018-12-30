from cpt.packager import ConanMultiPackager

if __name__ == "__main__":

    gcc_versions = ["4.8", "5", "6", "7"]
    clang_versions = ["3.9", "4.0", "6.0"]

    builder = ConanMultiPackager(username="ppodsiadly", gcc_versions=gcc_versions, clang_versions=clang_versions)
    builder.add_common_builds()

    for build in builder.items:
        if build.settings["compiler"] == "gcc":
            build.env_vars["CC"]  = "gcc-%s" % build.settings["compiler.version"]
            build.env_vars["CXX"] = "g++-%s" % build.settings["compiler.version"]
        elif build.settings["compiler"] == "clang":
            build.env_vars["CC"]  = "clang-%s" % build.settings["compiler.version"]
            build.env_vars["CXX"] = "clang++-%s" % build.settings["compiler.version"]

    builder.run()
