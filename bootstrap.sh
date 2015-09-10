#!/usr/bin/env bash

yum -y update
yum -y install python27-pip.noarch

pip install twilio
pip install boto3

mkdir -pv /home/ec2-user/send-billing-message-aws-twilio
aws s3 cp s3://bjn-scripts/send-billing-message-aws-twilio /home/ec2-user/send-billing-message-aws-twilio --recursive

cp -rfv send-billing-message-aws-twilio/send-billing-message.py /usr/bin/send-billing-message

cp -rfv send-billing-message-aws-twilio/send-bill-message.service /etc/init.d/send-bill-message
chmod 700 /etc/init.d/send-bill-message
mkdir -pv /var/log/send-billing-message

chkconfig --add send-bill-message
service send-bill-message start

