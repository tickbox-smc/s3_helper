# s3_helper

## Params
-account_profile dev-ic
-bucket_name cep-2310
-prefix AWSLogs/871281896564/vpcflowlogs/eu-west-2/2020/06/03/871281896564_vpcflowlogs_eu-west-2_fl-07992f874e91b9f8c_20200603T13 
-target_dir /tmp 
-download_data True 
-preserve_keys False

d = S3helper(args.prefix, dir, args.bucket_name, s3c, args.preserve_keys)
dl = d.download_dir()
print('Error Downloading objects from S3 %s' % dl)

#### Get a directory tree
l = S3helper(args.prefix, dir, args.bucket_name, s3c, args.preserve_keys)
tree = l.tree()
print(tree)