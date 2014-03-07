#!/bin/sh
user=jdf
pass=kokoko
host=localhost
database=JDF
echo "DROP VIEW IF EXISTS agency, stops, routes, trips, stop_times, calendar_dates, not_in_map" | mysql -u${user} -p${pass} -h ${host} ${database}
tmp=`mktemp`
echo "SET foreign_key_checks=0;" > $tmp
mysqldump -u${user} -p${pass} -h ${host} --add-drop-table --no-data ${database} | grep ^DROP >> $tmp
cat $tmp | mysql -u${user} -p${pass} -h ${host} ${database}


