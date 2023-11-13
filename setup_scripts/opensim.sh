#!/usr/bin/env bash

set -xeuo pipefail

git clone --depth 1 --branch 4.4.1 https://github.com/opensim-org/opensim-core
cmake -S opensim-core/dependencies/ -B opensim-core-dependencies-build -DCMAKE_INSTALL_PREFIX=${PWD}/opensim-core-dependencies-install -DCMAKE_BUILD_TYPE=RelWithDebInfo -DOPENSIM_WITH_CASADI=ON -DOPENSIM_WITH_TROPTER=ON
cmake --build opensim-core-dependencies-build/ -j$(nproc)
 cmake -S opensim-core -B opensim-core-build -DOPENSIM_DEPENDENCIES_DIR=${PWD}/opensim-core-dependencies-install -DCMAKE_BUILD_TYPE=RelWithDebInfo -DOPENSIM_WITH_CASADI=ON -DOPENSIM_WITH_TROPTER=ON -DBUILD_JAVA_WRAPPING=OFF -DBUILD_PYTHON_WRAPPING=ON -DCMAKE_INSTALL_PREFIX=/usr/local
cmake --build opensim-core-build -j$(nproc)
LD_LIBRARY_PATH=${PWD}/opensim-core-dependencies-install/simbody/lib:${PWD}/opensim-core-dependencies-install/colpack/lib ctest --test-dir opensim-core-build --output-on-failure -j$(nproc)

# install it
sudo cmake --build opensim-core-build -j$(nproc) --target install
