#!/bin/bash

mysql -uroot -pmysql meiduo_mall < areas.sql

mysql -uroot -pmysql meiduo_mall < goods_data.sql
