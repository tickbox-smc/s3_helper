# s3_helper

## Params
-account_profile dev-ic
-bucket_name cep-2310
-prefix AWSLogs/871281896564/vpcflowlogs/eu-west-2/2020/06/03/871281896564_vpcflowlogs_eu-west-2_fl-07992f874e91b9f8c_20200603T13 
-target_dir /tmp 
-preserve_keys False

## NOTE: s3c is a initialised s3 client object
sess    = boto3.Session(profile_name=account_profile)
s3c     = sess.client('s3',region_name='eu-west-2')

d = S3helper(prefix, target_dir, bucket_name, s3c, preserve_keys)
dl = d.download_dir()
print('Error Downloading objects from S3 %s' % dl)

#### Get a directory tree
l = S3helper(args.prefix, dir, args.bucket_name, s3c, args.preserve_keys)
tree = l.tree()
print(tree)