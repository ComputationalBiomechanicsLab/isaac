import os
import subprocess
import tempfile
import unittest

class TestInstalledSoftware(unittest.TestCase):

    def test_tensorrt_is_installed(self):
        p = subprocess.run("dpkg -l | grep -i tensorrt", shell=True, capture_output=True)
        self.assertEqual(p.returncode, 0)
        self.assertEqual(p.stdout.count(b'\n'), 1)

    def test_cuda_compiler_is_installed(self):
        p = subprocess.run("nvcc --version", shell=True)
        self.assertEqual(p.returncode, 0)
    
    def test_cuDNN_is_installed(self):
        # https://stackoverflow.com/questions/31326015/how-to-verify-cudnn-installation

        # generate C source for printing cuDNN's version
        test_src = """
#include <cudnn.h>
#include <stdio.h>

int main(char** argv, int argc)
{
    printf("%i.%i.%i\\n", CUDNN_MAJOR, CUDNN_MINOR, CUDNN_PATCHLEVEL);
    return 0;
}
"""
        with tempfile.TemporaryDirectory() as dir:
            # compile it in a temporary dir
            src_filepath = os.path.join(dir, "src.c")
            with open(src_filepath, "w") as f:
                f.write(test_src)
            out_filepath = os.path.join(dir, "out")
            p = subprocess.run(f"gcc {src_filepath} -o {out_filepath}", shell=True)
            self.assertEqual(p.returncode, 0)
            self.assertTrue(os.path.exists(out_filepath))

            # run the compiled binary
            p2 = subprocess.run(out_filepath, shell=True, capture_output=True)
            self.assertEqual(p2.returncode, 0)
            self.assertEqual(p2.stdout.count(b'\n'), 1)
    
    def test_both_GPUs_are_detected(self):
         p = subprocess.run("nvidia-smi | grep A5000", shell=True, capture_output=True)
         self.assertEqual(p.returncode, 0)
         self.assertEqual(p.stdout.count(b'\n'), 2)

    def test_tensorflow_on_base_system_detects_both_GPUs(self):
        # care: there appears to be a bug related to double-registering cuDNN atm: https://github.com/tensorflow/tensorflow/issues/62075
        p = subprocess.run('/usr/bin/python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices(\'GPU\'))"', shell=True, capture_output=True)
        self.assertEqual(p.returncode, 0)
        self.assertEqual(p.stdout.count(b'PhysicalDevice'), 2)
    
    def test_tensorflow_on_base_conda_environment_detects_both_GPUs(self):
        # care: there appears to be a bug related to double-registering cuDNN atm: https://github.com/tensorflow/tensorflow/issues/62075
        p = subprocess.run('conda run -n base python -c "import tensorflow as tf; print(tf.config.list_physical_devices(\'GPU\'))"', shell=True, capture_output=True)
        self.assertEqual(p.returncode, 0)
        self.assertEqual(p.stdout.count(b'PhysicalDevice'), 2)

    def test_opensim_cmd_installed(self):
        p = subprocess.run("opensim-cmd --version", shell=True)
        self.assertEqual(p.returncode, 0)

    def test_scone_cmd_is_installed(self):
        p = subprocess.run("sconecmd --version", shell=True)
        self.assertEqual(p.returncode, 0)

    def test_blender_is_installed(self):
        p = subprocess.run("blender --version", shell=True)
        self.assertEqual(p.returncode, 0)
    
    def test_conda_is_installed(self):
        p = subprocess.run("conda --version", shell=True)
        self.assertEqual(p.returncode, 0)
    
    def test_bme_specific_commands_exist(self):
        bme_commands_in_user_facing_readme = [
            "bme_vnc-passwd",
            "bme_vnc-restart",
            "bme_vnc-start",
            "bme_vnc-stop",
        ]
        for cmd in bme_commands_in_user_facing_readme:
            p = subprocess.run(f"which {cmd}", shell=True)
            self.assertEqual(p.returncode, 0)

if __name__ == '__main__':
    unittest.main()
