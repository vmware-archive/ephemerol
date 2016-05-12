# -*- coding: utf-8 -*-

import os
import re

from ephemerol import JavaModule


def test_accepts_files_with_zip_suffix():
    assert JavaModule.handles("foo.zip")
    assert JavaModule.handles(".zip")
    assert JavaModule.handles(u'ファイル.zip')


def test_rejects_files_without_zip_suffix():
    assert not JavaModule.handles(".doc")
    assert not JavaModule.handles("Jar.doc")
    assert not JavaModule.handles("foo.jar.doc")


def test_returns_manifest_content():
    pattern = re.compile("^<\?xml .*")
    results = JavaModule.do_handle(os.path.join("ephemerol", "test", "SampleWebApp-master.zip"))
    assert results is not None
    assert pattern.match(results[0][1]) is not None
