# -*- coding: utf-8 -*-
from functools import wraps
from flask import Blueprint, url_for, render_template, request, \
        redirect, g, flash, session, jsonify
import boto3
from botocore.config import Config
import simplejson
import tempfile
from forms import LoginForm, NewBucket



front = Blueprint('frontend', __name__)

def check_login(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if g.logged:
            try:
                return f(*args, **kwargs)
            except:
                return logout()
        flash("You should be logged in to access this page")
        return redirect(url_for('.index'))
    return wrap

def get_location(b):
    return get_client(None).get_bucket_location(Bucket=b)


def get_client(r):
    if r:
        cfg = Config(region_name=r['LocationConstraint'],
                signature_version='s3v4')
        return boto3.client('s3',
                aws_secret_access_key=session.get("key"),
                aws_access_key_id=session.get("id"),
                config=cfg)
    return boto3.client('s3',
            aws_secret_access_key=session.get("key"),
            aws_access_key_id=session.get("id"))


def get_client_location(b):
    return get_client(get_location(b))


@front.before_request
def add_session():
    if session.get("logged"):
        g.logged = True

@front.route('/', methods=['GET', 'POST'])
def index():
    form = None
    if not session.get("logged"):
        form = LoginForm()
        return render_template('frontend/index.html', form=form)
    return redirect(url_for(".buckets"))

@front.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session["logged"] = True
        session["key"] = form.access_key.data
        session["id"] = form.key_id.data
        return redirect(url_for('.buckets'))
    flash("can't login")
    flash(form.errors)
    return redirect(request.referrer or url_for('.index'))

@front.route('/buckets')
@check_login
def buckets():
    if not session.get("logged"):
        return redirec(url_for('.index'))
    b = get_client(None).list_buckets()
    buckets = b['Buckets']
    return render_template('frontend/buckets.html', buckets=buckets)

@front.route('/bucket/<bucket>')
@check_login
def bucket(bucket):
    r = get_client(None).get_bucket_location(Bucket=bucket)
    b = get_client(r).list_objects(Bucket=bucket)
    return render_template('frontend/bucket.html', content=b)

@front.route('/download/<bucket>/<_file>')
@check_login
def download(bucket, _file):
    r = get_client(None).get_bucket_location(Bucket=bucket)
    return redirect(get_client(r).generate_presigned_url('get_object', Params={
        'Bucket': bucket,
        'Key': _file
        }, ExpiresIn=100))

@front.route('/upload', methods=['POST'])
@check_login
def upload_file():
    b = request.args.get('bucket')
    c = get_client_location(b)
    for f in request.files.getlist("file[]"):
        _f = tempfile.TemporaryFile()
        f.save(_f.name)
        c.upload_file(_f.name, b, f.filename)
        _f.close()
    return redirect(request.referrer)

@front.route('/delete/<bucket>/<_file>')
@check_login
def delete_file(bucket, _file):
    c = get_client_location(bucket)
    c.delete_object(Bucket=bucket, Key=_file)
    return redirect(request.referrer)

@front.route('/remove/<bucket>')
@check_login
def remove_bucket(bucket):
    c = get_client_location(bucket)
    try:
        c.delete_bucket(Bucket=bucket)
    except Exception as e:
        flash("Cannot delete bucket %s" % e)
    return redirect(request.referrer)

@front.route('/newBucket', methods=['GET', 'POST'])
@check_login
def create_bucket():
    form = NewBucket()
    if form.validate_on_submit():
        cfg = {"LocationConstraint": form.location.data}
        c = get_client_location(cfg)
        c.create_bucket(Bucket=form.bucket_name.data,
                CreateBucketConfiguration=cfg)
        return redirect(url_for('.bucket', bucket=form.bucket_name.data))
    return render_template('frontend/newBucket.html', form=form)

@front.route("/logout")
@check_login
def logout():
    g.logged = False
    session.clear()
    print session.get("logged"), session.get("key"), session.get("id")
    flash("You've been successfully logged out")
    return redirect(url_for(".index"))
