RULEBASE_PATH=./ephemerol/test/rulebase.yml
SOURCE_ZIP_PATH=./ephemerol/test/SampleWebApp-master.zip
MINIMUM_SCAN_INDEX=99

scan_output=`python -m ephemerol $RULEBASE_PATH $SOURCE_ZIP_PATH`

cloud_readiness_index=`echo $scan_output | jq '.scan_stats.cloud_readiness_index'`
echo "$MINIMUM_SCAN_INDEX>$cloud_readiness_index" | bc