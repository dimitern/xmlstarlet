#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y libxslt-devel

/usr/bin/env

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    if [ "$(basename $(dirname ${PYBIN}) | cut -d'-' -f1)x" = "cp27x" ]; then
        continue
    fi
    if [ "$(basename $(dirname ${PYBIN}) | cut -d'-' -f1)x" = "cp34x" ]; then
        continue
    fi

    if [ "$(basename $(dirname ${PYBIN}) | cut -d'-' -f1)x" = "cp35x" ]; then
        continue
    fi

    "${PYBIN}/pip" install -U pip setuptools wheel
    "${PYBIN}/pip" install -r requirements.txt
    "${PYBIN}/python" setup.py sdist bdist_wheel
    auditwheel repair dist/*.whl --plat $PLAT -w dist/
    "${PYBIN}/pip" install xmlstarlet --no-index -f dist && "${PYBIN}/pytest" -v
    "${PYBIN}/twine" check dist/* && "${PYBIN}/twine" upload dist/*
done
