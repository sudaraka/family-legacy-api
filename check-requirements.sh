#!/usr/bin/env sh

TEMPFILE='/tmp/requirements.txt'

pip freeze | sort > $TEMPFILE 2>/dev/null
DIFF="`cat requirements/*|grep -v '\-r '|sort|diff $TEMPFILE - 2>/dev/null`"

if [ -z "$DIFF" ]; then
    exit 1
fi

echo $DIFF | sed 's/\s*<\s*/\n/g' | tail -n +2
