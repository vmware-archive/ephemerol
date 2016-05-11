# -*- coding: latin-1 -*-
import os
import re

from ephemerol.JarModule import JarModule


def test_accepts_files_with_jar_suffix():
    assert JarModule.handles("foo.jar")
    assert JarModule.handles(".jar")
    assert JarModule.handles("ファイル.jar")

def test_rejects_files_without_jar_suffix():
    assert not JarModule.handles(".doc")
    assert not JarModule.handles("Jar.doc")
    assert not JarModule.handles("foo.jar.doc")

def test_returns_manifest_content():
    pattern = re.compile("^Manifest-Version.*")
    results = JarModule.do_handle(os.path.join("tests", "commons-fileupload-1.3.1.jar"))
    assert results is not None
    assert pattern.match(results[0][1]) is not None