Bridle Common Testing
#####################

Currently this integration test verifies the auto-generated version number::

    west twister \
         --jobs 4 \
         --verbose \
         --inline-logs \
         --testsuite-root bridle/tests/bridle/common
