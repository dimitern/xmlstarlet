#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y libxslt-devel

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    set +x
    if [ "$(basename $(dirname ${PYBIN}) | cut -d'-' -f1)x" = "cp27x" ]; then
        continue
    fi

    if [ "$(basename $(dirname ${PYBIN}) | cut -d'-' -f1)x" = "cp34x" ]; then
        continue
    fi

    if [ "$(basename $(dirname ${PYBIN}) | cut -d'-' -f1)x" = "cp35x" ]; then
        continue
    fi
    set -x

    pushd /io/ > /dev/null 2>&1
    "${PYBIN}/pip" install -U pip setuptools wheel
    "${PYBIN}/pip" install -r requirements.txt
    "${PYBIN}/python" setup.py sdist bdist_wheel
    auditwheel repair dist/*.whl --plat $PLAT -w dist/
    "${PYBIN}/pip" install xmlstarlet --no-index -f dist && "${PYBIN}/pytest" -v
    "${PYBIN}/twine" check dist/* || exit 1
    rm -f dist/*linux_x64_32* dist/*.tar.* || true
    "${PYBIN}/twine" upload dist/* || true
    rm -fr build/* dist/* || true
    popd > /dev/null 2>&1
done
