from conans import ConanFile, tools
import os


class JsonRpcCxxConan(ConanFile):
    name = "json-rpc-cxx"
    description = "JSON-RPC for modern C++"
    topics = ("conan", "json-rpc-cxx", "json-rpc")
    url = "https://github.com/bincrafters/conan-json-rpc-cxx"
    homepage = "https://github.com/jsonrpcx/json-rpc-cxx"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    no_copy_source = True
    requires = "jsonformoderncpp/3.7.0"

    _source_subfolder = "source_subfolder"

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
