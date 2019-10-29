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

    "${PYBIN}/pip" install -U pip setuptools wheel
    "${PYBIN}/pip" install -r /io/requirements.txt
    "${PYBIN}/python" /io/setup.py sdist bdist_wheel
    auditwheel repair /io/dist/*.whl --plat $PLAT -w /io/dist/
    "${PYBIN}/pip" install xmlstarlet --no-index -f /io/dist && "${PYBIN}/pytest" -v
    "${PYBIN}/twine" check /io/dist/* && "${PYBIN}/twine" upload io/dist/*
done
