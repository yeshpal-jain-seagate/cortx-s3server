
import os
import sys
import time
from threading import Timer
import subprocess
from framework import S3PyCliTest
from framework import Config
from framework import logit
from s3client_config import S3ClientConfig

class JCloudTest(S3PyCliTest):
    jcloud_cmd = "java -jar ../jcloudclient.jar"

    def __init__(self, description):
        self.s3cfg = os.path.join(os.path.dirname(os.path.realpath(__file__)), Config.config_file)
        super(JCloudTest, self).__init__(description)

    def setup(self):
        if hasattr(self, 'filename') and hasattr(self, 'filesize'):
            file_to_create = os.path.join(self.working_dir, self.filename)
            logit("Creating file [%s] with size [%d]" % (file_to_create, self.filesize))
            with open(file_to_create, 'wb') as fout:
                fout.write(os.urandom(self.filesize))
        super(JCloudTest, self).setup()

    # return the
    def get_test_config(self):
        if S3ClientConfig.pathstyle:
            config = "-x '%s' -y '%s' -p" % (S3ClientConfig.access_key_id,
                        S3ClientConfig.secret_key)
        else:
            config = "-x '%s' -y '%s'" % (S3ClientConfig.access_key_id,
                        S3ClientConfig.secret_key)
        return config

    def run(self):
        super(JCloudTest, self).run()

    def teardown(self):
        super(JCloudTest, self).teardown()

    def with_cli(self, cmd):
        if 'jcloudclient.jar' in cmd:
            if Config.client_execution_timeout != None:
                cmd = cmd + " --cli-exec-timeout %s" % (Config.client_execution_timeout)
            if Config.request_timeout != None:
                cmd = cmd + " --req-timeout %s" % (Config.request_timeout)
            if Config.socket_timeout != None:
                cmd = cmd + " --sock-timeout %s" % (Config.socket_timeout)
        super(JCloudTest, self).with_cli(cmd)

    def create_bucket(self, bucket_name, region=None):
        if region:
            cmd =  "%s mb s3://%s -l %s %s" % (self.jcloud_cmd,
                    bucket_name, self.get_test_config())
        else:
            cmd =  "%s mb s3://%s %s" % (self.jcloud_cmd,
                    bucket_name, self.get_test_config())

        self.with_cli(cmd)
        return self

    def list_buckets(self):
        cmd =  "%s ls %s" % (self.jcloud_cmd, self.get_test_config())
        self.with_cli(cmd)
        return self

    def delete_bucket(self, bucket_name):
        cmd =  "%s rb s3://%s %s" % (self.jcloud_cmd,
                bucket_name, self.get_test_config())
        self.with_cli(cmd)
        return self

    def list_specific_objects(self, bucket_name, object_pattern):
        cmd =  "%s ls s3://%s/%s %s" % (self.jcloud_cmd, bucket_name,
                object_pattern, self.get_test_config())

        self.with_cli(cmd)
        return self

    def list_objects(self, bucket_name):
        cmd =  "%s ls s3://%s %s" % (self.jcloud_cmd, bucket_name,
                self.get_test_config())
        self.with_cli(cmd)
        return self

    def put_object(self, bucket_name, filename, filesize, prefix=None):
        self.filename = filename
        self.filesize = filesize
        self.prefix = prefix
        if prefix:
            # s3://%s/%s/%s = s3://bucket/prefix/filename
            cmd =  "%s put %s s3://%s/%s/%s %s" % (self.jcloud_cmd, filename,
                    bucket_name, prefix, filename, self.get_test_config())
        else:
            cmd =  "%s put %s s3://%s %s" % (self.jcloud_cmd, filename,
                    bucket_name, self.get_test_config())

        self.with_cli(cmd)
        return self

    def put_object_multipart(self, bucket_name, filename, filesize, size_of_part):
        self.filename = filename
        self.filesize = filesize

        cmd =  "%s put %s s3://%s -m %s %s" % (self.jcloud_cmd, filename,
                bucket_name, str(size_of_part), self.get_test_config())

        self.with_cli(cmd)
        return self

    def get_object(self, bucket_name, filename):
        cmd =  "%s get s3://%s/%s %s %s" % (self.jcloud_cmd,
                bucket_name, filename, filename, self.get_test_config())
        self.with_cli(cmd)
        return self

    def delete_object(self, bucket_name, filename):
        cmd =  "%s del s3://%s/%s %s" % (self.jcloud_cmd,
                bucket_name, filename, self.get_test_config())
        self.with_cli(cmd)
        return self

    def delete_multiple_objects(self, bucket_name, objects):
        self.bucket_name = bucket_name
        cmd =  "%s multidel s3://%s " % (self.jcloud_cmd,
                bucket_name)

        for i, object in enumerate(objects):
            cmd += " " + object

        cmd += " " + self.get_test_config()
        self.with_cli(cmd)
        return self

    def partial_multipart_upload(self, bucket_name, filename, filesize,
        size_of_part, no_of_parts):
        self.filename = filename
        self.filesize = filesize
        cmd =  "%s partialput %s s3://%s %s -m %s %s" % (self.jcloud_cmd,
            filename, bucket_name, str(no_of_parts), str(size_of_part),
            self.get_test_config())

        self.with_cli(cmd)
        return self

    def list_multipart(self, bucket_name):
        cmd = "%s multipart s3://%s %s" % (self.jcloud_cmd, bucket_name,
            self.get_test_config())

        self.with_cli(cmd)
        return self

    def list_parts(self, bucket_name, file_name, upload_id):
        cmd = "%s listmp s3://%s/%s %s %s" % (self.jcloud_cmd, bucket_name,
            file_name, upload_id, self.get_test_config())

        self.with_cli(cmd)
        return self

    def abort_multipart(self, bucket_name, file_name, upload_id):
        cmd = "%s abortmp s3://%s/%s %s %s" % (self.jcloud_cmd, bucket_name,
            file_name, upload_id, self.get_test_config())

        self.with_cli(cmd)
        return self

    def check_bucket_exists(self, bucket_name):
        cmd = "%s exists s3://%s %s" % (self.jcloud_cmd, bucket_name,
            self.get_test_config())

        self.with_cli(cmd)
        return self

    def head_object(self, bucket_name, file_name):
        cmd = "%s head s3://%s/%s %s" % (self.jcloud_cmd, bucket_name,
            file_name, self.get_test_config())

        self.with_cli(cmd)
        return self

    def partial_multipart_upload(self, bucket_name, filename, filesize,
        size_of_part, no_of_parts):
        self.filename = filename
        self.filesize = filesize
        cmd =  "%s partialput %s s3://%s %s -m %s %s" % (self.jcloud_cmd,
            filename, bucket_name, str(no_of_parts), str(size_of_part),
            self.get_test_config())

        self.with_cli(cmd)
        return self

    def list_multipart(self, bucket_name):
        cmd = "%s multipart s3://%s %s" % (self.jcloud_cmd, bucket_name,
            self.get_test_config())

        self.with_cli(cmd)
        return self

    def list_parts(self, bucket_name, file_name, upload_id):
        cmd = "%s listmp s3://%s/%s %s %s" % (self.jcloud_cmd, bucket_name,
            file_name, upload_id, self.get_test_config())

        self.with_cli(cmd)
        return self

    def abort_multipart(self, bucket_name, file_name, upload_id):
        cmd = "%s abortmp s3://%s/%s %s %s" % (self.jcloud_cmd, bucket_name,
            file_name, upload_id, self.get_test_config())

        self.with_cli(cmd)
        return self

    def get_bucket_location(self, bucket_name):
        cmd = "%s location s3://%s %s" % (self.jcloud_cmd, bucket_name,
            self.get_test_config())

        self.with_cli(cmd)
        return self

    # acl_action = acl-public or acl-private
    # acl_action = acl-grant, perm = PERM:UserCanonicalID[:DisplayName]
    # acl_action = acl-revoke, perm = perm = PERM:UserCanonicalID
    def set_acl(self, bucket_name, file_name=None, action="acl-public", permission=""):
        assert action in ["acl-public", "acl-private", "acl-grant", "acl-revoke"]
        self.bucket_name = bucket_name
        self.file_name = file_name
        acl_action = action

        if action == "acl-grant" or action == "acl-revoke":
            acl_action = action + "=" + permission

        if file_name:
            cmd = "%s setacl s3://%s/%s %s %s" % (self.jcloud_cmd, bucket_name,
                file_name, acl_action, self.get_test_config())
        else:
            cmd = "%s setacl s3://%s %s %s" % (self.jcloud_cmd, bucket_name, acl_action,
                self.get_test_config())

        self.with_cli(cmd)
        return self

    def get_acl(self, bucket_name, file_name=None):
        self.bucket_name = bucket_name
        self.file_name = file_name

        if file_name:
            cmd = "%s getacl s3://%s/%s %s" % (self.jcloud_cmd, bucket_name,
                file_name, self.get_test_config())
        else:
            cmd = "%s getacl s3://%s %s" % (self.jcloud_cmd, bucket_name,
                self.get_test_config())

        self.with_cli(cmd)
        return self
