#!/bin/sh

cp load_new_landmarks.sql.template.txt load_new_data.sql
printf $1 >> load_new_data.sql
printf " landmark_queue" >> load_new_data.sql
cat load_new_data.sql
sqlite3 sunspot.db < load_new_data.sql
rm load_new_data.sql
