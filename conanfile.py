from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
import os


class JsonRpcCxxConan(ConanFile):
    name = "json-rpc-cxx"
    description = "JSON-RPC for modern C++"
    topics = ("conan", "json-rpc-cxx", "json-rpc")
    url = "https://github.com/bincrafters/conan-json-rpc-cxx"
    homepage = "https://github.com/jsonrpcx/json-rpc-cxx"
    license = "MIT"
    settings = "compiler"
    no_copy_source = True
    requires = "nlohmann_json/3.7.3"

    @property
    def _source_subfolder(self):
        return os.path.join(self.source_folder, "source_subfolder")

    def configure(self):
        minimal_cpp_standard = "17"
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, minimal_cpp_standard)
        minimal_version = {
            "gcc": "6",
            "clang": "3.9",
            "apple-clang": "10",
            "Visual Studio": "17"
        }
        compiler = str(self.settings.compiler)
        if compiler not in minimal_version:
            self.output.warn(
                "%s recipe lacks information about the %s compiler standard version support." % (self.name, compiler))
            self.output.warn(
                "%s requires a compiler that supports at least C++%s." % (self.name, minimal_cpp_standard))
            return
        version = tools.Version(self.settings.compiler.version)
        if version < minimal_version[compiler]:
            raise ConanInvalidConfiguration("%s requires a compiler that supports at least C++%s." % (self.name, minimal_cpp_standard))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def package(self):
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*", dst="include", src=include_folder)

    def package_id(self):
        self.info.header_only()
