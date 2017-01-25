# -*- coding: utf-8 -*-:w

from flask_wtf import Form
from wtforms import fields

regions = [
    ("us-east-1", "US East (N. Virginia)"),
    ("us-east-2", "US East (Ohio)"),
    ("us-west-1", "US West (N. California)"),
    ("us-west-2", "US West (Oregon)"),
    ("ca-central-1", "Canada (Central)"),
    ("ap-south-1", "Asia Pacific (Mumbai)"),
    ("ap-northeast-2", "Asia Pacific (Seoul)"),
    ("ap-southeast-1", "Asia Pacific (Singapore)"),
    ("ap-southeast-2", "Asia Pacific (Sydney)"),
    ("ap-northeast-1", "Asia Pacific (Tokyo)"),
    ("eu-central-1", "EU (Frankfurt)"),
    ("eu-west-1", "EU (Ireland)"),
    ("eu-west-2", "EU (London)"),
    ("sa-east-1", "South America (Sao Paulo)")
]

class LoginForm(Form):
    key_id = fields.TextField(u'Access Key ID')
    access_key = fields.TextField(u'Access Key')

class NewBucket(Form):
    bucket_name = fields.TextField(u'Bucket Name')
    location = fields.SelectField(u'Region', choices=regions)

