import os
from botocore.exceptions import ClientError

class S3helper:
    """
    author:
    - Chris Falck:      chris.falck@tickboxconsulting.com
    params:
    - prefix:           pattern to match in s3
    - local:            local path to folder in which to place files
    - bucket:           s3 bucket with target contents
    - client:           initialised s3 client object
    - preserve_dirs:    bool to determine if s3 dir structure is preserved
    """

    def __init__(self, prefix, local, bucket, client, preserve_dirs):
        print("initialising s3dl class")
        self.prefix         = prefix
        print(self.prefix)
        self.local          = local
        print(self.local)
        self.bucket         = bucket
        print(self.bucket)
        self.client         = client
        print(self.client)
        self.preserve_dirs  = preserve_dirs
        print(self.preserve_dirs)

    def download_dir(self):
        """
        - Download objects from s3 matching the provided prefix
        - S3 Object paths can be preserved by setting 'preserve_dirs' to True
        - S3 Object paths can be removed by setting 'preserve_dirs' to False
        - If 'preserve_dirs' is False, all matched objects will be written directly
          to the 'local' directory
        """

        keys = []
        dirs = []
        next_token = ''
        base_kwargs = {
            'Bucket':self.bucket,
            'Prefix':self.prefix,
        }

        while next_token is not None:
            kwargs = base_kwargs.copy()
            if next_token != '':
                kwargs.update({'ContinuationToken': next_token})

            try:
                results = self.client.list_objects_v2(**kwargs)
            except ClientError as error:
                print("A Client exception occurred: %s" % error)
                return error

            contents = results.get('Contents')

            for i in contents:
                k = i.get('Key')
                if k[-1] != '/':
                    keys.append(k)
                else:
                    dirs.append(k)
            next_token = results.get('NextContinuationToken')
        if self.preserve_dirs:
            for d in dirs:
                dest_pathname = os.path.join(self.local, d)
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))
            for k in keys:
                dest_pathname = os.path.join(self.local, k)
                if not os.path.exists(os.path.dirname(dest_pathname)):
                    os.makedirs(os.path.dirname(dest_pathname))
                self.client.download_file(self.bucket, k, dest_pathname)
        else:
            for k in keys:
                dest_pathname = os.path.join(self.local, os.path.basename(k))
                self.client.download_file(self.bucket, k, dest_pathname)

    def upload_object(self):
        """
        s3_resource.meta.client.upload_file(
        Filename=first_file_name, Bucket=first_bucket_name,
        Key=first_file_name)
        """
        pass

    def delete_object(self):
        """
        s3_resource.Object(second_bucket_name, first_file_name).delete()
        """
        pass

    def delete_all_objects(self):
        """
        def delete_all_objects(bucket_name):
            res = []
            bucket=s3_resource.Bucket(bucket_name)
            for obj_version in bucket.object_versions.all():
                res.append({'Key': obj_version.object_key,
                            'VersionId': obj_version.id})
            print(res)
            bucket.delete_objects(Delete={'Objects': res})
        """
        res = []

        for obj_version in self.bucket.object_versions.all():
            res.append(
                {
                    'Key': obj_version.object_key,
                    'VersionId': obj_version.id
                }
            )
            print(res)
            #bucket.delete_objects(Delete={'Objects': res})

    def delete_bucket(self):
        """
        s3_resource.Bucket(first_bucket_name).delete()  
        """
        pass