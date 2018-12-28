from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="ppodsiadly")
    builder.add_common_builds()
    builder.run()
