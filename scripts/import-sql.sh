#!/bin/bash
# This scripsts will do the following things:
# 1.Backup the database juzz4v2
# 2.Import the new juzz4v2.sql

cd ../sql

# Backup the tables in DB
TIME=`date '+%Y%m%d-%H%M%S'`
mysqldump -uroot -pAptx4869 juzz4v2 -pAptx4869 > backup-$TIME-juzz4v2.sql
echo "----backup database juzz4v2 OK. Please see ../sql/backup-$TIME-juzz4v2.sql"

# Drop and create database
mysql -uroot -Djuzz4v2 -pAptx4869 -e "drop database if exists juzz4v2; create database if not exists juzz4v2; use juzz4v2;"

# Import juzz4v2.sql and juzz4v2-update.sql
mysql -uroot -Djuzz4v2 -pAptx4869 < juzz4v2.sql
#mysql -uroot -Djuzz4v2 -pAptx4869 < juzz4v2_update.sql
echo "----import new juzz4v2.sql OK."

cd ../scripts
