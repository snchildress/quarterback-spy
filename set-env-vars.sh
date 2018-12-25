# iterate through the provided env's env var; e.g. prod
for VAR in $(cat "${1}.env");
do
  # parse the VAR into a NAME and VALUE variable delimited by a = 
  IFS='=' read -r NAME VALUE <<< "$VAR"
  # set the env var in AWS SSM Param Store
  aws ssm put-parameter --type String --profile personal --region us-east-1  --overwrite --name "$NAME" --value "$VALUE"
done
