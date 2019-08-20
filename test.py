import os
import shutil
import tempfile
import unittest

from baroque.baroque_project import BaroqueProject


class TestBaroque(unittest.TestCase):

    def test_create_project(self):
        tmp_dir = tempfile.mkdtemp()
        source_dir_tmp = os.path.join(tmp_dir, "source")
        dst_dir_tmp = os.path.join(tmp_dir, "destination")
        os.makedirs(source_dir_tmp)
        os.makedirs(dst_dir_tmp)
        project = BaroqueProject(source_dir_tmp, dst_dir_tmp)
        self.assertEqual(project.source_directory, source_dir_tmp)
        self.assertEqual(project.destination_directory, dst_dir_tmp)
        shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    unittest.main()
